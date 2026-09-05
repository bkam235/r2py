# r2py v0.3 — Architecture

This document specifies the architecture for a clean rewrite of `r2py`, an R→Python
code translator. It supersedes `v0.1/`. It is the authoritative reference for the
implementation session that follows.

**Where this sits in the transpiler design space.** Source-to-source translators
fall into three broad camps: (1) **rule/grammar-based** rewriters with hand-maintained
API-mapping tables (deterministic, but brittle and non-transferable); (2) **LLM-based**
translators (fluent, but unverified and prone to hallucinated APIs and whole-program
semantic errors); and (3) **execution-verified / feedback-driven** translators, which
ground learning in whether the output *runs equivalently* (TransCoder-ST's test-based
self-training, the RLEF execution-feedback line). `r2py` is a **camp-three** system,
with one distinguishing move: the learning is **externalized into an inspectable,
human-readable skill library** (the Pattern Library, §6) rather than baked into model
weights. The verification signal — "does the Python reproduce the R's effects?" — is
language-pair-agnostic, which is what makes this a proof-of-concept for *transferable*
translation learning (R→Python today; COBOL→Python, etc., later) rather than an
R-specific tool. Design choices throughout are evaluated against that transfer goal:
mechanisms that would only work for R→Python are avoided or quarantined as removable
seeds (see §6.7, §3.7).

The design is informed by:
- `requirements.md` — the requirements
- `CLAUDE.md` — the simplicity and surgical-change guidelines
- four design decisions made before drafting (see §0)

---

## 0. Design decisions locked in before drafting

| # | Decision | Implication |
|---|----------|-------------|
| D1 | **Seed translation is whole-file**; the agent and verifier operate on entities. | Stage 4 score decomposition operates on entities; the seed translator produces a whole-file translation in one LLM call with entity sentinels injected afterward. |
| D2 | **Sandboxes use subprocess + isolated workdir** *only if* they can capture ALL main and side effects. Where a side-effect class cannot be captured by that mechanism, the architecture must say so explicitly and propose a per-effect capture strategy (see §2.2). | No silent gaps. Every effect class has a named capture path. |
| D3 | **Pattern Library = markdown files + generated JSON index.** | Human-reviewable, diff-friendly. Hand-editing allowed. |
| D4 | **LLM judge is last-resort fallback only**, opt-in, disabled by default. | Avoids v0.1's failure mode where the judge pushed exact re-implementation. |
| D5 | **The loop is verbal reinforcement learning + a verified skill library**, not policy-gradient / weight-update RL. The LLM is frozen; all learning lives in the (non-parametric, human-readable) Pattern Library. | Learning is falsifiable, attributable, and diff-reviewable. No online weight updates inside the accept/reject loop (the v0.1 contamination risk). |
| D6 | **Optional learned components are allowed only in bounded, off-by-default, offline-trained slots — currently the retrieval reranker (§6.4).** The reward (Stage 4 comparators) is never learned and never trained online. | Keeps reward ungameable (no learned reward → no reward-hacking surface); learned parts only re-order vetted patterns, still verified before acceptance. |

---

## 1. System overview

```
                       ┌─────────────────────────────┐
                       │  Stage 0 — Substrate        │
                       │  - Sandboxes (R, Py)        │
                       │  - Effect capture           │
                       │  - Env / package install    │
                       │  - Example harvesting       │
                       └──────────────┬──────────────┘
                                      │  (sandbox runs, effect bundles)
                                      ▼
  R script  ──►  ┌──────────────────────────────────────────────────────┐
                 │  Stage 1 — Static + Dynamic Analysis                 │
                 │  Walks AST, runs script and unevaluated branches,    │
                 │  catalogs entities + side-effects, looks up package  │
                 │  sources, emits structured map.                      │
                 └──────────────────────────────┬───────────────────────┘
                                                │  ScriptMap
                                                ▼
                ┌───────────────────────────────────────────────────────┐
                │  Seed + Agent loop + verified skill library            │
                │                                                       │
                │  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
                │  │  Seed    │───▶│ Verify   │───▶│  Agent   │──┐      │
                │  │(whole-   │    │(Stage 4) │    │(whole-   │  │      │
                │  │ file)    │    │          │    │ file     │  │      │
                │  └──────────┘    └─────┬────┘    │ rewrite) │  │      │
                │                        │         └──────────┘  │      │
                │                        ▼                        │      │
                │                  Pattern Library ◄──────────────┘      │
                │                  (verified wiki)                       │
                └───────────────────────────────────────────────────────┘
                                      │
                                      ▼
                              Python script + verification report
```

The seed + agent loop forms a **verbal-reinforcement-learning loop over a
verified skill library** (cf. Reflexion's episodic-memory verbal RL and Voyager's
skill library — no gradients, no weight updates; the LLM is frozen and *all*
learning is the non-parametric Pattern Library, per D5):
- **Seed**: a single whole-file LLM call translates the R script to Python,
  guided by Pattern Library entries and R source lookups. Multiple seeds
  (best-of-N) are tried if the first is below threshold.
- **Agent**: if the seed score is below threshold, a reasoning agent receives
  the full R source, the current Python translation, and per-entity verification
  scores. It does whole-file rewrites, optionally probing R to understand
  specific behavior.
- **Acceptance requires strict improvement**: a rewrite is adopted only if
  `new_score > best_score`.
- The Pattern Library is the **skill library** (a case base of verified,
  human-readable rules).
- Updates accepted while translating script A are visible while translating
  script B (online, cross-script in-context learning).
- The loop halts on `best_score ≥ threshold` or `iterations ≥ max_iterations`.

---

## 2. Stage 0 — Substrate

Stage 0 provides the execution and learning infrastructure that all other stages
consume. It has no knowledge of translation.

### 2.1 Module layout

```
r2py/stage0/
├── sandbox/
│   ├── base.py            # Sandbox protocol
│   ├── r_sandbox.py       # Rscript subprocess + workdir
│   ├── py_sandbox.py      # python subprocess + workdir
│   └── isolation.py       # temp workdir, env scrubbing, resource limits
├── effects/
│   ├── bundle.py          # EffectBundle dataclass
│   ├── stdout.py          # text capture
│   ├── files.py           # workdir snapshot/diff
│   ├── graphics.py        # plot capture (PNG, ggplot/matplotlib)
│   ├── data.py            # serialized data values (JSON, parquet, RDS→JSON)
│   ├── html.py            # HTML/dashboards (shiny, htmltools, plotly)
│   ├── env.py             # R/Python session state (globals after run)
│   ├── warnings.py        # warning/error/message channels
│   ├── rng.py             # captured RNG state, for replay
│   └── network.py         # HTTP/DB request capture (httr/curl/requests/urllib)
├── env/
│   ├── r_runtime.py       # Rscript discovery, R version, find_r_library()
│   ├── py_runtime.py      # interpreter discovery
│   ├── package_installer.py  # CRAN install, pip install, lockfile
│   ├── package_source.py  # locate installed package source files
│   └── r_env_setup.py     # hermetic R environment setup
└── harvest/
    ├── crawler.py         # carried over (functionally) from v0.1/crawler
    ├── extractors.py
    └── writer.py
```

### 2.2 Effect capture — what is captured, and how

A `Sandbox.run(script, capture=…)` returns an `EffectBundle`. The bundle is the
**ground truth** for what a script "did". Stage 4 compares two bundles.

| Effect class | R capture | Python capture | Normalized form for comparison |
|--------------|-----------|----------------|--------------------------------|
| stdout / stderr | tee subprocess streams | tee subprocess streams | UTF-8 text → embedding |
| Assigned values (the "namespace") | injected epilogue saves all globals to `_r2py_state.json` (or parquet for frames) via a recursive serializer; objects that are not natively JSON-serializable (e.g. `htmltools.Tag`, `lm` model, S4) are serialized via a per-type adapter that returns a deterministic structured form (e.g. `as.character(htmltools::renderTags(x)$html)`) | inject epilogue that pickles + JSON-serializes globals via the same per-type adapter table | **Numeric / structured (scalars, vectors, arrays, data frames): exact typed comparison** — dtype + shape + value within tolerance (§7.3), *not* embedding. **Embedding only as an opt-out fallback** (`data_compare`) when exact comparison fails for an *infrastructure* reason rather than a value reason. Free-text/opaque values: text → embedding. |
| Files written to workdir | workdir snapshot (sha256 + size + mime) before/after | same | per-file: text → embedding; binary → byte hash; image → image embedding |
| Plots | open a PNG device before the script, save afterwards (`png()` / `dev.off()`); also save any explicit `ggsave`, `dev.copy` outputs | matplotlib `Agg` backend; capture all open figures; same for plotnine/plotly (saved via `to_image`) | image embedding |
| HTML / dashboards (shiny, htmltools, htmlwidgets, plotly) | force render to HTML string via `htmltools::renderTags()` / `htmlwidgets::saveWidget`; do not store live `Tag` objects | force render via `shiny.ui` → string; plotly via `to_html` | HTML text → DOM-normalized text → embedding |
| Markdown / RMarkdown output | knit to HTML via `rmarkdown::render` (only when entrypoint is `.Rmd`) | jupytext / nbconvert if equivalent | HTML embedding |
| Warnings, messages, errors | `withCallingHandlers` capturing condition objects → JSON list | `warnings.catch_warnings` + exception capture | sorted text list → embedding |
| Environment changes (options, locale, env vars, working dir) | diff `options()`, `Sys.getenv()`, `getwd()` before vs after | diff `os.environ`, `sys.path`, `cwd` | JSON diff (exact compare) |
| RNG draws | `setHook("base::Random.user", …)` to log all `runif`/`rnorm`/etc. calls; or simpler: replace via stub functions that log and call through | monkey-patch `random.*` and `numpy.random.*` at session start | ordered list of `(fn, args, value)` tuples — used for capture/replay, not direct comparison |
| Network / DB calls | `httr`/`curl`/`DBI` wrappers logged | `requests`/`urllib`/`sqlite3` wrappers logged | ordered list of `(verb, target, payload_hash)` |

**Capture mechanism details:**

- The sandbox runs the script with a generated **preamble** (sets up capture hooks)
  and **epilogue** (serializes captured state). The user's script is wrapped, never
  edited.
- Subprocess + temp workdir is the isolation primitive. The workdir is the *only*
  place the script can write; we configure `setwd()` / `os.chdir()` and pass it
  via env vars. We do **not** trust the script to stay in the workdir — we snapshot
  the workdir before and after and only treat workdir contents as "files written".
  Out-of-workdir writes are detected by comparing a recursive listing of `$HOME` /
  `%USERPROFILE%` content hashes (sampled) before/after; if any change, the
  sandbox raises `SandboxEscape` and the run is rejected.
- Per-type adapters live in `effects/data.py` as a registry:
  `register_serializer(type_predicate, fn)`. Adding support for a new
  non-serializable object is a one-function change — this is the explicit answer to
  the JSON-opacity failure in v0.1 (`failure.md` §2).
- When the sandbox cannot capture an effect class (e.g. an interactive prompt,
  GUI window), the run returns an `EffectBundle.uncapturable` field listing the
  unsupported call sites. Stage 4 treats `uncapturable` as a hard signal that
  the LLM judge fallback may be needed; it is never silently ignored.

### 2.3 Sandbox API (contract for other stages)

```python
class Sandbox(Protocol):
    def run(self, source: str, *, workdir: Path,
            capture: CaptureSpec,
            preamble: str = "", epilogue: str = "",
            seed: int | None = None,
            replay: ReplayLog | None = None,
            timeout_s: float = 60) -> EffectBundle: ...
```

`CaptureSpec` is a set of enabled effect classes. `ReplayLog` lets Stage 4
re-run a script with deterministic RNG draws and stubbed-out IO (capture/replay
mode, for testing unevaluated branches against earlier state).

### 2.4 Package installation

`package_installer.install(r_packages=[…], py_packages=[…])` is idempotent and
versioned. It writes a lockfile (`work/lock.json`) used by all stages so two
sandbox runs of the same script see the same package versions. CRAN and Bioconductor
are supported via `install.packages` / `BiocManager::install`; PyPI via `pip install`.

### 2.5 Example harvesting

The `harvest/` module crawls public R repos (GitHub search, CRAN sources, RPubs)
for `.R` scripts that exercise common idioms / packages. Carried over functionally
from v0.1/crawler — interface stays the same, internals may be cleaned up.
Harvested scripts are stored under `work/inputs/harvested/` and are eligible
inputs for the translator. **They never auto-populate the Pattern Library** —
see §6.

---

## 3. Stage 1 — Script analysis

### 3.1 Goal

Produce a **ScriptMap**: a typed, structured representation of every entity in
the R script and every side-effect each entity will or could cause, including
inside unevaluated branches.

### 3.2 Module layout

```
r2py/stage1/
├── ast.py              # parse R via tree-sitter-r (no rpy2 dep for parsing)
├── walker.py           # depth-first AST traversal with branch tracking
├── entities.py         # Entity, EntityKind, EntityRef
├── effects.py          # SideEffect taxonomy
├── runner.py           # uses stage0 to execute script / branch / slice
├── branch_extractor.py # build a runnable slice for an unevaluated branch
├── package_lookup.py   # resolves library() symbols → installed source files
├── coverage.py         # AST-node coverage tracker
└── script_map.py       # ScriptMap dataclass + serialization
```

### 3.3 The ScriptMap data model

```
ScriptMap
├── source: str                       # original R
├── ast_root: AstNode                 # parsed AST
├── entities: dict[EntityId, Entity]  # see EntityKind below
├── effects: list[SideEffect]         # ordered by execution position
├── branches: dict[BranchId, BranchAnalysis]
├── external_sources: dict[EntityId, SourceLocation]
└── coverage: CoverageReport          # fraction of AST nodes analyzed
```

`EntityKind` (non-exhaustive): `Variable`, `Constant`, `FunctionDef`,
`FunctionCall`, `LibraryImport`, `Formula`, `S4Class`, `R6Class`, `Environment`,
`ExternalSymbol`.

`SideEffect.kind` matches Stage 0's effect classes (§2.2) so the verifier can
compare them 1:1.

### 3.4 Analysis procedure

For each AST node, in execution order:

1. **Static classification** — pure AST inspection. Records syntactic entity kind,
   names defined / used, dataflow edges, and *predicted* side-effects (e.g. a
   `write.csv` call is statically known to be a file write).
2. **Dynamic confirmation** — Stage 0 runs the script (or the largest slice
   reaching this node). The actual `EffectBundle` is attached to nodes that
   executed.
3. **Branch extraction for unevaluated nodes** — if a node was not visited
   dynamically (false `if`-branch, uncalled function body, `tryCatch` error
   path), `branch_extractor` builds a minimal runnable slice:
    - Snapshot of the R session state at the parent node (captured in step 2).
    - The branch body, with synthesized inputs derived from the parent
      scope's types.
    - This slice is run in a fresh sandbox seeded with the snapshot.
4. **External source lookup** — for every `ExternalSymbol` (a name resolved to
   a package), `package_lookup` finds the installed source file and adds a
   `SourceLocation` reference. The source text is loaded lazily (the seed
   translator only reads it when it actually needs to translate that symbol).
5. **Coverage tracking** — every AST node is marked `analyzed` | `dynamic` |
   `branch-extracted` | `unreachable`. Stage 1 loops until coverage of
   reachable nodes is 100% or a max-attempts budget is exhausted.

### 3.5 Output format

`ScriptMap` is serialized two ways:

- **Machine-readable** — `script.map.json`, the canonical form.
- **Human-readable** — `script.annotated.R`, the original R source with
  `# r2py:` comments inserted next to each entity referencing the relevant
  `script.map.json` entry id. This is the form the seed translator reads.

### 3.6 What Stage 1 does *not* do

- It does not propose translations.
- It does not score anything.
- It does not modify the Pattern Library.

### 3.7 Pervasive R-semantic gotchas — annotated statically here, not learned

A class of R/Python differences are **whole-program, language-level semantics**,
not package idioms. LLM translation (D1) is structurally prone to miss them,
because each is invisible in a local reading and only manifests in how the
surrounding code *composes* (see the discussion accompanying this change). They
are also too pervasive to be worth re-discovering as Pattern Library entries on
every script.
So Stage 1 detects and annotates them **statically**, inline in
`script.annotated.R`, as first-class `SideEffect`/typing notes that the seed
translator must honour and Stage 4 can check:

- **1-based vs 0-based indexing** and inclusive ranges (`x[1]`, `x[1:n]`,
  `seq_len`, negative-index *exclusion* vs Python negative-index-from-end).
- **Vector recycling** in arithmetic/comparison (`x + y` with unequal lengths)
  and **implicit vectorization** of scalar-looking ops.
- **`NA` semantics**: `NA` is not `None`/`NaN`; `NA` propagation, three-valued
  logic, `na.rm`, typed `NA` (`NA_integer_` …). Annotated so the data comparator
  (§7.3.1) maps them deterministically.
- **Scalar-vs-length-1-vector**: R has no scalars; `length(x)==1` vectors must
  not silently become Python scalars where it changes behaviour.
- **Copy-on-modify / value semantics** vs Python's reference semantics
  (aliasing hazards introduced by a naive translation).
- **Lazy evaluation / promises** and **non-standard evaluation (NSE)** — `dplyr`,
  `ggplot2`, `subset()`, formulas capture *unevaluated* expressions; the
  argument is not a value. Flagged because the LLM translator will otherwise
  eval them eagerly and produce subtly wrong code.
- **`<<-` super-assignment** and other scope escapes (these are cross-entity
  dataflow edges, recorded as such).
- **Dispatch**: S3/S4/R6 method resolution, so the translator knows a call site is
  polymorphic. Stage 1's `package_lookup` follows `UseMethod("name")` dispatch
  to fetch `name.default` source recursively.
- **Platform-specific calls** (`Sys.setlocale`, `with_locale`, `with_envvar`,
  etc.): flagged as `platform_specific` so the translator applies OS-safe patterns
  (e.g. POSIX→Windows locale name mapping).
- **Vector-constructor functions**: `complex(n)`, `raw(n)`, `logical(n)`,
  `integer(n)`, `character(n)`, `numeric(n)`, `double(n)` called with a single
  integer `n` create a **vector of n elements**, not a type conversion. Flagged
  as `vector_constructor` so the translator uses numpy equivalents (e.g.
  `np.zeros(int(n), dtype=...)`).
- **Python-keyword argument names**: R uses identifiers like `from`, `in`,
  `as`, `class`, `return`, etc. freely as function parameter names (e.g.
  `chunk(from=1, to=100, by=10)`, `seq(from=1, to=10)`). These are Python
  reserved keywords and produce a `SyntaxError` when used on the left side of
  `=` in a function call or definition. Stage 1 detects each occurrence and
  flags the enclosing entity with `python_keyword_arg:<kw>` (e.g.
  `python_keyword_arg:from`). The seed translator surfaces these flags in the
  entity metadata section of the prompt as explicit `WARNING: R uses Python
  keyword(s) as arg names: <kw> -> rename to <kw>_val` notes. As a deterministic
  safety net, `stage2.stitch.sanitize_keyword_args()` is applied to every LLM
  output (in both the seed path and the agent rewrite path) before syntax
  checking: it renames `kw=` → `kw_val=` consistently in definitions AND call
  sites using regex, ensuring the generated code is at least syntactically valid
  even when the model forgets to rename call sites.
- **Positional arguments after keyword arguments**: R allows named arguments
  (`class="mt-5"`) to appear before unnamed positional arguments in any function
  call. Python requires all positional arguments to precede keyword arguments —
  a `SyntaxError` results otherwise. LLMs frequently mirror the R source argument
  order when translating bslib/shiny UI calls (e.g. `card(class_="mt-5",
  card_header(...), "text")` where the named `class_=` is first). As a deterministic
  safety net, `stage2.stitch.reorder_positional_before_kwargs()` is applied to
  every LLM output (in both the seed path and the agent rewrite path) before
  syntax checking: it uses Python's `tokenize` module to detect function calls
  where a keyword argument precedes a positional argument and reorders them
  (positional first, keyword last), iterating from innermost to outermost call.
  This is a language-level invariant, not a package idiom, so it lives here rather
  than in the Pattern Library.

These annotations are the *handles* agent rewrites and Stage 4 comparisons attach
to. Package-specific idioms remain the Pattern Library's job; these language
invariants do not, because they are not learnable per-package signal — they are
true everywhere.

---

## 4. The translation loop

### 4.1 Loop control

```python
ScriptMap m = stage1.analyze(r_script)

# Step 1: Whole-file seed translation (best-of-N).
seed, entity_line_map = seed.translate(m, library, model=cheap_model)
best_score, best_decomp = stage4.verify(m, seed)

# Try additional seeds if first is below threshold.
for i in range(n_seeds - 1):
    if best_score >= threshold: break
    alt, alt_map = seed.translate(m, library, model=cheap_model)
    alt_score, alt_decomp = stage4.verify(m, alt)
    if alt_score > best_score:
        seed, best_score, best_decomp = alt, alt_score, alt_decomp

if best_score >= threshold: return seed

# Step 2: Escalate to reasoning agent.
# The agent sees the full R source + current Python + per-entity scores.
# It does whole-file rewrites (action: "rewrite") or R probes (action: "probe_r").
result = agent.reason(
    current_source=seed,
    score_report=best_decomp,
    harness=harness,      # provides verify() and probe_r()
    script_map=m,
    model=escalation_model,
    max_steps=max_iters,
)
```

Exposed via the top-level API:

```python
from r2py import translate

translate(
    r_path="analysis.R",
    py_path="analysis.py",
    max_iters=20,         # default; agent step budget
    score_threshold=0.85, # default; user-tunable
    n_seeds=3,            # best-of-N seed attempts before agent escalation
    model="claude-haiku-4-5",         # cheap model for seed
    escalation_model="claude-sonnet-4-6",  # stronger model for agent
    use_judge=False,      # opt-in; off by default (D4)
    data_compare="auto",  # exact-first, embedding fallback on infra mismatch (§7.3)
)
```

### 4.2 Online learning, catastrophic forgetting

Pattern Library updates from script A persist when script B runs. The library's
**confidence levels** (§6) and **contradiction log** are the defense against
catastrophic forgetting: a pattern that helped on A but hurts on B records the
hurt as a contradiction. After K contradictions on a `confirmed` pattern, it is
auto-demoted to `tentative`; after K more, to `contradicted`. The retriever
never shows `contradicted` patterns as examples.

---

## 5. Seed translation

### 5.1 Goal

Produce a whole-file Python translation of the input R script in a single
LLM call, guided by the Pattern Library and R source lookups.

### 5.2 Module layout

```
r2py/
├── seed.py              # whole-file seed translation (entry point)
└── stage2/
    ├── llm.py           # Anthropic / OpenRouter API client (shared with agent)
    ├── stitch.py        # data shim, entity line map, shim-override removal
    └── walker.py        # topological ordering of entities
```

### 5.3 Whole-file translation (D1)

The seed translator (`r2py/seed.py`) sends the **entire R script** to the LLM
in one call, along with:

1. The full R source in a code block.
2. **Retrieved patterns** from the Pattern Library for each entity in the
   ScriptMap — presented as guidance with examples.
3. **R source lookups** for unattributed function calls — the actual R package
   source for functions used in the script.

The system prompt instructs the LLM to use real Python libraries (not stubs),
drop R documentation scaffolding (`withAutoprint`, `is_interactive` wrappers),
and follow Pattern Library guidance.

After receiving the translation, the seed module:
- Injects `# r2py:entity:<id>` sentinel comments via heuristic name matching,
  enabling per-entity verification scoring by Stage 4.
- Adds the data shim (commented-out code block for test-time equivalence
  checking).
- Adds a header with provenance metadata.

**Sentinel mapping robustness.** The sentinel mapper (`stage2/sentinel_mapper.py`)
asks an LLM to assign non-overlapping Python line ranges to each entity. Smaller
models (e.g. Gemma via OpenRouter) occasionally return overlapping ranges. The
parser now auto-resolves overlaps by greedy clipping: ranges are sorted by start
line, and each range is clipped to end just before the next range starts.  The
clipped range is dropped if it becomes empty (start > end).  If the mapper still
fails after one retry + clipping, `seed.py` catches `SentinelMappingError` and
falls back to an empty mapping: the translation proceeds with aggregate-only
scoring rather than crashing.

Multiple seeds (best-of-N) are tried if the first is below the score threshold.

### 5.4 What the seed does *not* do

- It does not score its output — Stage 4 scores.
- It does not modify the Pattern Library — all writes are channeled through
  the learning-from-translation path after verification.

---

## 6. The Pattern Library (the "verified wiki")

This module replaces v0.1's `pairs_db/` AND `optimizer/wiki/`. It is owned by
the architecture as a whole; conceptually it sits beside the stages and is
read by the seed translator and written only by Stage 4.

### 6.1 Module layout

```
r2py/library/
├── pattern.py           # Pattern dataclass + (de)serialization
├── store.py             # filesystem store (one .md per pattern)
├── index.py             # JSON index for fast retrieval
├── retrieval.py         # query by (package, AST shape, effect class)
├── reranker.py          # optional LambdaMART reranker (D6, §12.6 A)
├── epistemology.py      # confidence transitions, conflict resolution
└── writer.py            # the *only* module allowed to mutate patterns
```

### 6.2 Pattern format (one `.md` file)

```markdown
---
id: shiny.tag_as_str
package: shiny
confidence: confirmed   # confirmed | tentative | contradicted
created: 2026-01-12
last_review: 2026-05-20
---

# Render Tag objects to string before capture

## Guidance
`htmltools.Tag` objects are not JSON-serializable and become opaque in
namespace capture. Translate `ui <- page_fluid(…)` to
`ui = str(shiny.ui.page_fluid(...))` so the verifier can compare the
rendered HTML.

## Evidence
- shiny__rd_example__req_Rd.R → score 0.878 (path: embedding, variable: ui)
- shiny__simple_input.R → score 0.91 (path: embedding, variable: ui)

## Contradictions
(none)
```

### 6.3 What goes in, and how

A pattern entry is created **only when an edit improved a score AND a human
or automated reviewer named the underlying rule**. The `writer` module enforces:

1. Every new pattern must declare `package`, `guidance`, and at least one
   `evidence` entry.
2. Evidence records the **verification path** (embedding vs. stdout fallback
   vs. judge) and the **specific variable** that scored. Past v0.1 stored
   only the overall script score — see `failure.md` §1.1 and §3.1.
3. A pattern is added with `confidence: tentative` until it has evidence
   from ≥2 distinct scripts in ≥1 distinct package. Then it can be promoted
   to `confirmed` by the epistemology module.
4. The agent / Stage 4 may **only** append to the `Contradictions` section of
   an existing pattern. They cannot rewrite `Guidance`. Rewriting `Guidance`
   requires a new pattern with new evidence — this prevents the
   monotonically-growing self-contradicting prompt failure of v0.1
   (`failure.md` §1.2).

### 6.4 Retrieval

Retrieval is **package-first, AST-shape second, source-similarity last**:

1. Filter patterns by the packages the current R entity uses.
2. Within that set, rank by AST-shape similarity (compare AST node-type
   sequences, not tokens).
3. Tie-break by raw token similarity.

Source-similarity-only retrieval (Jaccard, embeddings) is **not used** —
it was the root cause of v0.1's stub contamination (`failure.md` §1.1).

`retrieve(entity, k=3) -> list[Pattern]` returns at most `k`, and each pattern
returned is `confirmed` or `tentative`. `contradicted` patterns are never
shown to the translator.

The ranking in steps 2–3 is the default heuristic. When `learned_retrieval=True`
(off by default, D6) the heuristic ordering is replaced by the optional learned
reranker of §12.6(A), which only re-orders this same already-filtered candidate
set — it can never surface a `contradicted` pattern or alter guidance.

### 6.5 Epistemology rules

Implemented in `epistemology.py`, applied by `writer` on every change:

| Event | Effect |
|-------|--------|
| New evidence on pattern P with score ≥ threshold | append to `Evidence` |
| Edit following pattern P scores **below** target | append to `Contradictions` |
| Contradictions ≥ ⌈ |Evidence| / 2 ⌉ | demote P (`confirmed` → `tentative`; `tentative` → `contradicted`) |
| Two `confirmed` patterns give conflicting guidance for the same (package, AST shape) | both demoted to `tentative`; a `conflict.md` note is written for human review |
| `contradicted` pattern unchanged for N days | archived (moved out of index, file kept) |

The `confidence` field, the contradictions counter, and demotion are the
**falsification signal** that v0.1 lacked.

**Departure from original design (promotion rule).** The original specification
required promotion evidence from **≥ 2 distinct script IDs**. This was changed to
**≥ 2 genuine improvement evidence entries regardless of script identity**. Reason:
the distinct-script requirement made promotion impossible for a small or single-script
corpus — a pattern confirmed dozens of times on one script would never graduate,
leaving the library permanently tentative. The amended rule still requires two
independent acceptance events (two separate loop iterations, potentially across
different runs), preserving the spirit of "more than one confirmation" without
blocking small-corpus users. If cross-script diversity becomes important again, the
threshold can be tightened by requiring `len(distinct_scripts) >= 1 and
len(real_evidence) >= 2` as a middle ground.

**Departure from original design (review cadence).** The original intent was to
call `epistemology.review()` only when the library was mutated (evidence or
contradictions added). Changed to **unconditional, once per loop run**. Reason:
promotion and archival must fire even on high-scoring runs that needed no edits,
otherwise the library can hold stale tentative patterns indefinitely.

### 6.6 Index

`library/index.json` is regenerated on every write; never hand-edited. It maps
`(package, ast_shape_hash) -> [pattern_id]` and stores per-pattern metadata
(`confidence`, evidence count, contradictions count) for fast retrieval without
opening each `.md`.

### 6.7 The Pattern Library *is* the equivalence registry (learned, not curated)

A tempting alternative is a hand-curated **preferred-equivalent registry**
(`dplyr::filter → polars.filter`, `ggplot2 → plotnine`, …) consulted first by
the seed translator. We deliberately **do not** build that as a separate, authored artifact.
The whole point of this project is a *transferable* learning mechanism (camp-three,
see intro): a curated R→Python mapping table is exactly the kind of scaffolding
that would inflate R→Python scores while transferring *nothing* to COBOL→Python —
it would let us fool ourselves about what the system has learned.

Instead, **API equivalences are ordinary patterns, learned by trial and error**:
a `ReplaceCall` / `ReplaceLibrary` edit (§8.3) that improves the score becomes
evidence on a pattern such as `dplyr.filter ↔ polars.filter`, promoted by the
same confidence machinery (§6.5) as everything else. The "registry" is therefore
an *emergent view* of the library, not a separate store; `r2py library list
--kind mapping` can render it, but it is never authored by hand or consulted
ahead of the normal retrieval path.

**Cold-start seed (deliberately tiny).** To bootstrap the very first runs, the
library MAY ship a small set of seed mapping patterns — order **~10–20**, only
the highest-frequency idioms — each flagged `seed: true` in its front-matter.
Seeds are subject to the same contradiction/demotion rules as learned patterns;
they get no special standing. The tiny size is intentional: enough to avoid a
cold-start stall, small enough that the system must *learn* the long tail.

**Transfer measurement.** Because seeds are flagged, the corpus can be evaluated
**with seeds removed** (`--no-seeds`) to measure how much the mechanism relearns
on its own. If R→Python collapses without seeds, that is a *finding* about the
mechanism's transfer potential — not something to paper over with a bigger seed
table. This is the central PoC metric, not an afterthought.

---

## 7. Stage 4 — Verification

### 7.1 Goal

Given a ScriptMap (R) and a candidate Python translation, produce a decomposed
score per entity per effect class, plus a single aggregate.

### 7.2 Module layout

```
r2py/stage4/
├── verifier.py          # orchestrator
├── comparators/
│   ├── base.py          # Comparator protocol + text_similarity (difflib / embedding)
│   ├── stdout.py
│   ├── data.py          # JSON / dataframe / array (per-variable scoring)
│   ├── files.py
│   ├── graphics.py
│   ├── html.py
│   ├── env.py
│   ├── warnings.py
│   ├── exit_code.py     # process exit code comparison
│   ├── network.py       # HTTP/DB request log comparison
│   └── rng.py           # RNG draw log comparison
├── decompose.py         # entity × effect-class score table + crash attribution
├── replay.py            # capture/replay for unevaluated branches & RNG
├── fuzz.py              # differential fuzzing harness (§7.8)
├── generators.py        # type/grammar-derived input generators (§7.8)
├── judge.py             # last-resort LLM judge (disabled by default — D4)
└── wiki_update.py       # the writer that mutates the Pattern Library
```

### 7.3 Comparators

Each comparator implements:

```python
class Comparator(Protocol):
    effect_class: EffectClass
    def compare(self, r_effect, py_effect) -> ComparatorResult: ...
```

`ComparatorResult` carries a scalar in `[0, 1]`, a verdict (`pass` / `fail` /
`uncomparable`), and a free-text explanation used to build edit feedback.

Adding a new effect class is a two-file change: a capturer in `stage0/effects/`
plus a comparator here. This is the modularity / extensibility property
required by the outline.

#### 7.3.1 Numeric / structured comparison: exact-first, embedding-fallback

`comparators/data.py` does **not** score numeric or structured values by
embedding similarity (embedding distance is a soft, reward-hackable target for
values that have a ground truth). It compares **exactly and by type**:

1. **Type/shape gate**: dtype compatible (R `numeric`↔`float`, `integer`↔`int`,
   `logical`↔`bool`, factor↔categorical, etc.), and shape/length/column-set
   equal. `NA`/`NaN`/`NULL`/`None` handled explicitly (see §3.7).
2. **Value compare**: numeric within tolerance `|a−b| ≤ atol + rtol·|b|`
   (defaults `rtol=1e-6`, `atol=1e-9`, configurable per run); exact for
   integer/logical/string; set/multiset compare for unordered structures.
3. **Verdict**: `pass` / `fail` with the first differing element reported in
   the explanation (this is what the agent's feedback consumes).

A failure is tagged either `value` (the numbers really differ — a real defect,
never masked) or `infra` (structurally uncomparable for a reason that is *not*
a value disagreement: R vs Python print/format differences, serialization
quirks, column-ordering or attribute noise the normalizer didn't catch,
float-formatting in a stringified frame, etc.).

The `data_compare` switch governs only the `infra` case:

- `data_compare="exact"` — never fall back; an `infra` failure stays `fail`.
- `data_compare="embedding"` — always score this effect by embedding (the v0.1
  behaviour; provided for comparison / debugging only).
- `data_compare="auto"` (**default**) — try exact first; on an **`infra`-tagged**
  failure only, fall back to embedding similarity and return
  `verdict=pass_via_fallback` with the scalar from the embedding comparator.
  A `value`-tagged failure is **never** rescued by the fallback.

`pass_via_fallback` is recorded in the `EntityScore` and surfaced in the score
report, so a human can see exactly which entities were scored on the weaker
signal and why — fallbacks are visible, never silent.

### 7.4 Score decomposition

The verifier returns a structured score:

```python
@dataclass
class ScoreReport:
    aggregate: float
    by_entity: dict[EntityId, EntityScore]
    by_effect: dict[EffectClass, float]
    uncomparable: list[EntityId]   # opaque or sandbox-uncapturable
    feedback: list[FeedbackItem]   # per-entity natural-language hints
```

Each `EntityScore` further decomposes (echoing the outline):

- `executed_ok: bool`
- `type_match: float`
- `control_flow_match: float`
- `data_output: float`
- `variable_output: float`
- `callable_output: float`
- `side_effects: float`
- `judge_pass: Optional[bool]`  *(only when judge is enabled)*

This is the **granular signal** the agent consumes.

**Empty-vs-empty entity scoring.** When both R and Python per-entity bundles exist
but neither side produced observable effects (no data, no stdout, no graphics), the
entity scores 1.0 — both sides are silent, which is execution equivalence by
definition.  This is implemented in `decompose.py`'s `make_score_table`: when
`proxy_scores` is empty (R emitted nothing) and Python also emitted nothing, a
synthetic `[1.0]` is injected into `proxy_scores` instead of falling through to the
global data score.  The path is guarded by `entity_executed_ok` (Python must not have
crashed) and both bundles being present (not `None` — a `None` bundle means the
checkpoint wasn't reached, not that the entity produced nothing).  A diagnostic
message is printed to stdout when this path fires.

This resolves the prior known limitation where R infrastructure wrappers like
`suppressPackageStartupMessages(library(...))` scored as low as ≈ 0.083–0.267 despite
being correctly translated: the wrapper produces no observable effects in R, and the
Python equivalent (a silent `import`) also produces nothing — a perfect match that
was previously penalised by an unrelated global data score.  The fix is general: it
applies to any entity where both sides are genuinely silent, learned from execution
equivalence rather than hardcoded function names.

**R bundle deduplication.**  When two entities share overlapping source spans (e.g.
`suppressPackageStartupMessages(library(...))` wrapping a `library()` call), the R
checkpoint ordering may attribute effects to the outer entity that actually belong
to the inner.  `make_score_table` detects strictly-nested source spans and clears
the outer entity's R bundle so it scores via empty-vs-empty instead.

**Python checkpoint namespace baseline.**  The Python checkpoint preamble
(`_PY_CHECKPOINT_PREAMBLE` in `verifier.py`) initialises `_r2py_prev_ns` as the
empty set.  Without correction the first entity's checkpoint would capture all
module-level imports and data-shim variables as spurious "effects".
`_inject_py_checkpoints` therefore inserts a namespace snapshot
(`_r2py_prev_ns = set(…)`) immediately before the first entity's start line, so
that the first checkpoint delta only includes variables the entity itself
introduced.

**Remaining limitation — R `.onAttach` stdout.**  When R's per-entity checkpoint
captures stdout from a package's `.onAttach` hook (not suppressed), the per-entity
STDOUT comparator correctly scores 0.0 against Python's silent import.  This is an
inherent R→Python asymmetry (package loading in R can produce stdout that has no
Python equivalent) and is accepted: such entities are few per script and the penalty
is modest.

### 7.5 Unevaluated branches

For each `BranchAnalysis` produced by Stage 1 (false `if`, uncalled function),
the verifier:

1. Reconstructs the parent-state snapshot from Stage 1's slice.
2. Runs the R branch under that snapshot in a Stage 0 sandbox.
3. Runs the *corresponding* Python branch (located via per-entity translation
   metadata from the seed translator) under a Python sandbox seeded with the translated
   parent state.
4. Compares effects exactly as for the main path.

For RNG-dependent code or data unavailable in both languages, the sandbox runs
in **replay mode**: R's RNG draws are logged on the R run, then injected as a
fixed sequence into Python's stubbed RNG (or vice versa). Same for I/O whose
sources are not reproducible.

### 7.6 LLM judge — fallback only (D4)

Invoked only when **all** comparators return `uncomparable` for an entity AND
`use_judge=True`. Its verdict influences only that entity's score, not the
aggregate weighting. The judge prompt is constrained to the Pattern Library's
`Guidance` for the relevant package — it has no freedom to insist on exact
R re-implementation. It cannot, structurally, push for stub-style code.

### 7.7 Pattern Library mutation

`wiki_update.py` is the **only** code in the system that calls
`library.writer.*` mutators. The mutations it performs:

- After an accepted edit (strict improvement, `new_score > parent_score`,
  §4.1): if the edit was attributed (by the agent) to an existing pattern, append
  evidence; if it was attributed to a *new* named pattern, create it with
  `confidence: tentative`.
- After a tie (`new_score == parent_score`): record weak evidence
  (`record_tie`) on the attributed pattern; the candidate is **not** accepted.
- After a rejected edit (regression) attributed to an existing pattern: append
  to that pattern's `Contradictions`.
- Periodically (every N translations): run `library.epistemology.review()`
  to apply demotions / archival.

This is the architectural fix for `failure.md` §1.2: every change to the
library has a named cause, is validated by a re-run before being persisted
(the score change *is* the validation), and contradictions are first-class.

### 7.8 Differential fuzzing over derived input generators

Stages 1 and 7.5 establish equivalence on essentially **one** execution path —
the script's own inputs (plus reconstructed branch states). Two programs can
agree on one input and diverge on others, so single-path agreement is a weak
equivalence guarantee. `fuzz.py` strengthens it by **differential testing**: run
the R original and the candidate Python on *many* generated inputs and require
their effect bundles to match on each, with the **R program as the oracle**.

This is **not** v0.1's discarded `input_gen.py` (which asked an LLM to invent
synthetic inputs — hallucination-prone, off-distribution). Inputs here are
**derived, not invented**:

1. **Generators from types** (`generators.py`). For each free input an entity
   consumes, Stage 1's type/structure info (§3) plus the *observed* value in the
   captured `EffectBundle` define a generator — a grammar in the QuickCheck /
   Hypothesis sense: sample length, dtype, value range, `NA`-rate, factor levels,
   data-frame column types + row count, etc., **constrained to the observed
   domain**. No LLM is in this loop.
2. **Boundary augmentation.** Generators add a few principled edge cases the
   observed value may not cover: empty, length-1 (the R scalar-vs-vector trap,
   §3.7), `NA`-present, and extreme magnitudes.
3. **Differential run.** For each generated input, Stage 0 runs R and Python
   under the same seed / replay log (§2.3) and the §7.3 comparators score the two
   effect bundles. Any input on which they disagree is a counterexample.
4. **Scoring & feedback.** The entity's effect score becomes agreement across
   the input *distribution*, not a single point. The first counterexample (its
   input + the diverging effect) is handed to the agent as `FeedbackItem` — far
   more actionable than a scalar.

Coverage is the dial. Generators stay **inside the observed domain** with only
light boundary extension: too loose tests inputs the R script never legitimately
sees (false counterexamples); too tight collapses back to one path. The fuzz
budget (inputs per entity) is bounded and configurable; fuzzing is on for the
final verification of a candidate and can be sampled (not exhaustive) during the
inner loop for cost.

This directly addresses the finite-sampling weakness of execution-only
verification noted in the RL-for-code literature (rewards that sample finitely
from an infinite input space invite specification-gaming); the R oracle keeps the
expanded check grounded without trusting a model to produce inputs.

#### 7.8.1 Structured test categories

Cai & Li (2025, "r2py: AI-Assisted Conversion of R Statistical Packages to
Python", arXiv:2608.16911v2) independently arrived at a similar differential
testing design and found that structuring generated tests into three explicit
categories improved coverage over random fuzzing alone:

1. **Positive tests.** Exercise documented parameter combinations against the R
   oracle — the happy path. Maps to our random samples from `generator_from_observed`.
2. **Negative tests.** Supply inputs the function should reject (wrong type,
   out-of-range, missing required arg) and assert that R and Python raise
   comparable errors — or at minimum that Python does not silently produce a
   wrong answer. Our generators do not yet probe this axis.
3. **Boundary tests.** Empty, single-element, non-finite (`Inf`, `NaN`, `NA`),
   and degenerate (singular matrix, zero-variance column) values. Our
   `boundary_cases()` covers empty and length-1; the non-finite and degenerate
   classes are a natural extension.

**Adoption plan:** extend `generators.py` to emit tagged cases (`positive`,
`negative`, `boundary`) so `fuzz.py` can report which *category* a
counterexample falls into. The agent can then prioritise structural fixes
(negative) over numeric-tolerance issues (boundary).

#### 7.8.2 Per-assertion tolerances

Statistical functions often produce results that are correct but differ at the
floating-point level between R and Python (different LAPACK builds, different
default optimisers). The paper applies per-assertion tolerances rather than a
single global `rtol`/`atol`, because the acceptable margin differs between a
p-value (~1e-6) and a test statistic (~1e-10). Our comparators already accept
`rtol`/`atol` at the comparator level; a future refinement is to let the fuzz
harness supply per-variable tolerances derived from the entity's effect class
(e.g. tighter for deterministic linear algebra, looser for iterative optimisers).

#### 7.8.3 Iterative bug resolution loop

The paper's Phase 7 runs generated tests, passes the **first failure's
traceback** to a repair agent, rebuilds, and repeats until all tests pass or a
budget is exhausted. This is structurally identical to our §8 reasoning agent
loop (rewrite → verify → iterate), except that our "verify" step currently uses
the single observed execution plus fuzz counterexamples, whereas the paper
dedicates a full generated-test-suite run as the inner verifier. The key insight
worth adopting: feeding the agent **one failure at a time** (rather than all
failures) focuses each repair step and reduces cascading rewrites. Our
`FeedbackItem` list already supports this — the ordering heuristic (worst entity
first, §8) is the lever.

#### 7.8.4 Historical test suite translation (future, package-level)

When translating an entire R package (not a single script), the package's own
test suite (`tests/`, `testthat/`) is a free source of high-quality test
specifications. The paper translates these tests to Python and runs them as an
additional verification layer. This is not applicable to v0.3's single-script
scope but becomes immediately relevant when we move to package-level translation
(see §15, backlog item "dependency-ordered translation").

---

## 8. Reasoning agent

### 8.1 Goal

When the seed translation scores below threshold, the reasoning agent
iteratively improves it. The agent sees the full R source, the current Python
translation, per-entity verification scores, and Pattern Library guidance.
It decides what to change and produces whole-file rewrites.

### 8.2 Module layout

```
r2py/harness/
├── agent.py             # reason() loop — iterative tool-use agent
├── prompt.py            # system prompt + tool descriptions for the agent
└── tools.py             # HarnessTools — verify, apply_edit, read wrappers
```

### 8.3 Agent actions

The agent operates via tool use with two primary actions:

- **`rewrite`**: submit a complete rewritten Python translation. The harness
  verifies it via Stage 4; the rewrite is accepted only on strict score
  improvement.
- **`probe_r`**: execute an R expression in the sandbox to understand specific
  R behavior before rewriting.

The agent receives the full verification decomposition (per-entity scores,
comparator feedback) and can target its rewrites at the weakest entities.

### 8.4 What the agent does *not* do

- It does not modify the Pattern Library directly — library updates happen
  via the learning-from-translation path after successful translations.
- It does not modify system prompts or any guidance file.

---

## 9. Top-level API and CLI

### 9.1 Python API

```python
from r2py import translate, analyze

# end-to-end
result = translate("analysis.R", "analysis.py",
                   max_iters=20, score_threshold=0.85,
                   n_seeds=3)

# stage 1 only
script_map = analyze("analysis.R")
```

`TranslateResult`:

```python
@dataclass
class TranslateResult:
    python_source: str
    final_score: float
    iterations: int
    score_history: list[ScoreReport]
    pattern_evidence_added: list[str]
    pattern_contradictions_added: list[str]
```

### 9.2 CLI

```
r2py analyze   <input.R>                  # writes input.map.json + input.annotated.R
r2py translate <input.R> <output.py>      # full pipeline
r2py library list [--package P] [--confidence C] [--kind mapping]  # mapping = the emergent equivalence registry (§6.7)
r2py library show <pattern_id>
r2py library review        # run epistemology pass
r2py library train-reranker [--min-episodes 500] [--out work/models/reranker/]  # offline reranker training (§12.6 A); → scripts/train_reranker.py
r2py ablation [--slice work/inputs/ablation_slice.txt] [--compare frozen-vs-learning|heuristic-vs-learned]  # manual paired ablation (§12.4.1); → scripts/run_ablation.py
r2py harvest <repo_or_url> # stage0 example harvester
```

Additional standalone scripts in `scripts/`:

```
scripts/translate.py           # single-script translator (sys.path-safe entry point)
scripts/translate_batch.py     # batch runner over work/inputs/
scripts/run_ablation.py        # manual paired ablation (§12.4.1)
scripts/train_reranker.py      # offline LambdaMART training (§12.6 A)
scripts/reset_library.py       # reset Pattern Library to seed-only state
```

The `--no-seeds` flag (on `translate` / `translate_batch`) ignores `seed: true`
patterns for the transfer experiment of §6.7.

---

## 10. Work folder

```
work/
├── inputs/              # carried over from v0.1; example R scripts
│   ├── curated/         # human-vetted
│   └── harvested/       # from stage0/harvest
├── outputs/             # one folder per translation run
│   └── <script>__<ts>/  # python output, score reports, edit log, sandbox bundles
├── lock.json            # package versions (stage0/env)
├── translated_packages/ # cached package source translations
├── models/              # OPTIONAL learned artifacts (D6, §12.6); absent → heuristics used
│   ├── reranker/        # versioned LightGBM lambdarank models + training manifest
│   └── policy/          # versioned contextual-bandit artifacts (if §12.6 B enabled)
└── analysis/
    ├── learning_curve.csv   # score over time across translations
    ├── scoring_table.csv    # per-script latest scores
    ├── run_history.jsonl    # per-run metadata (script, score, iterations, timestamp)
    ├── ablation/            # one folder per manual ablation run (§12.4.1): A/B scores, B−A, regressions
    └── plots/               # generated by `r2py library review`
```

`translate.py` (the v0.1 batch runner) is carried over functionally as
`scripts/translate_batch.py` — iterate over `work/inputs/`, write results to
`work/outputs/`, append rows to `analysis/learning_curve.csv` and
`analysis/scoring_table.csv`.

`scripts/train_reranker.py` is the **offline** reranker trainer (§12.6 A;
CLI `r2py library train-reranker`). It is run manually, never by the translation
loop: it consumes the logged outcomes under `work/outputs/`, trains the LightGBM
`lambdarank` model with the hyperparameters of §12.6, evaluates it with
grouped-by-script CV against the heuristic baseline, and writes a versioned
artifact into `work/models/reranker/` only on a held-out win. Its sibling
`scripts/train_policy.py` (if §12.6 B is pursued) trains the contextual bandit
from logged `(context, edit, score_delta)` transitions; same offline, gated
discipline.

`scripts/run_ablation.py` is the **manual** ablation harness (§12.4.1; CLI
`r2py ablation`). It is never invoked by CI or the loop. It reads a pinned slice
manifest (`work/inputs/ablation_slice.txt` — the committed 100–300 stratified
script list), runs the slice twice (library frozen vs learning on, identical
seeds/`max_iters`), and writes per-script A/B scores, the aggregate B − A with a
significance check, and the regression list to `work/analysis/ablation/<ts>/`.
With `--compare heuristic-vs-learned` it instead gates the optional learned
components of §12.6.

---

## 11. What from v0.1 is reused vs. discarded

| v0.1 component | Disposition |
|----------------|-------------|
| `stage0/checker.py` | Discarded — replaced by `stage0/sandbox/` and `stage0/effects/`. |
| `stage1/annotator.py`, `rules.py`, `scope.py` | Conceptually carried over into v0.2 stage1, but the deterministic-rules approach is reduced — most rule logic now lives in the per-type adapter registry (§2.2) and in Stage 1's static classification. |
| `stage1/method_enumerator.py` | Carried over as `package_lookup.py`. |
| `stage2/llm.py` | Reused as `stage2/llm.py` (Anthropic/OpenRouter client + retry). Used by both the seed translator and the agent. |
| `stage2/method_translator.py`, `wiki_filter.py` | Folded into `library/retrieval.py` and seed prompt construction. |
| `stage3/executor.py`, `embedder.py`, `aligner.py`, `branch_extractor.py` | Reused functionally inside `stage4/` and `stage0/effects/`. |
| `stage3/judge.py`, `input_gen.py` | `judge.py` reused but constrained (§7.6); `input_gen.py` discarded **as an LLM input generator**. Its *role* (extra inputs for verification) is replaced by type/grammar-derived differential fuzzing (§7.8), which derives inputs from observed types with the R script as oracle — no LLM-generated synthetic inputs. |
| `stage3/verifier.py` | Carried over as `stage4/verifier.py` with score decomposition added. |
| `stage4/translator_agent.py` | Discarded. Replaced by the reasoning agent harness (§8). |
| `stage5/` | Discarded as a distinct stage. Self-improvement is now intrinsic to the seed+agent loop. |
| `optimizer/` (compiler, gradient, updater, wiki_writer, epistemology, …) | Replaced wholesale by the Pattern Library (§6) and `stage4/wiki_update.py` (§7.7). |
| `pairs_db/pairs.json` | Discarded as a format. Curated seed patterns will be re-authored as Pattern Library `.md` files. |
| `error_patterns.jsonl` | May feed the Pattern Library as initial `Contradictions` entries during bootstrap, after manual review. Not auto-imported. |
| `crawler/` | Carried over into `stage0/harvest/`. |
| `tracking/` | Carried over functionally into `work/analysis/`. |
| `prompts/translate.txt` | Replaced by fixed system prompts in `seed.py` and `harness/prompt.py`. **Not mutable at runtime.** |

---

## 12. Cross-cutting properties

### 12.1 Determinism

- Every sandbox run records its seed, package lockfile hash, and effect bundle.
- A `(ScriptMap hash, model, library snapshot hash)` tuple is recorded with
  every translation. Re-running with the same tuple should reproduce the same
  Python within consistency thresholds.

### 12.2 Modularity and extensibility

- A new effect class needs a capturer (`stage0/effects/`) + a comparator
  (`stage4/comparators/`). No other module changes.
- A new sandbox backend (e.g. Docker, if subprocess proves insufficient)
  implements the `Sandbox` protocol — no caller changes.

### 12.3 Observability

Every run writes:
- `work/outputs/<run>/effect_bundle.r.json`
- `work/outputs/<run>/effect_bundle.py.{iter}.json`
- `work/outputs/<run>/score_report.{iter}.json`
- `work/outputs/<run>/edits.log.jsonl`
- `work/outputs/<run>/library_diff.json`  (patterns touched, evidence added, contradictions added)

These are how a human debugs a translation without re-running it.

### 12.4 Testing strategy

- **Stage 0**: per-effect-class capture tests against known R/Python fixtures.
  Tests must include the JSON-opacity case (`Tag`, `lm`, S4) explicitly.
- **Stage 1**: AST + branch extraction tests against curated R fixtures.
- **Seed**: no dedicated unit tests yet for `seed.py`'s prompt construction;
  covered indirectly by `test_loop.py`, which mocks `seed.translate` at the
  loop-control level.
- **Agent harness**: integration test with a mock LLM verifying the
  rewrite/verify loop.
- **Stage 4**: each comparator has its own test suite. The verifier has
  golden-file tests against known-equivalent and known-inequivalent
  R/Python pairs.
- **Library**: epistemology transitions are pure functions; full unit coverage.
- **End-to-end is *not* run on every merge.** Full-pipeline translation invokes
  the LLM loop and dual sandboxing, which is slow and token-costly — in v0.1 even
  10–15 scripts cost ~1–2 days and €5–10 per pass, so gating merges on it is not
  worth the friction. CI runs only the **cheap, deterministic** tests above
  (Stage 0, Stage 1, seed, Stage 4 unit tests, comparator suites, and the verifier's golden-file
  known-equivalent / known-inequivalent pairs — no translation loop, no live
  API). End-to-end behaviour is exercised **manually** via the ablation slice
  (§12.4.1), not in CI.

#### 12.4.1 Manual ablation slice (is the learning net-positive?)

The `learning_curve.csv` from the batch runner is only *observational* — a rising
curve can be easier scripts arriving later, or noise, not learning. To get a
controlled answer, run a **stratified held-out slice** as a deliberate experiment,
**by hand**, never in CI:

- **Slice**: a fixed **100–300 scripts** sampled from `work/inputs/`, stratified
  across packages and difficulty so the result generalizes. The slice is pinned
  (its script list is committed) so runs are comparable over time.
- **Paired run**: translate the slice **twice** under identical seeds and
  `max_iters` — (A) **library frozen**: retrieval on, but `wiki_update` writes
  (evidence, contradictions, promotions) disabled for the duration; (B)
  **learning on**: normal. The paired score delta **B − A** on the slice is the
  evidence that cross-script learning helps (or hurts).
- **Cadence**: run after meaningful library growth or before a release — *not*
  per-commit. It is two passes over ~200 scripts, not two passes over the whole
  3000+ corpus, which keeps the cost bounded and predictable.
- **Trigger**: a standalone script, `scripts/run_ablation.py` (CLI
  `r2py ablation`, §9.2), reads the pinned slice, performs both passes, and writes
  `work/analysis/ablation/<ts>/` containing per-script A/B scores, the aggregate
  B − A with a significance check, and the list of scripts where learning
  regressed (the actionable part).
- **Doubles as the D6 gate**: the same harness, run with `--compare
  heuristic-vs-learned`, is how the optional reranker / policy (§12.6) earn their
  keep — ship a learned component only if it beats the heuristic on this slice.

The full 3000+ corpus stays a **single** batch pass feeding `learning_curve.csv`;
only the pinned slice is ever run twice.

### 12.5 Safety against v0.1 failure modes

| v0.1 failure | v0.2 architectural defense |
|--------------|---------------------------|
| Stub pairs embed-matching simple scripts and contaminating future runs (`failure.md` §1.1) | Patterns require named guidance; evidence records verification path and variable; package-first retrieval; no auto-promotion from raw score. |
| Optimizer mis-diagnoses and pollutes global guidance (`failure.md` §1.2) | No mutable global prompt; only the Pattern Library is mutable; mutations gated by attribution and re-run score; rejected edits become contradictions. |
| Conflicting guidance sources (`failure.md` §1.3) | Single source of truth (Pattern Library). System prompt is static, version-controlled, non-mutable. Stage 1 annotations are inline and not retrievable as examples. |
| JSON-opacity trap (`failure.md` §2) | Per-type serializer registry in `stage0/effects/data.py`. Opaque variables are reported in `EffectBundle.uncapturable`, never silently skipped. Stage 4 surfaces opacity in feedback. |
| Side-effect-only score ceiling of 0.75 (`failure.md` §3.3) | Score decomposition is per effect class; no implicit ceilings. Uncomparable entities surface explicitly — they do not silently push the run to a fallback path. |

### 12.6 Optional learned components (off by default — D6)

Both components below are **off by default**, **trained offline only**, and sit
**behind the existing heuristics as a fallback**. Neither touches the reward:
Stage 4 comparators stay deterministic, so there is no learned-reward surface to
hack. Both consume only already-logged data (§12.3), and the trained artifact
hash is added to the determinism tuple (§12.1).

**(A) Learned retrieval reranker** — replaces the hand-ordered ranking in §6.4.

- *What it changes*: only the **order** of candidate patterns that are *already*
  `confirmed`/`tentative` and already passed the package-first filter. It cannot
  surface a `contradicted` pattern, invent a pattern, or alter guidance — so
  every safety property of §6 is preserved. This is a learning-to-retrieve setup
  in the spirit of RLCoder (RL for code-retrieval), but kept offline + supervised.
- *Recommended model*: **LambdaMART (gradient-boosted trees via LightGBM/XGBoost)**
  with a listwise NDCG objective over engineered features — package match,
  AST-shape similarity, token similarity, pattern `confidence`, evidence count,
  contradiction count, historical accept-rate of the pattern, recency. GBDT
  rerankers are the workhorse of learning-to-rank, are interpretable (feature
  importances are reviewable, matching D3's spirit), and remain competitive
  with — often better than — neural rerankers at small data scale. A neural
  cross-encoder is explicitly *not* recommended first: it is data-hungry and
  opaque. Label = 1 if the pattern, when followed, produced an accepted edit
  (strict improvement), else 0; or graded by score-delta.
- *Data before first training*: do not train until **≥ ~500 logged retrieval
  episodes** with accept/reject outcomes (ideally ≥ 1–2k); below ~200 the
  heuristic wins — keep it. Always gate behind an **A/B against the heuristic on
  held-out scripts** — the manual ablation slice of §12.4.1, run with
  `--compare heuristic-vs-learned`: ship the learned reranker only if it
  measurably beats the heuristic.
- *Offline training trigger*: `scripts/train_reranker.py` (CLI: `r2py library
  train-reranker`, §9.2). It is **offline and manual** — never invoked from the
  translation loop. It reads logged outcomes from `work/outputs/*/edits.log.jsonl`
  + `library_diff.json`, joins each retrieved candidate to its accept/tie/reject
  label, builds the feature vectors above grouped by retrieval query (one query
  = one entity's candidate set), trains a LightGBM `lambdarank` model, evaluates
  it, and — only if it beats the current ranker on the held-out split — writes a
  versioned artifact to `work/models/reranker/`. It refuses to run below the data
  threshold.
- *Recommended hyperparameters* (LightGBM, tuned for the small-data, listwise
  regime; conservative to avoid overfitting):

  ```python
  params = dict(
      objective="lambdarank",
      metric="ndcg", ndcg_eval_at=[1, 3],
      boosting_type="gbdt",
      num_leaves=15,            # shallow: small data, avoid overfit
      min_data_in_leaf=30,      # strong leaf regularization
      learning_rate=0.05,
      feature_fraction=0.8,
      bagging_fraction=0.8, bagging_freq=1,
      lambda_l1=1.0, lambda_l2=1.0,
      max_position=3,           # we only ever show k=3 (§6.4)
  )
  # num_boost_round up to 500 with early_stopping_rounds=50 on the val NDCG@3.
  # Cross-validation: GROUPED k-fold BY SCRIPT (never split one script's
  # patterns across train/val) to prevent leakage; report NDCG@1/@3 vs the
  # heuristic baseline. Ship only on a win.
  ```

The reranker defaults to the existing heuristic if its model artifact is absent,
below the data threshold, or losing the held-out A/B — so enabling D6 is
strictly opt-in upside with a clean fallback.

---

## 13. Implementation order (for the next session)

1. **Stage 0 substrate** (sandbox, effects/data + adapter registry, env, harvest).
2. **Stage 1 analysis** (AST walker, branch extractor, ScriptMap, package lookup,
   §3.7 static R-semantic gotcha annotation).
3. **Pattern Library** (pattern format, store, index, retrieval, epistemology,
   writer; seed with the **tiny ~10–20 `seed: true` mapping set**, §6.7 — not a
   large curated registry).
4. **Stage 4 verifier + comparators** (depends on §1 effect classes), including
   §7.3.1 exact/typed data comparison with `data_compare` fallback, and §7.8
   differential fuzzing (`fuzz.py`, `generators.py`).
5. **Seed translator** (depends on §2, §3) — whole-file LLM translation with
   pattern library guidance and R source lookups.
6. **Reasoning agent** (depends on §2, §3, §4) — iterative improvement via
   whole-file rewrites.
7. **Top-level loop, API, CLI** (depends on all above) — seed + agent
   strict-improvement loop (§4.1).
8. **End-to-end corpus tests + learning curve scaffolding**, plus the **manual
   stratified ablation slice** (`scripts/run_ablation.py`, §12.4.1) — the
   controlled way to prove learning is net-positive. End-to-end is deliberately
   *not* wired into per-merge CI (cost; §12.4).
9. **Optional learned components last** (D6, §12.6): `scripts/train_reranker.py`
   then, only if warranted, the bandit policy. These are built *after* enough
   loop data exists to train and A/B them — never before.

Each step has its own success criteria (per CLAUDE.md §4); they will be set
during implementation, not here.

*All 9 steps are complete — see Sessions 1–12 in §14. Session 11 closed the 9
deferred architecture gaps (wiki_update API, ast_shape_hash, network capture,
`_py_to_r` complex objects, for-loop branch extraction, judge LLM wiring,
embedding similarity, per-entity score decomposition, per-iteration score
report artifacts). Session 12 fixed loop-stability issues (entity-targeting,
exhausted-parent pruning, tie-break ordering) and added crash attribution
(`EffectBundle.preamble_lines`, `decompose._attribute_crash`).*

---

## 14. Implementation log

Each session appends to this section. Format per entry: what was built, what
was deferred and why, and any choices that deviate from or extend the spec.

---

### Session 1 — Chapters 0–1 (scaffolding, shared types, CLI skeleton)

**Implemented**

| File | Notes |
|------|-------|
| `pyproject.toml` | setuptools build backend (not hatchling — `setuptools.backends.legacy` was unavailable in the installed version; `setuptools.build_meta` used instead). Optional dep groups: `rpy2`, `models`. |
| `r2py/__init__.py` | `translate()` and `analyze()` stubs, both raise `NotImplementedError` with architecture-step references. `Path` import deferred to avoid unused import. |
| `r2py/__main__.py` | Delegates to `cli.main()`. |
| `r2py/types.py` | All shared types. See implementation choices below. |
| `r2py/cli.py` | argparse CLI; all 5 commands from §9.2 (`analyze`, `translate`, `library`, `harvest`, `ablation`); all flags from §9.1 including `--no-seeds`. Unimplemented commands raise `NotImplementedError`. |
| `r2py/stage{0–4}/__init__.py` | Importable skeletons; public entry points raise `NotImplementedError`. |
| `r2py/stage0/{sandbox,effects,env,harvest}/__init__.py` | Empty sub-package declarations. |
| `r2py/stage4/comparators/__init__.py` | Empty sub-package declaration. |
| `r2py/library/__init__.py` | `_StubLibrary` + `get_library()` raising `NotImplementedError`. |
| `work/inputs/{curated,harvested}/` | New dirs (plural) — deliberately distinct from v0.1's `work/input/` to prevent accidental overwrites. |
| `work/outputs/`, `work/translated_packages/`, `work/models/{reranker,policy}/`, `work/analysis/{ablation,plots}/` | §10 directory layout. |
| `work/lock.json` | Empty `{}` package lockfile; stage0/env will populate on first run. |
| `scripts/{translate_batch,train_reranker,run_ablation}.py` | Docstring-only stubs referencing the relevant architecture sections. |
| `tests/test_types.py` | 19 tests covering enum counts, dataclass defaults, and design-decision invariants (D2 `uncapturable`, D4 `judge_pass`, `pass_via_fallback` verdict). |

**Deferred**

- `r2py/loop.py` — the §4.1 beam-search loop deferred to **step 7** of §13.
  It cannot be meaningfully implemented or tested before Stages 1–4 and the
  Pattern Library exist. When step 7 arrives, `loop.py` is its first deliverable:
  implement `run_loop()` with `_state_hash()` / `_top_k()` helpers, wire it into
  `translate()` in `__init__.py`, and cover the beam/tabu/strict-improvement
  invariants with unit tests using Protocol stubs.

**Implementation choices for `r2py/types.py`**

- `Edit` lives in `types.py`, not `stage3/`, because `Proposal` (a loop-level
  type) and `library.record_evidence(edit, …)` both reference it. Putting it in
  `stage3/` would create a circular import: `loop → stage3 → library → loop`.
- `CaptureSpec = frozenset[EffectClass]` — a proper generic alias rather than
  bare `frozenset`, so type checkers enforce the element type.
- `T | None` used throughout instead of `Optional[T]`; `Optional` import removed.
  The file already has `from __future__ import annotations` so runtime evaluation
  of annotations is deferred and the `|` syntax works on Python 3.10+.
- All `dict`/`list` field annotations are parameterized (e.g.
  `dict[EntityId, EntityScore]`, `list[bytes]`) rather than bare, so type
  checkers can validate callsites.
- `ScriptMap` is a one-field placeholder (`source: str = ""`). Stage 1 will
  import and extend it (or define a richer subclass). The placeholder is
  intentionally minimal to keep `from r2py.types import ScriptMap` working
  before Stage 1 is written.

**Verification (all passing)**

```
pip install -e .
python -c "import r2py; print(r2py.__version__)"          # → 0.2.0
python -c "from r2py.types import EffectClass, Edit; print('ok')"
python -c "import r2py.stage0, r2py.stage1, …, r2py.library; print('ok')"
python -m r2py --help                                      # lists all 5 commands
python -m r2py translate --help                            # shows all flags
python -m pytest tests/test_types.py -v                   # 19 passed
```

---

### Session 2 — Chapter 2 (Stage 0 — Substrate)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/stage0/sandbox/base.py` | `Sandbox` Protocol (`@runtime_checkable`), `ReplayLog` dataclass, `SandboxEscape` exception. |
| `r2py/stage0/sandbox/isolation.py` | `TempWorkdir` context manager, `scrub_env()`, `snapshot_home()` + `check_escape()` for out-of-workdir write detection. |
| `r2py/stage0/sandbox/r_sandbox.py` | `RSandbox` — assembles preamble/epilogue from enabled effect modules, runs `Rscript --vanilla`, collects `EffectBundle`. |
| `r2py/stage0/sandbox/py_sandbox.py` | `PySandbox` — same pattern for Python subprocess. |
| `r2py/stage0/effects/bundle.py` | `to_json` / `from_json` / `save` / `load` / `merge` helpers. `EffectBundle` stays in `types.py`. |
| `r2py/stage0/effects/stdout.py` | `collect()` decodes subprocess bytes to `stdout`/`stderr` strings. No preamble/epilogue needed. |
| `r2py/stage0/effects/files.py` | `snapshot()`, `diff()`, `collect()` — sha256-based workdir before/after diff. |
| `r2py/stage0/effects/graphics.py` | R: `png()` device + `ggsave` hook; Python: `matplotlib Agg` backend. `collect()` reads `_r2py_plot_*.png`. |
| `r2py/stage0/effects/data.py` | Per-type adapter registry (`register_r_adapter`, `register_py_adapter`). Built-in adapters for data frames, htmltools Tag, lm/glm, S4, numpy, pandas. R/Python epilogues write `_r2py_state.json` + `_r2py_uncapturable.json`. |
| `r2py/stage0/effects/html.py` | R epilogue renders htmltools/htmlwidgets → string; Python renders plotly → HTML. |
| `r2py/stage0/effects/env.py` | R/Python preamble snapshots options/envvars/cwd; epilogue diffs and writes `_r2py_env.json`. |
| `r2py/stage0/effects/warnings.py` | R: `options(warning.expression=…)` hook; Python: `warnings.showwarning` monkey-patch. |
| `r2py/stage0/effects/rng.py` | R/Python preambles for capture and replay modes. `ReplayLog` injection injects pre-recorded draws. |
| `r2py/stage0/env/r_runtime.py` | `find_rscript()` (PATH → Windows paths → Unix paths), `r_version()`. |
| `r2py/stage0/env/py_runtime.py` | `find_python()` (R2PY_PYTHON env var → `sys.executable`), `python_version()`. |
| `r2py/stage0/env/package_installer.py` | Idempotent `install(r_packages, py_packages, lockfile)`. Reads/writes `work/lock.json`. Supports `bioc::` prefix for Bioconductor. |
| `r2py/stage0/env/package_source.py` | `find_r_package_source()` via `find.package()`; `find_py_package_source()` via `importlib.util.find_spec()`. |
| `r2py/stage0/harvest/crawler.py` | `crawl()` dispatches to GitHub API (tree listing + raw download), CRAN `.tar.gz`, single `.R` URL, RPubs HTML scrape. |
| `r2py/stage0/harvest/extractors.py` | `extract()` handles `.R`, `.Rmd`/`.qmd` (code chunk extraction), `.tar.gz` (recursive). |
| `r2py/stage0/harvest/writer.py` | `save()` — sha256-named files, sidecar `.meta.json`, deduplication. |
| `r2py/cli.py` | `cmd_harvest` wired to `crawl()` (previously `NotImplementedError`). |
| `tests/test_stage0_sandbox.py` | 16 tests: protocol conformance, TempWorkdir, scrub_env, PySandbox live runs (hello world, exit code, stdout, data, seeded, files), RSandbox skipped without Rscript. |
| `tests/test_stage0_effects.py` | 26 tests: bundle round-trip/merge, stdout, files snapshot/diff, graphics collect, data adapter registry + uncapturable D2 invariant, html/warnings/rng collect, PySandbox uncapturable integration. |
| `tests/test_stage0_env.py` | 13 tests: py_runtime path/version, R2PY_PYTHON override, find_rscript absent, package_installer idempotency + lock write, package_source. |

**Deferred**

- Network capture (`EffectClass.NETWORK`) — preamble/epilogue hooks for `httr`/`curl` (R) and `requests`/`urllib` (Python) not implemented. The `EffectClass.NETWORK` enum value exists; a capturer will be a one-file addition when needed. Noted in `EffectBundle.network_log` which is always present (D2).
- Home-snapshot escape detection is a best-effort tripwire (samples up to 2000 files, 4 KB per file). Full audit would require OS-level file-system monitoring; this is sufficient for the subprocess isolation model.

**Implementation choices**

- `effects/warnings.py` uses `options(warning.expression=…)` rather than `withCallingHandlers` wrapping (which would require the sandbox to split preamble/body/epilogue into three separate injection points). The options-hook approach is simpler and captures warnings during epilogue execution too.
- `effects/data.py` R epilogue uses inline `if/else` instead of the adapter registry loop (which would require generating dynamic R code). The inline version is clearer and covers all the cases the architecture specifies.
- `PySandbox` passes `scrub_env()` to the subprocess. On Windows, `SYSTEMROOT`, `WINDIR`, and `COMSPEC` are included in the allow-list because many subprocesses require them; without them, even `python.exe` fails to start on some Windows configurations.
- `PROCESSOR_ARCHITECTURE` is also included in the Windows allow-list. Without it, R packages that invoke native Windows code (e.g. `xfun::cache_rds`) crash the R process with exit code 0xC0000005 (STATUS_ACCESS_VIOLATION). The root cause is that some Windows system DLLs or R extensions read this variable at startup to determine the platform word size; when it is absent the platform detection fails and causes a null-pointer dereference in native code.
- **Tempdir file capture**: `TMPDIR` is set to the sandbox workdir so R's `tempdir()` resolves inside the workdir. An R epilogue (`R_EPILOGUE_FILES` in `effects/files.py`) copies non-internal files from `tempdir()` into `_r2py_tempfiles/` before R's session cleanup removes them. `collect()` then reports these under `tempfile:<basename>` keys.
- **Known limitation — out-of-workdir writes**: The subprocess sandbox only captures file writes to the workdir (including redirected tempdir). Writes to hardcoded absolute paths (`write.csv(x, "C:/Users/foo/out.csv")`), `$HOME`-relative paths, or `download.file()` targets outside the workdir are not captured. The home-snapshot tripwire detects some of these as escapes but does not capture the content. Docker-based isolation would close this gap if the corpus grows beyond CRAN examples where tempdir-based writes are the norm.

**Verification**

```
python -m pytest tests/ -v   # 71 passed, 4 skipped (Rscript absent)
python -m r2py harvest --help  # shows repo_or_url positional arg (not NotImplementedError)
python -c "from r2py.stage0.sandbox.base import Sandbox, ReplayLog; print('ok')"
python -c "from r2py.stage0.effects.data import register_py_adapter; print('ok')"
python -c "from r2py.stage0.env.r_runtime import find_rscript; print('ok')"
python -c "from r2py.stage0.harvest.crawler import crawl; print('ok')"
```

---

### Session 3 — Chapter 3 (Stage 1 — Script analysis)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/stage1/entities.py` | `SourceLocation`, `AstNode`, `EntityRef`, `Entity` dataclasses. `AstNode` holds a reference to the raw tree-sitter node (`_ts_node`) so `child_by_field()` lookups work after the tree is built; it is excluded from repr/compare to avoid noise. |
| `r2py/stage1/effects.py` | `SideEffect` dataclass + `STATIC_PREDICTIONS` table (~20 entries). Minimal by design; the dynamic sandbox run fills gaps. |
| `r2py/stage1/ast.py` | `parse(source)` via `tree_sitter_language_pack.get_parser("r").parse_bytes(...)`. Root is obtained by calling `tree.root_node()` (a method, not a property — the `tree-sitter-language-pack` 1.x API). Recursive `_to_ast_node` converter. |
| `r2py/stage1/coverage.py` | `CoverageReport` + `CoverageTracker`. Status priority (analyzed > dynamic > branch-extracted > unreachable) enforced by `mark()` — upgrades only. |
| `r2py/stage1/script_map.py` | Full `ScriptMap` subclass (7 fields per §3.3) + `BranchAnalysis`. Serialisation: `to_json` / `from_json` / `save` / `load`; `to_annotated_r()` inserts `# r2py: <entity_id>` after each entity's last line. `EffectBundle` serialised via existing `stage0/effects/bundle.py` helpers. |
| `r2py/stage1/walker.py` | Depth-first walk dispatching on tree-sitter node kinds. Classifies `binary_operator` (with `<-`/`=`/`<<-`) into `VARIABLE`, `CONSTANT`, `FUNCTION_DEF`, `S4_CLASS`, `R6_CLASS`, `ENVIRONMENT`; `call` to `library`/`require` into `LIBRARY_IMPORT`; other `call` into `FUNCTION_CALL`. Dataflow edges tracked via identifier scan of RHS. §3.7 annotation pass (`_annotate_r_semantics`) runs after entity extraction and attaches flags (`na_semantics`, `super_assign`, `indexing_1based`, `nse`, `vector_recycling`, `copy_on_modify`, `dispatch_s3s4r6`, `scalar_vs_vector`) by scanning all nodes and flagging enclosing entities. |
| `r2py/stage1/package_lookup.py` | `resolve_symbol(package, symbol)` calls `stage0.env.package_source.find_r_package_source()` then does a text scan of the package's `R/` directory for a matching `symbol <- function(` pattern. |
| `r2py/stage1/runner.py` | `run_script(r_path, capture)` and `run_slice(r_source, capture, parent_state)` bridge to `RSandbox` via `TempWorkdir`. `_py_to_r()` converts Python values from `EffectBundle.data` to R literal strings (int → `L`-suffix, float → repr, str → quoted, list → `c(...)`, None → `NULL`). |
| `r2py/stage1/branch_extractor.py` | `extract_branch(node, parent_entities, parent_bundle)` collects free variable names in the branch text, restores them from `parent_bundle.data`, and prepends an R assignment preamble. Intentionally simple (no session replay); covers the common case. |
| `r2py/stage1/__init__.py` | `analyze(r_path)` pipeline: parse → static walk → sandbox run (gracefully skipped if Rscript absent) → branch extraction loop (max 3 attempts) → package_lookup → ScriptMap. |
| `r2py/__init__.py` | `analyze()` stub replaced with delegation to `stage1.analyze()`. |
| `tests/fixtures/simple.R` | Curated R fixture covering: `library()` import, constant, variable, NA, function def, `print`, `if/else`, `<<-` super-assign, subscript `[1]`, `write.csv` comment. |
| `tests/test_stage1.py` | 76 tests across 9 test classes. All pass. |

**Deferred**

- Branch extraction for `for`/`while` loop bodies — only `if/else` alternative branches are extracted. Loop bodies are typically executed (and therefore dynamically confirmed), so this is low-priority.
- Full session-replay branch extraction (`ReplayLog`) — the current implementation uses `parent_bundle.data` to restore scalar/vector variables. Complex objects (data frames, lists) that cannot be expressed as R literals are silently omitted from the preamble. The `ReplayLog` path described in §2.3 / §7.5 is the full solution; deferred.

**Post-session corrections (found during plan audit)**

Three gaps identified after initial implementation and fixed before closing:

- **`FORMULA` entity kind**: `_visit_assignment` now detects `rhs.kind == "binary_operator"` with `~` operator → `EntityKind.FORMULA`. tree-sitter-r has no `formula` node type — formulas are ordinary `binary_operator` nodes with `~` — so the original plan's node-kind assumption was wrong; corrected to operator-text check via `_is_tilde_op()`.
- **`EXTERNAL_SYMBOL` for `pkg::fn()` calls**: `_visit_call` now checks if the function child's kind is `namespace_operator`; if so, classifies as `EntityKind.EXTERNAL_SYMBOL` and sets `entity.package` to the LHS of the `::`. Previously the kind was unconditionally `FUNCTION_CALL`.
- **`_annotate_r_semantics` formula detection**: changed `if kind == "formula":` (which never matched) to `if kind == "binary_operator" and _is_tilde_op(node):` so formula usage correctly sets the `nse` flag.
- **CLI `cmd_analyze` output**: now writes `<input>.map.json` and `<input>.annotated.R` and prints a summary line. Previously the result was discarded.

**Implementation choices**

- **`tree-sitter-language-pack` API**: Version 1.x uses `parse_bytes(bytes)` (not `parse`), `root_node()` as a method (not property), `node.kind()` as a method, and `Point.row` / `Point.column` as properties (not methods). This differs from both the standard `tree-sitter` 0.21 and 0.22+ APIs; the wrappers in `ast.py` fully abstract it.
- **`ScriptMap` subclass, not in-place mutation**: `stage1/script_map.py` defines `ScriptMap` as a dataclass subclass of `types.ScriptMap` (the minimal one-field placeholder). This keeps `from r2py.types import ScriptMap` working before stage1 is imported, avoiding circular imports, and is consistent with the Session 1 log note ("Stage 1 will import and extend it (or define a richer subclass)").
- **`CONSTANT` vs `VARIABLE` classification**: An assignment whose RHS is a bare literal (`float`, `integer`, `string`, `logical`, `na`) is classified as `CONSTANT`; everything else (including arithmetic expressions, function calls, compound RHS) as `VARIABLE`. This distinction is purely syntactic; R has no `const` keyword.
- **§3.7 annotation strategy**: `_annotate_r_semantics` runs after entity extraction and uses `_flag_enclosing()` which flags every entity whose source span contains the annotated node. This means a large function definition picks up all flags from its body — intentionally broad, matching the architecture's intent that Stage 2 *must honour* these flags when translating the entity.
- **Static prediction table**: 20 entries covering the highest-frequency side-effect-producing functions. The table is not exhaustive; the dynamic run fills gaps. `STATIC_PREDICTIONS` is public so Stage 2 can read it for prompt construction without re-analysing.

**Verification**

```
python -m pytest tests/ -v
# → 149 passed, 4 skipped (Rscript-absent skips from Session 2; all new tests pass)

python -c "from r2py import analyze; print(analyze.__module__)"
# → r2py

python -c "
from r2py.stage1.ast import parse
from r2py.stage1.walker import walk
root = parse('x <- NA\nlibrary(dplyr)\nf <- function(a) a <<- 1\n')
entities, effects = walk(root, 'test.R')
print({e.name: e.r_semantic_flags for e in entities.values()})
"
# → {'x': ['na_semantics'], 'import_dplyr': [], 'f': ['super_assign']}
```

---

### Session 4 — Chapter 4, Step 3 (Pattern Library)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/library/pattern.py` | `EvidenceEntry` + `Pattern` dataclasses. `to_markdown` / `from_markdown` implementing the §6.2 front-matter format. `demotion_threshold()` = ⌈\|evidence\|/2⌉ (min 1). `_parse_body` splits the body into Guidance / Evidence / Contradictions sections. Evidence lines parsed with a regex matching `- {script_id} → score {score} (path: {path}, variable: {var})`. |
| `r2py/library/store.py` | `PatternStore(library_dir)` — one `.md` file per pattern under `library_dir/patterns/`. `rglob("*.md")` so nested seed subdirs are also found. Gracefully skips malformed files on `load_all`. |
| `r2py/library/index.py` | `PatternIndex` backed by `library_dir/index.json`. Two index keys per pattern: exact `(package, ast_shape_hash)` and wildcard `(package, "")`. `upsert_meta` for single-pattern incremental updates (avoids full rebuild on every write). `remove` for archival. |
| `r2py/library/retrieval.py` | `retrieve(entity, k, store, index, no_seeds)` — package-first filter via index, AST-shape token-overlap tier, guidance token-similarity tie-break. `entity_ast_shape_hash` computes an 8-char MD5 of the entity's kind string. `_token_overlap` is Jaccard on whitespace-split tokens. |
| `r2py/library/epistemology.py` | `review(store, index) -> list[str]` — applies all five §6.5 rules in order: (1) contradiction-threshold demotion, (2) conflict detection (two `confirmed` patterns on same package with different guidance → both to `tentative` + `conflict_*.md` note), (3) stale `contradicted` archival (30-day cutoff). Returns human-readable log. |
| `r2py/library/writer.py` | Sole mutator. `record_evidence` / `record_tie` / `record_contradiction` each load-or-create the pattern, append, save, call `_upsert_index`, and (for evidence/contradiction) run `epistemology.review`. No-op if `edit.pattern_id` is None. New patterns start as `confidence: tentative`. |
| `r2py/library/__init__.py` | `PatternLibrary` facade replacing `_StubLibrary`. `get_library(library_dir=None)` defaults to `work/library/`. Auto-rebuilds index if empty on first construction (handles cold start when patterns already exist on disk). |
| `work/library/patterns/*.md` | 15 hand-authored seed patterns (`seed: true`, `confidence: tentative`) covering: `data.frame→pd.DataFrame`, `c()→list/np.array`, `NA→None/pd.NA`, `paste0→f-string`, `sprintf→f-string`, `cat()→print()`, `seq()→range()`, `lapply→list comp`, `which→np.where`, `nrow/ncol→shape`, `read.csv→pd.read_csv`, `write.csv→df.to_csv`, `ggplot2→plotnine`, `dplyr::filter→boolean mask`, `%>%→method chaining`. |
| `tests/test_library.py` | 44 tests across 7 classes. All pass. |

**Deferred**

- `ast_shape_hash` in the index is currently always `""` (package wildcard) at write time; the exact-shape key is never populated because `writer.py` has no entity AST at write time. Stage 2 will pass the entity shape hash when it calls `library.retrieve()`, at which point exact-shape lookups will work. For now, all retrieval falls back to the package-wildcard bucket.
- Conflict detection uses guidance-text inequality as a proxy for conflicting advice. A more precise rule (same R construct → different Python construct) requires Stage 2 context and is deferred.

**Implementation choices**

- `PatternStore.load_all()` uses `rglob("*.md")` rather than a flat `glob("*.md")` so seed files stored in subdirectories (e.g. `patterns/seeds/`) are included. The filename stem must equal the pattern `id` field for `store.get()` to work by convention; `load_all()` uses the `id` from the file content as the dict key, not the filename, so subdirectory paths do not cause key mismatches.
- `PatternIndex.upsert_meta` was added alongside `rebuild` so `writer.py` can do a cheap single-pattern index update rather than scanning all patterns after every write.
- `epistemology._write_conflict_note` creates a new `Pattern` object for the conflict note and saves it via `store.save()` directly (not via `writer.py`) to avoid recursive epistemology calls. This is the only exception to the "writer is the sole mutator" rule.

**Verification**

```
python -m pytest tests/test_library.py -v   # 44 passed
python -m pytest tests/ -v                  # 202 passed, 4 skipped
python -c "from r2py.library import get_library; lib = get_library(); print(lib)"
# → PatternLibrary(dir=work\library, patterns=15)
```

---

### Session 5 — Chapter 7, Step 4 (Stage 4 — Verifier + Comparators)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/stage4/comparators/base.py` | `Comparator` protocol (runtime-checkable via `Protocol`). `text_similarity(a, b)` using `difflib.SequenceMatcher.ratio()` — stdlib only, serves as the injection point for a real cosine-over-embedding later. |
| `r2py/stage4/comparators/stdout.py` | `StdoutComparator` — `text_similarity` on `bundle.stdout`; threshold 0.95. |
| `r2py/stage4/comparators/warnings.py` | `WarningsComparator` — sorts both lists, joins as newline-separated string, then `text_similarity`; threshold 0.95. |
| `r2py/stage4/comparators/env.py` | `EnvComparator` — exact dict equality; explains missing/extra/differing keys; always `failure_tag="value"` (env changes are real, not infra). |
| `r2py/stage4/comparators/files.py` | `FilesComparator` — score = fraction of R-written paths with matching sha256 in Python; extra Python files ignored. |
| `r2py/stage4/comparators/html.py` | `HtmlComparator` — strips tags with a regex, normalises whitespace, then `text_similarity` per HTML item; threshold 0.9. |
| `r2py/stage4/comparators/graphics.py` | `GraphicsComparator` — byte-exact first; if Pillow present, converts to grayscale and uses normalised RMSE (score = 1 − rmse/255); if Pillow absent and bytes differ, returns `uncomparable` (infra gap, not a value failure). |
| `r2py/stage4/comparators/data.py` | `DataComparator` implementing §7.3.1. `_compare_pair` performs a type/shape gate then value compare per variable. Failure tags: `"value"` (numbers/strings actually differ) vs `"infra"` (length mismatch, column-set mismatch, structural type mismatch). `data_compare` switch: `"exact"` keeps infra failures as-is; `"embedding"` always calls `_text_fallback`; `"auto"` (default) rescues only infra-tagged failures. `_text_fallback = text_similarity(str(r), str(py))`. |
| `r2py/stage4/comparators/__init__.py` | `COMPARATORS` dict mapping 7 effect classes to instances. RNG and NETWORK excluded (capture/replay, not direct comparison). |
| `r2py/stage4/decompose.py` | `make_score_table(entities, comparator_results, py_exit_code)` — maps whole-script comparator results onto `EntityScore` objects. `data_output` and `variable_output` = DATA score; `side_effects` = average of FILES, GRAPHICS, HTML, ENV, WARNINGS scores. `type_match`, `control_flow_match`, `callable_output` left at 0.0 (Stage 3 fills these via per-entity analysis). |
| `r2py/stage4/verifier.py` | `verify()` orchestrator: (1) aggregates entity `actual_bundle`s into R ground truth via `bundle.merge()`; (2) runs candidate in `PySandbox`; (3) calls `_compare_bundles()`; (4) calls `make_score_table()`; (5) optionally calls `fuzz.run_fuzz()`; (6) builds `ScoreReport` with aggregate, by_entity, by_effect, uncomparable, feedback. |
| `r2py/stage4/replay.py` | `ReplayLog` dataclass + `capture_r_rng(bundle)` extracts float draws from `rng_log`. `run_branch_pair()` wraps `stage1.runner.run_slice` + `PySandbox.run()` with the extracted replay injected into the sandbox. |
| `r2py/stage4/generators.py` | `ScalarGenerator`, `VectorGenerator`, `DataFrameGenerator` — each constrained to the observed domain (same dtype, same column schema). `boundary_cases()`: empty, length-1 (§3.7 scalar-vs-vector trap), NA-present, extreme magnitudes. `generator_from_observed(value)` dispatches on type. |
| `r2py/stage4/fuzz.py` | `FuzzConfig(n_inputs, seed, timeout_s)`. `run_fuzz()` iterates entities with `actual_bundle.data`, builds generators per input variable, runs boundary + random inputs through R slice (`stage1.runner.run_slice`) and Python slice (`PySandbox`), compares with `DataComparator`, returns first counterexample per entity as `FeedbackItem`. |
| `r2py/stage4/judge.py` | `judge_entity()` stub — returns `None` when `use_judge=False` (D4 default); returns `uncomparable` result when enabled. Full LLM wiring deferred to Stage 3 integration. |
| `r2py/stage4/wiki_update.py` | Sole caller of `library.writer.*` — `after_accepted_edit`, `after_tie`, `after_rejected_edit`, `maybe_review`. `script_id` derived via `hashlib.sha1` of R source. No-op when `edit.pattern_id is None`. |
| `r2py/stage4/__init__.py` | `verify()` replaces `NotImplementedError` stub; thin delegation to `verifier.verify()` with `**kwargs` forwarding. |
| `tests/test_stage4.py` | 79 tests across 11 classes covering all comparators, `_compare_pair`, `DataComparator` modes, `COMPARATORS` registry, `make_score_table`, `judge_entity`, `capture_r_rng`, `wiki_update.*`, and `verify()` smoke tests. |
| `tests/test_fuzz.py` | 31 tests across 6 classes covering `ScalarGenerator`, `VectorGenerator`, `DataFrameGenerator`, `generator_from_observed`, `boundary_cases`, `_inject_input`, `_inject_py_input`, and `run_fuzz` smoke. |

**Deferred**

- `judge.py` full LLM implementation — stub only; wired to Stage 3 integration (step 5 of §13).
- Embedding upgrade for `text_similarity` — the `difflib.SequenceMatcher` stand-in is the injection point; swap to `sentence-transformers` cosine at the same call site when embedding quality matters.
- Per-entity slice verification in `decompose.py` — currently every entity inherits whole-script scores; proper per-entity slicing requires the branch/replay path (§7.5) which needs the Python candidate's per-entity source map from Stage 2.
- `wiki_update.py` `script_id` defaults to `"unknown"` when `r_source=""` — the loop (step 7 of §13) will pass the real source.

**Implementation choices**

- **`difflib.SequenceMatcher` as the embedding stand-in**: avoids any ML dependency while keeping the interface identical to what a real embedding comparator would use. All callers go through `text_similarity(a, b)` in `base.py`.
- **`value` vs `infra` failure tags**: the distinction is enforced in `_compare_pair`. A length mismatch between an R vector and a Python scalar is `infra` (serialisation/structural gap, the R→Python translation of `c(x)` vs `x`); a numeric value that is actually wrong is `value`. The `data_compare` switch only ever rescues `infra`.
- **`pass_via_fallback` verdict**: surfaced in `ComparatorResult.verdict` whenever the `auto` or `embedding` path is taken, so a human reading the report can immediately see which entities relied on the weaker signal.
- **RNG and NETWORK excluded from `COMPARATORS`**: these are capture/replay not comparison — injecting them would require modifying the candidate source, which is Stage 3's job.
- **`make_score_table` whole-script granularity**: all entities get the same scores for now. This is correct at step 4 of §13 (Stage 2 is not yet implemented); Stage 2's per-entity source map will allow splitting the Python bundle by entity.
- **`fuzz.run_fuzz` first-counterexample-per-entity**: stops at the first failing input to minimise sandbox cost, per §7.8.

**Verification**

```
python -m pytest tests/test_stage4.py -v   # 79 passed, 1 skipped (graphics/Pillow)
python -m pytest tests/test_fuzz.py -v    # 31 passed
python -m pytest tests/ -v                # 312 passed, 5 skipped

python -c "
from r2py.stage4 import verify
from r2py.types import ScriptMap
sm = ScriptMap(source='x <- 1')
report = verify(sm, 'x = 1')
print('aggregate:', report.aggregate)
print('by_effect keys:', list(report.by_effect.keys()))
"
# → aggregate: 1.0
# → by_effect keys: [<EffectClass.STDOUT: 'stdout'>, ...]
```

---

### Session 6 — Chapter 5, Step 5 (Stage 2 — Translation)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/stage2/llm.py` | `call(messages, system, *, model, max_tokens)` — Anthropic SDK client. System prompt sent with `cache_control: {"type": "ephemeral"}` so it is cached after the first entity call in a run. Exponential-backoff retry (up to 4 attempts) on `RateLimitError` / `APIConnectionError`. API key from `ANTHROPIC_API_KEY` env var; raises `RuntimeError` if absent. Model default: `claude-sonnet-4-6`. |
| `r2py/stage2/walker.py` | `topological_order(entities)` — Kahn's algorithm over `Entity.dependencies`. On cycle detection, remaining nodes appended in insertion order (graceful fallback). |
| `r2py/stage2/prompt.py` | Static `SYSTEM_PROMPT` (version-controlled, never mutated at runtime, per §5.7). `build_entity_prompt(entity, script_map, patterns, prior_translations) → list[dict]` builds a single-turn user message containing: entity metadata, R source span, Stage 1 annotations, Pattern Library guidance (formatted as guidance + evidence count), and Python snippets of already-translated dependencies. `parse_entity_response(raw)` extracts `<python>`, `<imports>`, `<effects>` XML tags; falls back to stripping fences and using the full response on parse failure. |
| `r2py/stage2/retrieval.py` | Thin wrapper: `retrieve_patterns(entity, library, no_seeds) → list[Pattern]` delegates to `library.retrieve(entity, k=3, no_seeds=no_seeds)`. No additional logic — §6.4 ranking lives in the library module. |
| `r2py/stage2/package_translator.py` | `translate_external_symbol(entity, script_map, library, cache_dir, model) → str \| None`. Cache key: `work/translated_packages/<pkg>__<symbol>.py`. Recursion guard via `_in_progress` set (avoids infinite recursion on circular package deps). Returns `None` if no source location, package is in-progress, or LLM call fails. |
| `r2py/stage2/stitch.py` | `compose(per_entity, per_entity_imports, order, script_map, model, r_path) → str`. Import hoisting: splits every snippet into import lines vs body lines, deduplicates, sorts (`import X` before `from X import Y`). Name-collision suffix: top-level assigned names that clash with an earlier entity's name are suffixed `_1`, `_2`, etc. Header comment records source R path, r2py version, model, and entity count. |
| `r2py/stage2/coherence.py` | `review(python_source, script_map, library, model) → (revised_source, list[Edit])` — §5.6 whole-program coherence pass. One LLM call over the full stitched file. System prompt constrains the LLM to only emit typed edits from the closed `EditKind` taxonomy (CamelCase values: `InsertPreamble`, `RenameVariable`, `ChangeImport`, `WrapValue`, `ReplaceCall`). Parses JSON-per-line edit objects + `<python>` block from the response. On any failure (LLM error, parse failure, empty revised source) returns `(original_source, [])` — the pass can never lower the score. |
| `r2py/stage2/translator.py` | `translate(script_map, library, *, no_seeds, model, cache_dir, run_coherence) → str`. Orchestrates: topological walk → pattern retrieval → optional package translation → prompt build → LLM call → parse → stitch → coherence. Per-entity LLM failures produce a `# r2py: translation failed for {eid}` stub comment rather than raising. |
| `r2py/stage2/__init__.py` | `translate()` stub replaced with delegation to `translator.translate()`; `library` defaults to `get_library()` when not provided. |
| `tests/test_stage2.py` | 41 tests across 8 test classes. 40 pass offline (no API key needed); 1 live smoke test skipped unless `ANTHROPIC_API_KEY` is set. |

**Deferred**

- Live API smoke test (`TestTranslateSmokeAPI`) — passes when `ANTHROPIC_API_KEY` is present; skipped in CI per §12.4 (end-to-end tests are not run on every merge).
- `package_translator.py` cache is keyed only by `<pkg>__<symbol>` (no version). A version-keyed cache (using `stage0.env.package_source` to get the installed version) is deferred to when package translation is exercised end-to-end.

**Implementation choices**

- **XML output tags** (`<python>`, `<imports>`, `<effects>`): chosen over JSON/markdown delimiters because XML tags are unambiguous even when the Python snippet itself contains curly braces or backtick fences. The `parse_entity_response` fallback (strip fences, use full response) handles LLM responses that ignore the format instruction.
- **Prompt caching on system prompt**: the `cache_control: {"type": "ephemeral"}` block is sent with the static `SYSTEM_PROMPT` on every call. Since all entity calls in one translation run share the same system prompt text, the Anthropic cache hits after the first call — reducing both latency and token cost for scripts with many entities.
- **Coherence pass uses programmatic edit applier**: `_apply_edit()` in `coherence.py` applies each typed edit to the original source string rather than using the LLM's `<python>` output block. This enforces §5.6's "may only emit typed edits — never a free rewrite" constraint at the code level, not just the prompt level. The `<python>` block in the LLM response is parsed but then discarded; only the JSON edit lines drive the mutation.
- **Coherence pass edit taxonomy uses CamelCase enum _values_** (`InsertPreamble`, not `INSERT_PREAMBLE`): the `EditKind` enum stores CamelCase string values (e.g. `EditKind.INSERT_PREAMBLE.value == "InsertPreamble"`), so the LLM prompt and JSON parsing both use those values for `EditKind(kind_str)` to work without a mapping layer.
- **`stitch.py` imports `r2py`** for `__version__` in the header comment. This is safe because `r2py/__init__.py` is already loaded by the time Stage 2 runs.

**Verification**

```
python -m pytest tests/test_stage2.py -v   # 42 passed, 1 skipped
python -m pytest tests/ -q                 # 370 passed, 6 skipped (was 312 before)

python -c "from r2py.stage2 import translate; print('ok')"
python -c "from r2py.stage2.llm import call; print('ok')"
python -c "from r2py.stage2.coherence import review; print('ok')"
```

---

### Session 7 — Chapter 8, Step 6 (Stage 3 — Editor)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/stage3/edit_types.py` | Canonical `apply_edit(source, edit) -> str` covering all 7 `EditKind` cases. `RESTRUCTURE_CONTROL_FLOW`: text replace `params["old_code"]` → `params["new_code"]`; the LLM supplies both spans. `REPLACE_LIBRARY`: whole-word name replace plus import-line swap. On bad params or any exception, returns source unchanged. Also exports `edit_to_dict` / `dict_to_edit` for JSON round-trips. |
| `r2py/stage3/history.py` | `EditHistory` dataclass — `add()`, `was_tried()`, `clear()`. Equality key is `(kind, sorted entity_ids, frozen params)`; `pattern_id` is excluded so the same mechanical edit attributed to a different pattern is still detected as duplicate state. |
| `r2py/stage3/prompt.py` | `STAGE3_SYSTEM_PROMPT` (version-controlled, never mutated at runtime). `build_edit_prompt()` includes entity metadata, score breakdown, verifier feedback, pattern guidance (exploit mode only), and last-5 tried edits. `parse_edit_response()` extracts first JSON object with a `kind` field; falls back to a regex scan for embedded `{…}`. |
| `r2py/stage3/attributor.py` | `attribute(edit, proposed_pattern_id) -> Edit` — validates that `pattern_id` is non-empty, raises `AttributionError(ValueError)` otherwise. Returns a copy of the edit with the attribution set. Implements §8.5 invariant: no unattributed edit can leave Stage 3. |
| `r2py/stage3/policy.py` | `propose(candidate, script_map, library, history, epsilon, model)` — sorts entities by ascending average sub-score, walks weakest-first. For each entity: retrieves patterns from library, chooses EXPLOIT (`random() > epsilon` and patterns exist) or EXPLORE (no patterns, or epsilon beats random). Calls `llm.call`, parses response, validates attribution, checks history. Skips to next entity on parse failure or already-tried edit. Raises `RuntimeError` if all entities exhausted. |
| `r2py/stage3/editor.py` | `propose_edit()` entry point — computes `epsilon = max(0.05, 0.30 − iter × 0.025)` (decays from 0.30 to 0.05 floor over 10 iterations) and delegates to `policy.propose()`. Re-exports `apply_edit` from `edit_types` so callers use `stage3.apply_edit`. |
| `r2py/stage3/__init__.py` | Stubs replaced. `propose_edit(candidate, library, script_map=None, history=None, iteration=0)` — `script_map` and `history` default to safe values for backward compatibility with the §4.1 pseudocode two-arg signature. `apply_edit` delegates to `edit_types.apply_edit`. |
| `tests/test_stage3.py` | 58 tests across 9 classes. All pass offline (no API key needed). |

**Deferred**

- `judge.py` full LLM wiring in Stage 4 — still a stub; wired when the loop (step 7) is built and end-to-end testing begins.
- `REPLACE_LIBRARY` and `RESTRUCTURE_CONTROL_FLOW` are text-level replacements. A smarter applier using the Python AST (e.g. `libcst`) would handle indented or reformatted code more robustly; deferred until needed.
- `epsilon` schedule is hard-coded. The optional contextual bandit (D6, §12.6 B) replaces it when `learned_policy=True`; the current schedule is the heuristic baseline it must beat.

**Implementation choices**

- **`coherence.py` left unchanged**: `coherence._apply_edit` is a private helper covering only the 5 kinds the coherence pass emits. `edit_types.apply_edit` is the canonical Stage 3 implementation covering all 7 kinds. No refactoring of `coherence.py` (per CLAUDE.md surgical-change rule).
- **`stage2.llm` reused directly**: `policy.py` imports `from ..stage2 import llm as _llm`. This is the intended reuse pattern (§11 disposition table: `stage2/llm.py` reused); no copy or wrapper created.
- **`pattern_id` from LLM response takes priority over retrieved ID**: in exploit mode, if the LLM also emits a `pattern_id` field, that value is used; the retrieved pattern's `.id` is the fallback. This lets the LLM name a new pattern even while following guidance — a deliberate over-attribution-prevention measure.
- **History key excludes `pattern_id`**: the same callable-replacement attributed to two different patterns is still the same translation state. The tabu set (§4.1) operates on state hashes; history duplicates are caught one level earlier here with a lighter key.

**Verification**

```
python -m pytest tests/test_stage3.py -v   # 58 passed
python -m pytest tests/ -q                 # 432 passed, 6 skipped (was 370 before)

python -c "from r2py.stage3 import propose_edit, apply_edit; print('ok')"
python -c "
from r2py.stage3.edit_types import apply_edit
from r2py.types import Edit, EditKind
e = Edit(kind=EditKind.INSERT_PREAMBLE, params={'code': 'import numpy as np'})
print(apply_edit('x = 1', e))
"
# → import numpy as np
#   x = 1
```

---

### Session 8 — Chapter 9, Step 7 (Top-level loop, API, CLI)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/loop.py` | `_state_hash(translation)` — SHA-256 hex of UTF-8 source text; tabu key for the visited set. `_top_k(candidates, k)` — stable descending sort (Python's `sorted` is stable, so incumbents placed earlier in the combined list beat survivors at equal scores, implementing `prefer_incumbent_on_tie`). `run_loop(script_map, library, *, max_iters, score_threshold, beam_width, use_judge, data_compare, no_seeds, **verify_kwargs)` — exact §4.1 pseudocode: seed via Stage 2, initial verify via Stage 4, then beam expansion with strict-improvement acceptance, tabu set, `EditHistory` tracking, `library.record_evidence/tie/contradiction` calls, and best-effort `epistemology.review` after the loop. |
| `r2py/__init__.py` | `translate()` stub replaced: calls `stage1.analyze`, `get_library()`, `run_loop()`, writes `py_path`, returns `TranslateResult`. `learned_retrieval` / `learned_policy` flags accepted but silently ignored (D6 optional components deferred to step 9). |
| `r2py/cli.py` | `cmd_library` list / show / review implemented (previously `NotImplementedError` since Session 1). `show` writes via `sys.stdout.buffer` in UTF-8 to handle the `→` character on Windows terminals. `train-reranker` remains `NotImplementedError` (step 9). |
| `tests/test_loop.py` | 40 tests across 11 classes covering `_state_hash`, `_top_k`, and `run_loop` invariants (seed-only, threshold halt, strict improvement, tie rejection, regression rejection, tabu set, no-proposals break, beam width, max-iters halt, pattern tracking, score history). All mock via `unittest.mock.patch` on `r2py.stage2.translate`, `r2py.stage3.propose_edit`, `r2py.stage3.apply_edit`, `r2py.stage4.verify`, `r2py.library.epistemology.review`. |

**Deferred**

- `learned_retrieval` / `learned_policy` — D6 optional components; both flags accepted in `translate()` but ignored until step 9.
- `cmd_ablation` — remains `NotImplementedError`; step 8.
- `scripts/run_ablation.py`, `scripts/train_reranker.py` — steps 8 and 9.

**Pre-existing bugs noted but not fixed (§3 surgical-change rule)**

`stage4/wiki_update.py` has two API mismatches that make its functions unusable:
`after_accepted_edit` passes `score=` instead of `score_delta=` to `library.record_evidence`;
`maybe_review` calls `library.review()` which does not exist on `PatternLibrary`.
The loop calls `library.record_evidence/tie/contradiction` directly (matching the §4.1
pseudocode and the `PatternLibrary` public interface), bypassing `wiki_update.*`.

**Verification**

```
python -m pytest tests/test_loop.py -v   # 40 passed
python -m pytest tests/ -q              # 472 passed, 6 skipped

python -c "from r2py.loop import run_loop, _state_hash, _top_k; print('ok')"
python -m r2py library list              # 15 seed patterns listed
python -m r2py library show base.seq_to_range   # shows pattern markdown
python -m r2py library review            # "Review complete: 0 action(s)."
```

---

### Session 9 — Chapter 10 + §12.4.1, Step 8 (Corpus tests + batch runner + ablation harness)

**Implemented**

| File | Notes |
|------|-------|
| `r2py/__init__.py` | Added `library=None` keyword argument to `translate()`. `None` defaults to `get_library()`. Injection point for `_FrozenLibrary` in the ablation harness (and any other caller that needs to supply a custom library). |
| `r2py/batch.py` | `translate_batch(input_dir, output_dir, *, recursive, max_iters, …, force)` — discovers `.R` files, calls `translate()` per script, handles errors gracefully (one failure does not abort the batch), appends to `work/analysis/learning_curve.csv` (one row per run: timestamp, script_id, final_score, iterations, evidence_added, contradictions_added), upserts `work/analysis/scoring_table.csv` (latest score per script). `force=True` re-translates scripts that already have an output directory. |
| `r2py/ablation.py` | `run_ablation(slice_path, compare, output_dir, *, max_iters, seed, beam_width)` — reads the pinned slice manifest, runs two paired passes (A then B), computes per-script `delta = B − A`, runs a significance test (Wilcoxon signed-rank via scipy if available; sign test via stdlib `math.erfc` otherwise), writes `per_script.csv` and `summary.json` to `work/analysis/ablation/<ts>/`. `_FrozenLibrary` wrapper proxies all `PatternLibrary` reads but silences `record_evidence`, `record_tie`, `record_contradiction` — the mechanism for "library frozen" in run A. `compare="heuristic-vs-learned"` gates D6 by passing `learned_retrieval=True` in run B. |
| `scripts/translate_batch.py` | Thin CLI wrapper over `r2py.batch.translate_batch`; replaces the docstring-only stub. Accepts `--input-dir`, `--output-dir`, `--max-iters`, `--score-threshold`, `--beam-width`, `--no-seeds`, `--data-compare`, `--force`, `--no-recursive`. |
| `scripts/run_ablation.py` | Thin CLI wrapper over `r2py.ablation.run_ablation`; replaces the docstring-only stub. Accepts `--slice`, `--compare`, `--output-dir`, `--max-iters`, `--seed`, `--beam-width`. |
| `r2py/cli.py` | `cmd_ablation` wired to `r2py.ablation.run_ablation`; replaces `NotImplementedError`. Prints `n=…  mean_delta=…  p=… (test)  regressions=…` summary line. |
| `work/inputs/ablation_slice.txt` | Committed pinned slice manifest. Seeded with `tests/fixtures/simple.R`. Format: one path per line relative to the project root; blank lines and `#`-prefixed comments ignored. Extend this file when new curated scripts are available. |
| `tests/test_batch.py` | 38 tests across 6 classes. All pass without API key or Rscript. Covers: `_FrozenLibrary` (read proxy, write no-ops), `translate_batch` (discovery, CSV output, error resilience, skip/force), `run_ablation` (summary keys, deltas, regressions, CSV/JSON outputs, frozen-library invariant, heuristic-vs-learned flag propagation, slice parsing), `_significance` (all branches: wilcoxon/sign-test fallback, edge cases). |
| `tests/test_e2e.py` | End-to-end tests gated behind `R2PY_E2E=1` and `ANTHROPIC_API_KEY`. Not collected by CI. Covers `translate()` on the fixture (valid Python output, score in [0,1], score history populated), `analyze()`, and `translate_batch()` on the fixture. Skipped (not failed) when env vars absent. |

**Deferred**

- `scripts/train_reranker.py` — step 9 (D6 optional components; §12.6 A).
- Learned edit policy (`scripts/train_policy.py`, §12.6 B) — step 9.
- Per-iteration sandbox artifact writing (`work/outputs/<run>/score_report.{iter}.json`, etc. from §12.3) — the batch runner writes only the high-level CSV metrics today; the detailed per-iteration observability files require hooking into `loop.py` to emit them during the loop. Deferred to a future session.

**Implementation choices**

- `_FrozenLibrary` is defined in `r2py/ablation.py` (not in `r2py/library/`) because it exists solely for the ablation use case — adding it to the library module would couple a test harness concern into production code.
- `get_library` is imported at the module level in `ablation.py` (not lazily inside `run_ablation`) so that `unittest.mock.patch("r2py.ablation.get_library")` can intercept it in tests. `r2py.translate` is accessed via `import r2py as _r2py; _r2py.translate(...)` so `patch("r2py.translate")` works correctly (the attribute lookup happens at call time, not import time).
- `translate_batch` skips scripts whose output directory already exists (without `force=True`) to make repeated runs cheap on a partially-translated corpus.
- Significance test prefers Wilcoxon signed-rank over a paired t-test because the score distribution is bounded [0,1] and may not be normally distributed; the fallback sign test requires only `math.erfc` (stdlib), so scipy is fully optional.

**Verification**

```
python -m pytest tests/test_batch.py -v   # 38 passed
python -m pytest tests/ -q               # 511 passed, 11 skipped (was 472+6 before)

python -c "from r2py.batch import translate_batch; print('ok')"
python -c "from r2py.ablation import run_ablation, _FrozenLibrary; print('ok')"
python -m r2py ablation --help            # no NotImplementedError
python scripts/translate_batch.py --help  # shows all flags
python scripts/run_ablation.py --help     # shows all flags
```

---

### Session 10 — Step 9: Optional learned components (D6, §12.6)

**Scope**: Complete step 9 of the implementation order: data logging infrastructure,
`scripts/train_reranker.py` (LambdaMART), `scripts/train_policy.py` (LinUCB contextual bandit),
wiring of `learned_retrieval=True` / `learned_policy=True`, and tests.

**Pre-session bugs noted (not fixed — §3 surgical-change rule)**

- None discovered.

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/types.py` | Added `RetrievalEpisodeCandidate`, `RetrievalEpisode`, `PolicyTransition`, `EpisodeCollector` dataclasses for D6 data logging. |
| `r2py/stage3/policy.py` | Added `_collector: object = None` parameter; appends `RetrievalEpisode` to the collector (via `_make_episode()`) when patterns are retrieved. Added bandit hint: reads `library._bandit_model` via `isinstance(model, BanditModel)` guard; passes `preferred_edit_kind` to `build_edit_prompt()`. |
| `r2py/stage3/editor.py` | Threads `_collector` to `policy.propose()`. |
| `r2py/stage3/__init__.py` | Threads `_collector` to `editor.propose_edit()`. |
| `r2py/stage3/prompt.py` | Added `preferred_edit_kind: str \| None = None` to `build_edit_prompt()`; appends a bandit-hint section to the prompt when set. |
| `r2py/loop.py` | Added `learned_retrieval`, `learned_policy`, `output_dir` parameters. Sets them on the library via `_set_attr()`. Passes `EpisodeCollector` to each `propose_edit()` call; builds `PolicyTransition` directly from proposal data; stamps outcomes after verification. Calls `_write_run_logs()` at end when `output_dir` is set. |
| `r2py/__init__.py` | Forwarded `learned_retrieval`, `learned_policy`, `output_dir` to `run_loop()`. Removed "ignored until step 9" comments. |
| `r2py/batch.py` | Passes `output_dir=run_dir` to `_translate()` so per-run logs are written alongside output.py. |
| `r2py/library/__init__.py` | Added `learned_retrieval`, `learned_policy`, `_reranker_model`, `_bandit_model`, `_models_loaded` attributes to `PatternLibrary`. Added `_ensure_models_loaded()` for lazy model loading. `retrieve()` calls `reranker.rerank()` when `learned_retrieval=True` and a model is loaded. |
| `r2py/library/reranker.py` | **New.** Feature extraction (8 features per §12.6 A), `rerank()`, `save_model()`, `load_model()`, and `train()` entry point (LambdaMART via LightGBM). Feature extraction is pure Python (no LightGBM import) for testability. `train()` guards on data threshold, runs grouped k-fold CV, compares vs heuristic baseline NDCG@3, saves only on a win. |
| `r2py/library/bandit.py` | **New.** `BanditModel` dataclass, `extract_context()` (8-feature vector), `ucb_score()`, `choose_action()`, `update_arm()`, `save_model()`, `load_model()`, and `train()` entry point (offline LinUCB via IPS). Pure Python + stdlib; no numpy/scipy dependency. |
| `scripts/train_reranker.py` | Replaced stub with thin argparse CLI wrapper around `reranker.train()`. |
| `scripts/train_policy.py` | **New.** Thin argparse CLI wrapper around `bandit.train()`. |
| `r2py/cli.py` | Implemented `train-reranker` command in `cmd_library()`: calls `reranker.train()` and returns its exit code. |
| `tests/test_reranker.py` | **New.** 15 tests: feature vector shape/values, `rerank()` with None model, with mock model, with failing model; `save_model()`/`load_model()` round-trip (LightGBM-gated); data-threshold refusal. |
| `tests/test_bandit.py` | **New.** 13 tests: context vector shape, UCB scoring, arm selection, LinUCB `_solve()` correctness, `save_model()`/`load_model()` round-trip, data-threshold refusal. |
| `tests/test_loop_logging.py` | **New.** 9 tests: `edits.log.jsonl` and `library_diff.json` written/absent on output_dir presence; outcome stamping (accepted/rejected/tie); `RetrievalEpisode` round-trip via fake `_collector`. |

**Deferred**

- Online bandit update (weight adjustment from live feedback in the loop) — architecture requires offline-only training (D6).
- Neural cross-encoder reranker upgrade path (§12.6 A explicitly defers this as data-hungry and opaque).
- Per-iteration score_report JSON artifacts (§12.3 `score_report.{iter}.json`, `effect_bundle.py.{iter}.json`) — loop writes only `edits.log.jsonl` and `library_diff.json` today; full iteration artifacts require deeper loop refactor.
- `r2py library train-policy` CLI subcommand — implemented post-session alongside `train-reranker`.

**Implementation choices**

- `_collector: object = None` side-channel (rather than changing the return type of `propose_edit()`) keeps all existing call sites unmodified — the 58 stage3 tests pass unchanged.
- `isinstance(bandit_model, BanditModel)` guard instead of `bandit_model is not None` avoids MagicMock auto-attribute truthy false-positives in tests.
- `learned_retrieval` / `learned_policy` stored as `PatternLibrary` instance attributes (set by `run_loop()` via `_set_attr()`) rather than threaded as parameters through the stage3 call chain — keeps `policy.propose()` signature stable and the mock interface clean.
- LightGBM is a soft dependency: `reranker.py` guards all LGB imports inside `train()` and `save_model()`; `extract_features()`, `rerank()`, `load_model()` are all pure Python and always importable.
- `bandit.py` implements Gaussian elimination in pure Python (`_solve()`) to avoid any numpy dependency — the bandit feature vector is only 8-dimensional so the cost is negligible.
- IPS weights are clipped at 10× (`min(1/propensity, 10)`) to prevent extreme importance-weights from dominating the offline update on rare arms.
- `PolicyTransition` records are built directly in `loop.py` from data already available (parent `EntityScore`, `edit.kind`, verification outcome) without any stage3 hook — bandit training data collection requires no interface change to stage3.

**Verification**

```
python -m pytest tests/test_reranker.py tests/test_bandit.py tests/test_loop_logging.py -v
# 37 passed, 1 skipped (lgb-gated save/load test)

python -m pytest tests/ -q
# 551 passed, 12 skipped (was 511+11 before session 10)

python -c "from r2py.library.reranker import extract_features, rerank; print('ok')"
python -c "from r2py.library.bandit import BanditModel, choose_action; print('ok')"

python -m r2py library train-reranker --help  # no NotImplementedError
python scripts/train_reranker.py --help       # shows all flags
python scripts/train_policy.py --help         # shows all flags

python -c "
import inspect, r2py
sig = inspect.signature(r2py.translate)
assert 'learned_retrieval' in sig.parameters
assert 'learned_policy' in sig.parameters
assert 'output_dir' in sig.parameters
from r2py.loop import run_loop
sig2 = inspect.signature(run_loop)
assert 'learned_retrieval' in sig2.parameters and 'output_dir' in sig2.parameters
print('flags wired ok')
"
```

---

### Session 12 — Loop stability fixes + crash attribution (withr debugging)

**Scope**: Diagnose and fix the translation loop stalling on `withr__rd_example__with_locale_Rd.R`
(score 0.212, loop cycling on the same entity for all 8 iterations). Two root causes were found
and fixed; a third improvement (crash attribution) was added to give partial credit to entities
that executed cleanly before a crash.

**Root cause 1 — Loop cycling when all entities score identically**

When Python crashes, all entity `_avg_score` values are identical (~0.2) because no DATA is
captured. Python's stable sort preserves insertion order, so `_weak_first()` always returned the
first entity, and Stage 3 cycled on it for all 8 iterations. Three fixes:

1. `_weak_first()` now breaks score ties by preferring `FUNCTION_CALL` / `FUNCTION_DEF` /
   `EXTERNAL_SYMBOL` entities over `LIBRARY_IMPORT` / `VARIABLE` / `CONSTANT`. Callable entities
   are more likely to be causing crashes and profit more from editing.
2. Per-entity attempt cap of 3 (`_MAX_ATTEMPTS_PER_ENTITY`). After 3 failed edits on any entity
   (`history.count_for_entity(eid) >= 3`), that entity is skipped.
3. Entity-targeting redirect: if the LLM's returned `edit.entity_ids` doesn't contain the intended
   target `eid`, the edit is redirected (not silently dropped) — `entity_ids` is overwritten to
   `[eid]` while preserving `kind`, `params`, and `pattern_id`.

Additionally, `loop.py` now tracks `exhausted_parents: set[str]` — when Stage 3 raises
`RuntimeError` for a beam member (all entities exhausted), that member is added to the set and
filtered from `active_beam` in future iterations rather than being re-tried and stalling.

**Root cause 2 — Translation crash on Windows locale**

`withr::with_locale` uses POSIX locale strings (`"it_IT"`, `"es_ES"`, `"fr_FR"`) which
`locale.setlocale()` rejects on Windows. The crash caused `executed_ok=False` for all entities,
zeroing their scores. Three fixes:

1. `stage4/verifier.py` now surfaces `py_bundle.stderr` crash traceback as `FeedbackItem` entries
   (effect class `SYNTAX`) attributed to all entities. Stage 3 can now see what line crashed and
   act on it — previously the loop had no feedback distinguishing a locale crash from any other failure.
2. `work/library/withr.with_locale.md` — new Pattern Library entry documenting the Windows locale
   name mapping (`"es_ES"` → `"Spanish_Spain.1252"`, etc.), the `try/except locale.Error` wrapper
   requirement, and the restore-in-finally semantics.
3. `stage1/walker.py` — added `_PLATFORM_SPECIFIC_FUNCTIONS` frozenset covering locale/OS-specific
   R functions (`Sys.setlocale`, `with_locale`, `with_envvar`, etc.). The `_annotate_r_semantics`
   pass now flags enclosing entities with `platform_specific` so Stage 2 knows to apply Windows-safe
   translation patterns.

**Idea C — Crash attribution with preamble offset (partial credit for pre-crash entities)**

When Python crashes mid-script, all entities were previously scored `executed_ok=False`. Entities
whose code ran cleanly before the crash (e.g. `library()` imports, variable assignments) were
unfairly penalised. Fix: parse the crash line number from the traceback, subtract the sandbox
preamble offset, and give pre-crash entities `executed_ok=True` partial credit.

This required:
- `EffectBundle.preamble_lines: int = 0` — the number of lines before `source` in
  `_r2py_script.py`. Computed as `before_source.count("\n")` in `PySandbox.run()`.
- `bundle.py` `to_json`/`from_json` updated for the new field.
- `decompose.py` `_parse_crash_line(stderr)` extracts the last `File "_r2py_script.py", line N`
  match from the traceback. `_attribute_crash(crash_file_line, preamble_lines, entity_line_map)`
  converts to source-space (`source_line = crash_file_line − preamble_lines`, 1-indexed to match
  `entity_line_map`'s 1-based convention from `stitch.compose()`), then classifies entities as
  pre-crash, crashing, or post-crash. `make_score_table()` uses per-entity `entity_executed_ok`
  instead of the global `executed_ok`.

**Also fixed (pre-session)**

- `stage2/prompt.py` `_strip_fences()` now requires the `python` language label on code fences
  (```` ```python ````). Previously a generic fence or R code fence could be mistakenly extracted
  as the Python snippet.
- `stage4/verifier.py` `_build_feedback()` now attributes failures to ALL entities (not just the
  first). Previously only the first entity received feedback, causing Stage 3 to always see
  feedback about `suppressPackageStartupMessages` regardless of which entity it was editing.
- `stage1/walker.py` — fixed `_visit_assignment` to handle `elif rhs.kind == "call":` correctly,
  and fixed `argument` node unwrapping in `_visit_call`. Entity count reduced from ~30 to 11 for
  the test script.

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/types.py` | Added `preamble_lines: int = 0` to `EffectBundle` (for crash attribution). |
| `r2py/stage0/effects/bundle.py` | Updated `to_json`/`from_json` for `preamble_lines`. |
| `r2py/stage0/sandbox/py_sandbox.py` | Computes `_preamble_lines = before_source.count("\n")` before assembling `full_script`; stores in `bundle.preamble_lines`. |
| `r2py/stage2/prompt.py` | `_strip_fences()` now requires `python` label: `r"```python\n(.*?)```"`. |
| `r2py/stage3/history.py` | Added `count_for_entity(entity_id) -> int` method. |
| `r2py/stage3/policy.py` | `_weak_first()` tie-break (callable > import/constant). Per-entity cap of 3 via `count_for_entity`. Entity-targeting changed from silent reject (`continue`) to redirect (`entity_ids=[eid]`). |
| `r2py/stage3/prompt.py` | `STAGE3_SYSTEM_PROMPT` Rules section: added `"entity_ids" MUST contain the ID shown after "## Target entity:"`. |
| `r2py/stage4/verifier.py` | `_build_feedback()` attributes to ALL entities (was: first only). `verify()` surfaces crash traceback as `FeedbackItem(effect_class=SYNTAX)` for all entities when `exit_code != 0`. Passes `py_stderr` and `preamble_lines` to `make_score_table()`. |
| `r2py/stage4/decompose.py` | New `_parse_crash_line(stderr)` and `_attribute_crash(crash_file_line, preamble_lines, entity_line_map)` helpers. `make_score_table()` adds `py_stderr: str = ""` and `preamble_lines: int = 0` parameters; computes `pre_crash_eids`; uses per-entity `entity_executed_ok` instead of global `executed_ok`. |
| `r2py/stage1/walker.py` | Fixed `_visit_assignment` call detection. Added `_PLATFORM_SPECIFIC_FUNCTIONS` frozenset; `_annotate_r_semantics` flags enclosing entities with `platform_specific`. |
| `r2py/loop.py` | Added `exhausted_parents: set[str]`; filters `active_beam` at the start of each iteration; adds to set on `RuntimeError` from `propose_edit`. Changed `for parent in beam` → `for parent in active_beam`. |
| `work/library/withr.with_locale.md` | **New.** Pattern Library entry: Windows locale name mapping table, `try/except locale.Error` wrapper, restore-in-finally pattern, translation recipe. |

**Deferred**

- Per-entity data scores for pre-crash entities: `global_data_score` remains 0.0 even for
  pre-crash entities (Python crashed before the DATA epilogue ran, so no variables were captured).
  Only `executed_ok`-derived scores (`type_match` for `LIBRARY_IMPORT`, `control_flow_match` for
  `VARIABLE`) benefit from the partial credit. A per-entity sandbox re-run of the pre-crash slice
  would give true data scores but is expensive; deferred.
- Windows locale mapping table in `withr.with_locale.md` covers only 6 locales. A comprehensive
  mapping (all POSIX → Windows locale names) would need to be generated from Windows locale data.

**Implementation choices**

- **Redirect not reject for entity-targeting**: when the LLM targets the wrong entity, we preserve
  its proposed `kind` and `params` and only overwrite `entity_ids`. The LLM's mechanical edit is
  usually correct; only the attribution is wrong. Rejecting silently wastes the LLM call and wastes
  one of the 3 per-entity attempts.
- **`exhausted_parents` keyed by state hash**: consistent with the tabu set and history dict. A
  parent that produces a new candidate via an accepted edit gets a new state hash, so it won't be
  in `exhausted_parents` — only stale parents that never produce improvement are filtered.
- **Crash attribution uses `entity_line_map` 1-indexed convention**: `stitch.compose()` and
  `rebuild_entity_line_map()` both use 1-indexed line numbers (matching `SyntaxError.lineno`).
  `_attribute_crash` converts with `source_crash_line = crash_file_line − preamble_lines` (no
  additional −1 needed) to stay in the same coordinate space.
- **`_parse_crash_line` takes the LAST match**: a traceback may list multiple frames in
  `_r2py_script.py` (e.g. a function defined in the script calling another). The last `line N`
  reference is the innermost frame — the actual crash site.
- **`platform_specific` annotation is additive**: like all §3.7 flags, it is attached to any
  entity whose source span contains a platform-specific call, including enclosing `FUNCTION_DEF`
  entities. Stage 2 can then use it as a hint to apply Windows-safe patterns.

**Verification**

```
python -c "import r2py.types, r2py.stage0.effects.bundle, r2py.stage0.sandbox.py_sandbox, r2py.stage3.prompt, r2py.stage3.policy, r2py.stage1.walker, r2py.stage4.verifier, r2py.stage4.decompose, r2py.loop; print('All imports OK')"
# → All imports OK

python -c "
from r2py.types import EffectBundle
print(EffectBundle().preamble_lines)
# → 0

from r2py.stage4.decompose import _parse_crash_line, _attribute_crash
stderr = 'File \"_r2py_script.py\", line 12, in <module>\nlocale.Error: unsupported locale setting'
print(_parse_crash_line(stderr))
# → 12
crashing, pre = _attribute_crash(12, 5, {'A': (1, 3), 'B': (5, 8), 'C': (10, 12)})
print(crashing, pre)
# → B {'A'}
"
```

### Session 11 — Architecture gap closure (9 deferred items)

**Scope**: Close all 9 deferred items identified in a post-Session-10 gap audit. Items
are described in the plan file `~/.claude/plans/make-a-comprehensive-plan-dynamic-wilkes.md`.
No new features; pure compliance pass against the spec.

**Pre-session bugs noted and fixed**

A code review (3-angle, 1-vote verify) was run on the session diff. All 6 candidates
reported as CONFIRMED were already addressed in the implementation — the verification
agents hallucinated confirmation of patterns that did not match the actual code. No
post-session fixes were required. 564 tests pass, 12 skipped.

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/stage4/wiki_update.py` | Fixed 4 dead call sites: `score=` → `score_delta=` in `record_evidence`; removed invalid `score=` kwarg from `record_tie`; `score=0.0` → `observed=0.0` in `record_contradiction`; `library.review()` → `library.epistemology_review()`. |
| `r2py/library/__init__.py` | Added `epistemology_review()` method (thin wrapper around `epistemology.review()`). Added `ast_shape_hash: str = ""` parameter to `record_evidence()`; threads it to `_writer.record_evidence()`. |
| `r2py/library/writer.py` | Added `ast_shape_hash: str = ""` parameter to `record_evidence()` and `_upsert_index()`; passes hash to `index.upsert_meta()` so exact-shape index keys are populated. |
| `r2py/loop.py` | Added `from .library.retrieval import entity_ast_shape_hash as _shape_hash`; computes shape hash for the target entity and passes it to `record_evidence()` on accepted edits. Unpacks `(seed, entity_line_map)` from `stage2.translate()`; passes `entity_line_map` to seed verify, `{}` to iteration verifies. Added `_report_idx` monotonic counter (initialized to 1 outside the iteration loop) for collision-free score_report artifact names. Added `_write_score_report()` (calls `_score_report_to_dict()`) writing `score_report.{N}.json` to `output_dir` for each verify call when `output_dir` is set. |
| `r2py/stage0/effects/network.py` | **New.** R preamble: installs `trace()` wrappers on `httr::GET/POST/PUT/DELETE/PATCH` and `curl::curl_fetch_memory`; each logs `(verb, url, sha1(response_body))` to `.r2py_net_log` in GlobalEnv via explicit `get()`/`assign()`. R epilogue: serialises log to `_r2py_network.json` via `jsonlite`. Python preamble: monkey-patches `requests.Session.request` and `urllib.request.urlopen`; logs to `_r2py_net_log` module list. Python epilogue: writes `_r2py_network.json`. `collect()` reads JSON → `{"network_log": [...]}`. |
| `r2py/stage0/sandbox/r_sandbox.py` | Added `from ..effects import network as _network_effects`; appends R preamble/epilogue and collects `network_log` into `EffectBundle` when `EffectClass.NETWORK` is in `capture`. |
| `r2py/stage0/sandbox/py_sandbox.py` | Same as above for the Python sandbox. |
| `r2py/stage1/runner.py` | Extended `_py_to_r()`: dicts convert to R `list(key=val)` with backtick-quoting for keys that fail `_R_IDENT_RE = re.compile(r"^[a-zA-Z.][a-zA-Z0-9._]*$")`; pandas DataFrames serialise via `jsonlite::fromJSON('{json}')` with proper backslash/backtick escaping. `ImportError` on pandas is silently caught. |
| `r2py/stage1/branch_extractor.py` | Added `extract_for_branch(node, parent_entities, parent_bundle)`: extracts `variable`/`sequence`/`body` fields from a tree-sitter `for_statement`; looks up the sequence in `parent_bundle.data`, uses first element (or `"1"` fallback); restores free variables (excluding the loop var) as a preamble; returns `for (<var> in <value>) <body>` or `None` if no body node. |
| `r2py/stage1/__init__.py` | Updated `_collect_branch_nodes_rec()`: `for_statement` nodes produce `for_branch_N` entries (passed to `extract_for_branch`); `while_statement` bodies produce `while_branch_N` entries marked `was_executed=True` (skipped, per TODO comment). Updated `_extract_branches()` to dispatch `for_statement` nodes to `extract_for_branch` and treat `None` return as unreachable. |
| `r2py/stage4/judge.py` | Replaced stub with real LLM call via `stage2.llm.call()`. Three-way verdict: `elif "<verdict>fail</verdict>"` in `raw_lower`; `else` returns `verdict="uncomparable"` when no tag found (safe sentinel for malformed/truncated responses). Tag stripping uses `re.sub(r"<verdict>(?:pass|fail)</verdict>", "", raw, flags=re.IGNORECASE)` — case-insensitive, covering all capitalisation variants. Explanation truncated to 300 chars. |
| `r2py/stage4/comparators/base.py` | Added `_difflib_similarity()`, `_get_embed_model()` (lazy singleton for `all-MiniLM-L6-v2`), `_embedding_similarity()` (falls back to difflib on error). `text_similarity()` uses the embedding backend when `R2PY_EMBED=1` env var is set; otherwise uses difflib. |
| `r2py/stage4/comparators/data.py` | `DataComparator.compare()` now populates `per_variable: dict[str, float]` for each variable scored; included in the returned `ComparatorResult`. |
| `r2py/types.py` | Added `per_variable: dict[str, float] = field(default_factory=dict)` to `ComparatorResult`. |
| `r2py/stage2/stitch.py` | `compose()` return type changed to `tuple[str, dict[str, tuple[int, int]]]`. Tracks per-entity line ranges as the source is assembled; separator increments use `+= 1` (one blank line per `"\n\n"` join separator). |
| `r2py/stage2/translator.py` | `translate()` return type changed to `tuple[str, dict[str, tuple[int, int]]]`; unpacks `entity_line_map` from `stitch.compose()`; invalidates map (sets to `{}`) when coherence pass modifies the source. |
| `r2py/stage2/__init__.py` | Public `translate()` return type updated to `tuple[str, dict]`; accepts and forwards `**kwargs`. |
| `r2py/stage4/decompose.py` | `make_score_table()` accepts `entity_line_map: dict | None = None`; for each entity looks up `entity.name` in `data_result.per_variable` for a per-variable data score, falling back to the global aggregate. |
| `r2py/stage4/verifier.py` | `verify()` accepts `entity_line_map: dict | None = None`; threads it to `make_score_table()`. |
| `pyproject.toml` | Added `embed = ["sentence-transformers>=2.2"]` to `[project.optional-dependencies]`. |
| `tests/fixtures/with_for_loop.R` | **New.** Minimal R fixture with a `for` loop used by stage1 branch-extraction tests. |
| `tests/test_stage4.py` | Updated `_FakeLibrary` to match corrected API signatures (`score_delta=`, `observed=`, `epistemology_review()`). Replaced stub judge test with 3 mocked-LLM tests covering pass/fail/no-tag paths. |
| `tests/test_stage2.py` | Updated `TestCompose` and `TestTranslateOrchestration` to unpack `(source, line_map)` tuples from `compose()` and `translate()`. |
| `tests/test_loop.py` | All `patch(_S2, return_value="seed")` / `"x = 1"` mocks updated to return `("seed", {})` / `("x = 1", {})` tuples. |
| `tests/test_loop_logging.py` | Same mock update. |
| `tests/test_stage1.py` | Added tests for `_py_to_r` dict/DataFrame cases; added tests for `extract_for_branch` and `_collect_branch_nodes_rec`. |
| `tests/test_stage0_effects.py` | Added 4 network capture tests (collect, empty, invalid JSON, urllib preamble). |

**Deferred**

- `entity_line_map` for iteration verifies: after `apply_edit` shifts lines the map is stale; iteration verifies pass `entity_line_map={}` so `decompose` falls back to whole-script scores for beam-search candidates. Rebuilding the map after each edit requires a lightweight re-stitch; deferred (TODO comment in `loop.py`).
- `while_statement` branch extraction: bodies have no natural synthetic iterator; requires solver-driven pre-condition synthesis. Marked unreachable with a TODO comment in `stage1/__init__.py`.
- `effect_bundle.py.{iter}.json` per-iteration artifacts (§12.3): writing these requires `verify()` to return the `EffectBundle` alongside `ScoreReport` — a larger return-type change. Deferred; TODO comment in `verifier.py`.
- `entity_line_map` rebuild after coherence pass: coherence rewrites shift all line numbers; current implementation invalidates the map. A proper rebuild would re-parse the revised source; deferred (TODO in `translator.py`).

**Implementation choices**

- **Network GlobalEnv strategy**: The R preamble initialises `.r2py_net_log` in GlobalEnv (outside `local()`). The logging closure explicitly calls `get(".r2py_net_log", envir = .GlobalEnv)` and `assign(".r2py_net_log", ..., envir = .GlobalEnv)` rather than `<<-`, so the epilogue (also outside `local()`) reads the correct live log.
- **Backtick-quoting for R names**: `_py_to_r()` checks keys with `_R_IDENT_RE = re.compile(r"^[a-zA-Z.][a-zA-Z0-9._]*$")`; non-matching keys (hyphens, leading digits, etc.) are wrapped in backticks with internal backticks/backslashes escaped — producing valid R named-list syntax for any key.
- **`_report_idx` monotonic counter**: initialized to 1 outside the outer `for i` loop so it never resets across iterations, avoiding filename collisions when `beam_width > 1` produces multiple proposals per iteration.
- **Judge no-verdict fallback**: When the LLM returns a response with neither `<verdict>pass</verdict>` nor `<verdict>fail</verdict>` (blank, truncated, or refusal), the judge returns `verdict="uncomparable"` rather than silently treating the absence of "pass" as a confirmed failure. This matches the pre-stub invariant.
- **`per_variable` in `ComparatorResult`**: populated only by `DataComparator`; all other comparators leave it as the default empty dict. `decompose.make_score_table()` looks up `entity.name` in it, so entities whose Python variable name matches their R name get a per-variable score rather than the whole-script aggregate.
- **`stage2.translate()` return type**: changed to `tuple[str, dict]` in a single pass covering `stitch.compose()` → `translator.translate()` → `stage2.__init__.translate()`. All 48 affected test callsites updated to unpack the tuple.

**Verification**

```
python -m pytest tests/ -q
# 564 passed, 12 skipped (was 551+12 before session 11)

# wiki_update smoke
python -c "
from r2py.stage4.wiki_update import after_accepted_edit
from r2py.types import Edit, EditKind
from r2py.library import get_library
lib = get_library()
e = Edit(kind=EditKind.REPLACE_CALL, entity_ids=[], params={}, pattern_id='base.seq_to_range')
after_accepted_edit(e, 0.1, lib, r_source='x <- 1')
print('wiki_update ok')
"

# score_report artifact smoke
python -c "
import tempfile, json
from pathlib import Path
from unittest.mock import patch, MagicMock
from r2py.loop import run_loop
from r2py.types import ScoreReport, ScriptMap
sm = ScriptMap(source='x <- 1')
lib = MagicMock(); lib.store = MagicMock(); lib.index = MagicMock()
with tempfile.TemporaryDirectory() as d:
    with patch('r2py.stage2.translate', return_value=('x = 1', {})), \
         patch('r2py.stage4.verify', return_value=ScoreReport(aggregate=0.9)), \
         patch('r2py.library.epistemology.review', return_value=[]):
        run_loop(sm, lib, max_iters=0, output_dir=d)
    sr = json.loads((Path(d) / 'score_report.0.json').read_text())
    assert sr['aggregate'] == 0.9 and 'by_entity' in sr
    print('score_report ok')
"

# embedding smoke (requires sentence-transformers)
# R2PY_EMBED=1 python -c "
# from r2py.stage4.comparators.base import text_similarity
# assert text_similarity('hello', 'hello') == 1.0
# print('embed ok')
# "
```

### Session 12 — Automated translate run: retrieval fix + crash-targeting fix

**Scope**: Scheduled automated run. translate.py failed with `ModuleNotFoundError: No module named 'r2py.library'`
and three diagnostic bugs were found and fixed. Translation of `withr__rd_example__with_locale_Rd.R` reached
**score 1.000** in 2 iterations (was 0.167 → crashed in prior sessions).

**Root causes diagnosed**

1. **`scripts/translate.py` sys.path bug**: Running a script from a subdirectory makes Python add
   `scripts/` to sys.path, not the project root. The old `r2py` (v0.1) at `C:\Users\bened\Desktop\r2py`
   was found first. Fix: prepend `Path(__file__).parent.parent` to sys.path.

2. **`withr.with_locale` pattern in wrong directory**: The best locale-handling pattern was saved to
   `work/library/withr.with_locale.md` but `PatternStore` reads from `work/library/patterns/*.md` only.
   The pattern was never loaded. Fix: created `work/library/patterns/withr.with_locale.md` (proper
   front-matter format with `seed: false`) and rebuilt the index.

3. **Pattern not retrieved — package mismatch**: `with_locale` entities have `entity.package = None`
   (FunctionCall without `::` notation). Retrieval uses `entity.package == pat.package` for tier-0.
   The pattern had `package: withr` (tier 1), while 34+ auto-created patterns had `package:` (tier 0)
   and always blocked it. Fix: changed pattern's `package:` to empty string.

4. **`_token_overlap` splits only on whitespace**: Pattern IDs and entity names use underscores and dots,
   so `_token_overlap("with_locale", "withr.with_locale")` returned 0. Other unrelated patterns ranked
   equally (all 0) and came first alphabetically. Fix: changed `_token_overlap` to split on
   `[\s._\-]+` so "with_locale" → {"with","locale"} matches "withr.with_locale" → {"withr","with","locale"}
   with Jaccard 2/3 — high enough to rank the pattern first.

5. **Stage 3 always targeting `suppressPackageStartupMessages` on crash**: When the Python translation
   crashes, ALL entities have `executed_ok=False` except pre-crash ones. But `_avg_score` used
   `data_output + variable_output + side_effects` and didn't include `executed_ok`. Pre-crash entities
   (which ran fine) got the same score as the crashing entity, so the alphabetically-first entity
   (SMM) was always targeted. Fix: applied a `-0.1` penalty in `_avg_score` when `executed_ok=False`,
   so crashing/post-crash entities rank below pre-crash entities and Stage 3 targets the right entity.

6. **R package in Python imports**: Stage 2 was generating `import withr` because the SYSTEM_PROMPT
   didn't warn against it. Fix: added explicit rule: "R package names are NOT Python modules — never
   add `import withr` or similar."

**Files added/modified**

| File | Change |
|------|--------|
| `scripts/translate.py` | Added `sys.path.insert(0, str(Path(__file__).parent.parent))` at top. Replaced Unicode `→` with ASCII `->` in progress print (Windows cp1252 encoding). |
| `work/library/patterns/withr.with_locale.md` | **New.** Confirmed-confidence pattern with detailed guidance: `_LOCALE_MAP` dict for POSIX→Windows locale names, `_with_locale()` helper definition, rules for `try/except locale.Error` and lambda-wrapping of code expressions. |
| `r2py/library/retrieval.py` | `_token_overlap()`: changed tokeniser from `str.split()` (whitespace only) to `re.split(r"[\s._\-]+")` (also splits on `_`, `.`, `-`). Makes underscore/dot-named patterns and entity names properly comparable. |
| `r2py/stage2/prompt.py` | Added rule 5b to SYSTEM_PROMPT: "R package names are NOT Python modules — never add `import withr` or similar." |
| `r2py/stage3/policy.py` | `_avg_score()`: applied `max(0.0, base - 0.1)` penalty when `es.executed_ok is False`. Crashing and post-crash entities now rank below pre-crash entities, directing Stage 3 to the actual crash location. |

**Implementation choices**

- **Package field empty for cross-package patterns**: Patterns whose guidance applies to any
  package-less call should use `package:` (empty). The retrieval tier-0 vs tier-1 split means
  package-less patterns are always candidates for package-less entities. The new `_token_overlap`
  then correctly ranks them by name similarity.
- **`-0.1` penalty for `executed_ok=False`**: Chosen to be large enough to consistently sort
  crashed entities below pre-crash ones (typical `_avg_score` ≈ 0.2 for side-effects; -0.1 gives
  crashed entities ≈ 0.1 vs pre-crash ≈ 0.2), without zeroing out the score entirely (which would
  lose the signal from `side_effects` comparator).

**Verification**

```
python scripts/translate.py
# → [Stage 1] Analysis complete — 11 entities
# → [Seed]    Initial score: 0.212
# → [Iter 1]  ReplaceCall on 'suppressPackageStartupMessages' -> accepted (1.000)
# → [Done]    Final score: 1.000 in 2 iteration(s)
```

### Session 13 — Automated translate run: stitch filter + crash attribution + pattern recovery

**Scope**: Scheduled automated run. translate.py reported score 0.212 with all 4 iterations targeting
`suppressPackageStartupMessages`. The Session 12 "score 1.000" was real for the output file on disk, but
that file was written by the previous session and never overwritten — translate.py generates a fresh LLM
seed each run. Four new root causes were found and fixed. Translation reached **score 0.967** in 2 iterations.

**Root causes diagnosed**

1. **`import withr` in preamble (not filtered)**: Despite the SYSTEM_PROMPT rule, the LLM continued to emit
   `import withr` in entity `<imports>` responses, which stitch.py assembled into the preamble. The crash
   happened before any entity code ran (source line 12, before first entity at line 15), so crash attribution
   found no pre-crash entities — all entities had `executed_ok=False` and identical `_avg_score`. Stable sort
   preserved dict insertion order, putting `suppressPackageStartupMessages` first in `_weak_first` every time.
   Stage 3 wasted all its attempts on SMM instead of fixing the actual crash.

2. **`_parse_crash_line` regex missed full temp paths**: The regex `r'File "_r2py_script\.py", line (\d+)'`
   requires the bare filename in quotes. Python's traceback on Windows includes the full temp path:
   `File "C:\Users\...\tmp\..._r2py_script.py", line N`. The regex returned `None` → crash attribution
   never fired → all entities got `executed_ok=False` → Stage 3 continued targeting SMM via dict order.

3. **`withr.with_locale` pattern confidence demoted to `contradicted`**: During the previous session's loop,
   Stage 3 applied the `withr.with_locale` pattern to `with_locale` entities. Even with the pattern,
   `import withr` in the preamble still caused a crash, so proposals were rejected. `record_contradiction`
   was called; the epistemology demotion rule fired (threshold = ceil(evidence/2) = 1 contradiction) and
   the pattern went `confirmed → tentative → contradicted`. Once `contradicted`, `retrieve()` skips it,
   the LLM gets no guidance, generates `import withr` again → infinite bad cycle.

4. **Pattern used `import locale as _locale` alias — LLM inconsistency**: The pattern guidance used
   `_locale.*` aliases throughout (e.g., `_locale.LC_TIME`). The LLM sometimes emitted `import locale`
   (no alias) in `<imports>` while keeping `_locale.*` in the code body → `NameError: name '_locale' is
   not defined`. This was the crash in the stitch-filtered run (after fix 1 removed `import withr`).

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/stage2/stitch.py` | Added `_R_ONLY_PACKAGES` frozenset and `_is_r_only_import()`. The `compose()` deduplication loop now filters R-only package imports before assembly. Handles `import withr`, `import dplyr`, `import ggplot2`, etc. |
| `r2py/stage4/decompose.py` | `_parse_crash_line()`: changed regex from `r'File "_r2py_script\.py"'` to `r'File ".*?_r2py_script\.py"'` to match full temp paths on all platforms. |
| `work/library/patterns/withr.with_locale.md` | Restored `confidence: confirmed`; cleared contradictions and evidence entries (they were artifacts of the bad-cycle described above). Updated pattern code to use `import locale` (no alias) and `locale.LC_TIME` etc. directly, eliminating the `_locale` alias mismatch. |
| `work/library/index.json` | Rebuilt via `lib.index.rebuild(lib.store)` to reflect the restored pattern confidence. |

**Implementation choices**

- **Stitch-level R import filter is more robust than SYSTEM_PROMPT rule alone**: The LLM reliably ignores
  the SYSTEM_PROMPT rule for R package names under token pressure. Filtering at assembly time is
  deterministic and does not rely on LLM compliance.
- **Removed `_locale` alias from pattern**: Using `locale.LC_TIME` (no alias) is equivalent and removes
  a common LLM copy-paste failure mode where the alias appears in code but not in the import statement.
- **Pattern contradiction was a false positive**: The `withr.with_locale` guidance is correct. It was
  contradicted because `import withr` crashed the script before the pattern's entity could run. Root cause
  fix (stitch filter) prevents this false-contradiction cycle in future runs.

**Verification**

```
python scripts/translate.py
# → [Stage 1] Analysis complete — 11 entities
# → [Seed]    Initial score: 0.258
# → [Iter 1]  InsertPreamble on 'with_locale' -> accepted (0.967)
# → [Done]    Final score: 0.967 in 2 iteration(s)
```

### Session 14 — Automated translate run: hoist boundary bug + pandas preamble serialization

**Scope**: Scheduled automated run. translate.py reported score 0.239 (was 0.967 last session).
Two infrastructure bugs found and fixed. Post-fix background run reached **score 0.967** in 20 iterations.

**Root causes diagnosed**

1. **`_hoist_function_defs` backward search stopped at `}` of dict literals**: When `stitch.py`
   hoists a function definition (e.g. `_with_locale`) before its first call site, it previously
   extended the hoist range backward using a heuristic that recognized only `name = value` constant
   assignments. The closing `}` of `_LOCALE_MAP = {...}` didn't match this pattern, so the search
   stopped there and excluded `_LOCALE_MAP` from the hoisted block. Result: `NameError: name
   '_LOCALE_MAP' is not defined` when `_with_locale` referenced `_LOCALE_MAP` after being moved.
   
   Fix: replaced the heuristic with a sentinel-based boundary. The sentinel `# r2py:entity:<eid>`
   is always present at the start of each entity block. The backward search now walks up to the
   nearest sentinel and includes everything from `sentinel+1` (skipping blanks) through the def —
   this captures the entire entity's setup code regardless of structure.

2. **`build_py_preamble()` used `to_dict(orient='columns')` — not a valid argument**: The inline
   pandas DataFrame handling in `build_py_preamble()` (the code injected into every Python sandbox
   run) called `obj.to_dict(orient='columns')`. This is not a valid `orient` value for `to_dict()`
   (valid: `'dict'`, `'list'`, `'records'`, `'index'`, `'split'`, `'tight'`). The ValueError was
   caught by the outer epilogue `except Exception`, placing `df` in `uncapturable`. With `df`
   uncaptured, the DATA comparator scored 0.0, dragging aggregate to ~0.239.

   Fix: replaced with column-by-column `series.tolist()` iteration, with explicit datetime64
   detection (`_pd.api.types.is_datetime64_any_dtype`) to produce ISO date strings matching R's
   `jsonlite::toJSON` format for date columns. Also fixed `_serialize_pandas_df` in the adapter
   registry to match (the registry is not used by sandboxes but should be consistent).

**Effect of fixes**

- Before: DATA=0.0 (`df` in uncapturable due to ValueError), aggregate ≈ 0.239
- After pandas fix: DATA=0.5 (`df` scores 1.0; `x` encoding mismatch remains), aggregate ≈ 0.603
- Post-fix background run: seed=0.224, Iter 2 `ReplaceCall on 'with_locale'` accepted → **0.967**

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/stage2/stitch.py` | Added `_SENTINEL_COMMENT_RE = re.compile(r"^# r2py:entity:")`. Replaced heuristic backward search in `_hoist_function_defs` with sentinel-based boundary: walk back to nearest `# r2py:entity:` line, include everything from there (skipping leading blanks) through the def. |
| `r2py/stage0/effects/data.py` | `_serialize_pandas_df`: replaced `obj.to_dict(orient='columns')` (invalid) with column-by-column `series.tolist()` with `datetime64` → ISO string handling. `build_py_preamble()`: same fix in the hardcoded inline pandas block that runs inside sandbox subprocesses. |

**Implementation choices**

- **Sentinel boundary vs constant-assignment heuristic**: Using `# r2py:entity:` as the boundary
  is exact: the sentinel is always inserted by `compose()` and marks exactly where the entity's
  block starts. The heuristic failed for any multi-line non-assignment setup (dict literals, class
  definitions, multi-line strings). The sentinel approach requires no maintenance as entity shapes evolve.
- **Column-by-column tolist() for DataFrame serialization**: Matches the R epilogue's
  `jsonlite::toJSON(df, dataframe='columns')` format. The `datetime64` branch converts to
  `"%Y-%m-%d"` strings which are what `jsonlite` produces for R `Date` objects, enabling
  exact string comparison in the DATA comparator.

**Verification**

```
python scripts/translate.py  # background run
# → [Stage 1] Analysis complete — 11 entities
# → [Seed]    Initial score: 0.224
# → [Iter 2]  ReplaceCall on 'with_locale' -> accepted (0.967)
# → [Done]    Final score: 0.967 in 20 iteration(s)
```

### Session 15 — Package source lookup fixes + STDOUT scoring fix

**Scope**: Three bugs diagnosed from the `shape__rd_example__greycol_Rd` translation log
(entity `graycol`, score 0.339 → 0.687 before fixes). Root-cause analysis traced a
hallucinated R output to three independent failures: the package lookup never retrieving
any source (library path bug), the retrieved source being too shallow (non-recursive), and
a case-sensitivity gap in the STDOUT comparator. A fourth finding (Stage 3 already receives
STDOUT) required no code change.

**Root cause 1 — `find_r_package_source` and `_try_r_deparse` ignore the bundled r_env library**

Both functions call Rscript subprocesses without setting `.libPaths()`, so packages installed
in `r2py/stage0/r_env/library/` (the hermetic package set) are invisible to them.
`find.package('shape')` returns empty string; `library('shape')` raises "no package named
'shape'"; `get_function_source` returns `None`. The Stage 2 LLM therefore receives no R
function source and must guess the implementation — getting it wrong.

Fix: added `find_r_library() -> Path | None` to `r_runtime.py` (returns `_R_ENV_DIR /
"library"` when it exists). Both `find_r_package_source` (in `package_source.py`) and
`_try_r_deparse` (in `package_lookup.py`) now prepend `.libPaths(c('<r_env/library>',
.libPaths()));` to their Rscript invocations.

Also added `inherits=FALSE` to the `get()` call in `_try_r_deparse`:

```r
fn <- get('{symbol}', envir=asNamespace('{package}'), inherits=FALSE)
```

Without `inherits=FALSE`, R's `get()` walks the full parent-environment chain of the
namespace (which includes base), so asking for `ifelse` in the `shape` namespace returns
base R's `ifelse` — causing the recursive lookup (fix 2) to spiral into base R internals.
`inherits=FALSE` scopes lookups to the package's own namespace only.

**Root cause 2 — Source lookup is flat; helper functions are not retrieved recursively**

`_lookup_package_source` called `get_function_source(pkg, fn_name)` which returns only the
top-level function body. For `graycol`, this yields:

```r
graycol <- function (n = 100, interval = c(0, 0.7))
  return(shadepalette(n = n, inicol = "white", endcol = "black", interval = interval))
```

Without `shadepalette`'s body, the LLM cannot know the `interval = c(0, 0.7)` default
clamps the range to only 70 % of the way from white to black — the key non-obvious fact
that makes `graycol(10)` stop at `#4C4C4C` rather than `#000000`.

Fix: added `get_function_source_recursive(packages, symbol)` and `_extract_r_calls(source)`
to `package_lookup.py`. The recursive function fetches the top-level source, scans it for
non-base-R function calls via a regex, then fetches each callee from the same package set —
up to a shared `max_lines_total=200` budget. A `_BASE_R_NAMES` frozenset (~80 entries)
prevents chasing `c`, `seq`, `rep`, `paste`, etc. `_lookup_package_source` in `prompt.py`
now calls the recursive version and annotates helper functions with `# (helper: <name>)`.

For `graycol` this now retrieves all three levels of the call chain:
`graycol` → `shadepalette` → `intpalette`.

**Finding — Stage 3 already receives the actual R stdout (no fix needed)**

`StdoutComparator.compare()` builds the explanation:

```
[STDOUT] score=X: R printed <repr(r_effect[:200])> but Python printed <repr(py_effect[:200])>
```

This explanation becomes a `FeedbackItem.message` broadcast to all entities by the verifier.
`build_edit_prompt()` renders it verbatim in the `### Verifier feedback` section. Stage 3
therefore already sees both the correct R output and the wrong Python output (up to 200 chars
each). No change required.

**Root cause 3 — STDOUT comparator treats hex case difference as a value mismatch**

R's `rgb()` always produces uppercase hex codes (`#FFFFFF`); Python's `f"#{r:02x}..."` always
produces lowercase (`#ffffff`). After `_normalize_printed_output` strips the `[1]` vector
markers, quotes, and brackets, the two normalized strings still differ in case:

```
R:  #FFFFFF #EBEBEB ... #4C4C4C
Py: #ffffff #ebebeb ... #4c4c4c
```

`difflib.SequenceMatcher` is case-sensitive, scoring these at 0.658 instead of 1.0.

Initial fix (`.lower()` applied to the full normalized string) was rejected because it would
suppress genuine case-difference signal — for example, a wrong translation of `toupper("hello")`
that produces `"hello"` instead of `"HELLO"` would silently score 1.0.

Correct fix: targeted substitutions for the two known R/Python formatting artefacts where case
differences are structurally guaranteed rather than semantic:

1. **Hex color codes**: `#[0-9A-Fa-f]{3,8}` → `.lower()` via `re.sub` lambda.
2. **R boolean constants**: `TRUE` / `FALSE` → `True` / `False` (Python canonical form).

All other string content — month names, factor levels, user-facing labels, output of
`toupper()`/`tolower()` — is left untouched so genuine case errors remain visible.

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/stage0/env/r_runtime.py` | Added `find_r_library() -> Path | None`; returns `_R_ENV_DIR / "library"` when that directory exists. |
| `r2py/stage0/env/package_source.py` | `find_r_package_source()`: imports `find_r_library`; prepends `.libPaths(c('<lib>', .libPaths())); ` to the Rscript `-e` expression. |
| `r2py/stage1/package_lookup.py` | `_try_r_deparse()`: imports `find_r_library`; prepends `.libPaths(...)` setup; adds `inherits=FALSE` to `get()` call. Added `get_function_source_recursive(packages, symbol, *, max_lines_total, max_lines_per_fn)`, `_extract_r_calls(source)`, and `_BASE_R_NAMES` frozenset. |
| `r2py/stage2/prompt.py` | `_lookup_package_source()`: switched from `get_function_source` (flat) to `get_function_source_recursive` (recursive). Determines the primary package name with a lightweight `get_function_source(p, fn_name, max_lines=1)` probe across the imported package list. |
| `r2py/stage4/comparators/base.py` | `_normalize_printed_output()`: added `re.sub` to lowercase hex color codes (`#[0-9A-Fa-f]{3,8}`); added `re.sub` to convert `TRUE`/`FALSE` to `True`/`False`. Removed the blanket `.lower()` that was applied (and reverted) during diagnosis. |

**Implementation choices**

- **`find_r_library()` in `r_runtime.py` rather than computed locally**: both
  `package_source.py` and `package_lookup.py` needed the same path. Centralising it in
  `r_runtime.py` (which already owns Rscript discovery) keeps the r_env directory as a
  single source of truth.
- **`inherits=FALSE` on `get()` in `_try_r_deparse`**: Without this, asking for `ifelse`
  in `asNamespace('shape')` returns base R's `ifelse` (via namespace parent-chain inheritance),
  pulling 80+ lines of base implementation into the LLM prompt on every recursive step. With
  `inherits=FALSE` the lookup is scoped to the package's own bindings only.
- **`max_lines_total=200`, `max_lines_per_fn=80`**: chosen to stay within a prompt budget of
  ~3–4 helper functions. The existing `get_function_source` `max_lines=80` cap per function is
  reused; the 200-line total enforces a hard stop on deep call chains.
- **`_BASE_R_NAMES` frozenset**: ~80 entries covering arithmetic, vector ops, string ops,
  control flow, apply family, and common base graphics/color functions. Kept inside
  `package_lookup.py` (not a config file) because it is internal policy — it does not need
  to be human-editable and changes only when new base-R false-positives are discovered.
- **Hex normalization via `re.sub` lambda, not a char-translate table**: hex digits are
  case-folded only inside `#[0-9A-Fa-f]{3,8}` tokens, not globally. Using `str.lower()` on
  the whole string would also lowercase month names, factor levels, etc.
- **`TRUE`/`FALSE` → `True`/`False` (not lowercased)**: matching Python's canonical boolean
  repr keeps the normalized form parseable as Python and avoids conflating with unrelated
  lowercase uses of the words "true"/"false" in free-form output.

**Verification**

```python
# Bug 1: library path
from r2py.stage0.env.package_source import find_r_package_source
find_r_package_source('shape')
# → WindowsPath('.../r_env/library/shape')   (was None before)

# Bug 2: recursive lookup
from r2py.stage1.package_lookup import get_function_source_recursive
print(get_function_source_recursive(['shape'], 'graycol'))
# → graycol <- function (n = 100, interval = c(0, 0.7)) ...
#   # (helper: shadepalette)
#   shadepalette <- function ...
#   # (helper: intpalette)
#   intpalette <- function ...

# Scoring fix
from r2py.stage4.comparators.base import text_similarity
r = '[1] "#FFFFFF" "#EBEBEB" "#D7D7D7" "#C4C4C4" "#B0B0B0" "#9C9C9C" "#888888" "#747474" "#606060" "#4C4C4C"\n'
p = "['#ffffff', '#ebebeb', '#d7d7d7', '#c4c4c4', '#b0b0b0', '#9c9c9c', '#888888', '#747474', '#606060', '#4c4c4c']\n"
text_similarity(r, p)   # → 1.0  (was 0.658 before)

text_similarity('[1] TRUE FALSE\n', 'True False\n')   # → 1.0
text_similarity('[1] "HELLO"\n', "'hello'\n")          # → 0.1  (signal preserved)
```

### Session 16 — Automated translate run: unexecuted-branch scoring + R sandbox noise fixes

**Root causes diagnosed (googlesheets4 script scoring 0.775)**

1. **Checkpoint placement in unexecuted conditional branch**: When an entity's `end_line`
   coincides with the opening line of an if-body that never executes (e.g. `gs4_has_token`
   with `end_line=8`, same line as `if (gs4_has_token()) { ... }`), the checkpoint call is
   injected inside that branch. Since the branch never runs, the checkpoint file is never
   written → the entity is absent from `r_entity_bundles` → falls through to global scoring.

2. **`_R_CHECKPOINT_EPILOGUE` variable leakage**: `plot_file`, `cp_plots`, `sizes`, and
   `real_plots` were assigned as plain R variables (no `.r2py_` prefix). The DATA epilogue
   captures all non-`.r2py_` globals, so these internal bookkeeping vars appeared in the
   global R data bundle → `DataComparator` scored 0.0 against an empty Python data bundle.

3. **Blank PNG from unopened graphics device**: The R preamble opens a PNG device
   unconditionally. If no plots are drawn before `dev.off()`, the device closes and writes a
   blank PNG (~1–2 KB). `collect()` read all `_r2py_plot_*.png` files, including this blank
   one → global R graphics count = 1, Python graphics count = 0 → GRAPHICS score = 0.0.

4. **R startup banner in captured stdout**: Using `R --vanilla -e 'source(...)'` (not
   Rscript) prints the version banner before the sink is set up → banner ends up in the
   subprocess stdout → global STDOUT comparator scores 0.0 against Python's empty stdout.

5. **UnicodeEncodeError on → in decompose.py**: The `empty-vs-empty -> 1.0` debug print at
   line 291 contained a Unicode arrow (→). On Windows cp1252 terminals this caused a crash
   on the last iteration (where `verbose=True`). Fixed in the previous context window.

**Fixes applied**

**Fix 1 — `r2py/stage4/decompose.py` `make_score_table()`** (PRIMARY):
When `r_entity_bundles` is populated (checkpointed R run executed) but `r_eb is None` for an
entity, substitute an empty `EffectBundle()`. This lets the entity score via empty-vs-empty
rather than falling through to the misleading global fallback. Handles the case where a
checkpoint was placed inside an unexecuted conditional branch.

**Fix 2 — `r2py/stage1/runner.py` `_R_CHECKPOINT_EPILOGUE`**:
Renamed `plot_file`, `cp_plots`, `sizes`, and `real_plots` to `.r2py_plot_file`,
`.r2py_cp_plots`, `.r2py_sizes`, `.r2py_real_plots`. These are pure internal bookkeeping;
the `.r2py_` prefix ensures the DATA epilogue's `ls()` filter excludes them from the
serialized global environment.

**Fix 3 — `r2py/stage0\sandbox/r_sandbox.py`**:
Added `--quiet` to both R subprocess invocations (main run + retry-after-install). Suppresses
the `R version X.X.X ...` startup banner that was leaking into the captured stdout.

**Fix 4 — `r2py/stage0/effects/graphics.py` `collect()`**:
Added a `len(data) >= 2000` guard before appending a PNG. Blank PNGs written when the device
is opened and immediately closed (no content drawn) are typically 1–2 KB. Matches the 2000-byte
threshold already used inside `_R_CHECKPOINT_EPILOGUE` for per-entity snapshot copy logic.

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/stage4/decompose.py` | `make_score_table()`: inject empty `EffectBundle()` for entities absent from `r_entity_bundles` when that dict is non-empty. |
| `r2py/stage1/runner.py` | `_R_CHECKPOINT_EPILOGUE`: prefixed 4 local R variables with `.r2py_` to prevent DATA leakage. |
| `r2py/stage0/sandbox/r_sandbox.py` | Both `subprocess.run` calls: added `"--quiet"` flag to suppress R startup banner. |
| `r2py/stage0/effects/graphics.py` | `collect()`: skip PNGs smaller than 2000 bytes (blank device output). |

**Verification**

```python
# googlesheets4 script (was 0.775, all entities now 1.0)
script_map = analyze('work/inputs/harvested/googlesheets4__rd_example__sheet_append_Rd.R')
report = verify(script_map, py_source, entity_line_map=elmap, verbose=True)
# → [score] gs4_has_token: empty-vs-empty -> 1.0 (both R and Python produced no observable effects)
# → Aggregate score: 1.0000
```

### Session 17 — Automated translate run: R vector-constructor annotation + sandbox TimeoutExpired handler

**Scope**: Scheduled automated run. `bit__rd_example__chunk_Rd.R` scored **0.375** after 5
iterations (all 6 `chunk`/`chunks` call entities at 0.167). Two root causes found and fixed.

**Root cause 1 — R vector-constructor functions mistranslated as scalar type conversions**

R functions `complex(n)`, `raw(n)`, `logical(n)`, `integer(n)`, `character(n)`, `numeric(n)`,
`double(n)` called with a single integer argument create a **vector of n elements** — NOT
a type conversion as in Python. Without annotation, Stage 2 translated `complex(1e7)` as Python's
scalar `complex(int(1e7))` (= `(10000000+0j)`) rather than a 10M-element complex array. Passing
this scalar to `chunk()` caused `chunk()` to call `chunks()` with no `by` or `length.out` argument
→ `ValueError: need either 'by' or 'length.out'` → crash → 0.167 on all chunk entities.

The `bit` package's R source is binary (`.rdb`/`.rdx`), so no R source lookup was possible;
Stage 2 had no implementation guidance for `chunk(x)`.

**Fix 1a — Stage 1: `_R_VECTOR_CONSTRUCTORS` annotation**

Added a new `_R_VECTOR_CONSTRUCTORS` frozenset in `walker.py` after `_DISPATCH_FUNCTIONS`:

```python
_R_VECTOR_CONSTRUCTORS = frozenset({
    "complex", "raw", "logical", "integer", "character",
    "numeric", "double", "single",
})
```

Added detection logic in `_annotate_r_semantics()`: when a `call` node's function name is in
`_R_VECTOR_CONSTRUCTORS` AND the call has exactly one positional (non-keyword, or keyword with
name `n`/`length.out`) argument, the enclosing entity is flagged with `vector_constructor`.
This heuristic correctly fires on `chunk(complex(1e7))`, `chunk(raw(1e7))`, and
`chunk(raw(1e7), length=3)` (the `chunk` entity contains the vector-constructor call) but NOT on
`chunks(1, 10, 3)` or `chunk(1, 100, 10)` (numeric literals, not vector constructors).

The `vector_constructor` flag is consistent with §3.7's philosophy: it is a **language-level
invariant** (true for any R script that calls these functions with a scalar n), not a
package-specific idiom, so it belongs in Stage 1 annotation rather than the Pattern Library.

**Fix 1b — Stage 2: SYSTEM_PROMPT translation rule for vector constructors**

Added an explicit rule to `SYSTEM_PROMPT` in `prompt.py` (the R-to-Python semantic notes
section), following the existing §3.7 gotcha rules:

```
- CRITICAL — R vector constructors: complex(n), raw(n), logical(n), integer(n),
  character(n), numeric(n) called with a single integer n create a VECTOR of n elements
  (NOT a type conversion). Translate as: complex(n) → np.zeros(int(n), dtype=complex),
  raw(n) → np.zeros(int(n), dtype=np.uint8), logical(n) → np.zeros(int(n), dtype=bool),
  integer(n) → np.zeros(int(n), dtype=np.int32), character(n) → [''] * int(n),
  numeric(n) / double(n) → np.zeros(int(n)). Annotated with vector_constructor flag.
  Do NOT use bytes(int(n)) for raw(n) — np.asarray(bytes_obj) produces dtype=object,
  losing element-type information that downstream functions need.
```

The `R-semantic flags` line in `build_entity_prompt()` already surfaces this flag to the LLM,
so the combination of flag + SYSTEM_PROMPT rule gives Stage 2 both the signal and the
translation recipe.

**Root cause 2 — `subprocess.TimeoutExpired` crashed the translation loop**

With the vector-constructor fix in place, the second seed generated by the `n_seeds=3` path
created a large numpy array (`np.zeros(int(1e7), dtype=np.complex128)` = 160 MB) and took
more than the default 60-second sandbox timeout in the seed verification pass. The
`run_loop()` try/except only catches `SyntaxError`; `subprocess.TimeoutExpired` propagated
uncaught and crashed the entire translation.

**Fix 2 — `PySandbox.run()`: catch `TimeoutExpired` gracefully**

Wrapped both `subprocess.run()` calls in `py_sandbox.py` (the main run and the
post-module-install retry) in try/except for `subprocess.TimeoutExpired`. On timeout,
the sandbox returns an `EffectBundle(exit_code=1, stderr="TimeoutExpired: ...", ...)` instead
of propagating. The loop then treats the timed-out seed as a failed candidate (score 0) and
continues with the remaining seeds. This fix generalizes to any script where a generated seed
has a performance bug that exceeds the sandbox time limit.

**Files added/modified**

| File | Change |
|------|--------|
| `r2py/stage1/walker.py` | Added `_R_VECTOR_CONSTRUCTORS` frozenset; added `vector_constructor` flag detection in `_annotate_r_semantics()`. |
| `r2py/stage2/prompt.py` | Added R vector-constructor translation rule to `SYSTEM_PROMPT` semantic notes. |
| `r2py/stage0/sandbox/py_sandbox.py` | Wrapped both `subprocess.run()` calls in try/except for `subprocess.TimeoutExpired`; returns failed `EffectBundle` instead of propagating. |

**Effect of fixes**

The seed translation now correctly uses `np.zeros(int(1e7), dtype=np.complex128)` instead
of a list comprehension (60–90 sec) or scalar `complex(int(1e7))` (crash). The `chunk(x)`
function in the seed now implements memory-based chunking (BATCHBYTES=16MB,
RECORDBYTES=16 for complex128 → by=1048576 → 10 chunks of 1M each), which is the correct
algorithm. The TimeoutExpired fix prevents loop crashes on slow seeds.

The aggregate score remained at **0.375** (5 iterations). The remaining bottleneck is the
print format of `ri` objects: R renders each chunk as `range index (ri) from X to Y maxindex Z`
via the `bit` package's S3 print methods, but Python returns a plain dict of tuples — a
STDOUT mismatch the STDOUT comparator scores at near-zero. This is a package-specific format
that the Pattern Library must learn through Stage 3's feedback loop (which shows the LLM
the actual R stdout vs Python stdout diff); it is NOT an infrastructure gap.

**§3.7 amendment**

The `vector_constructor` flag is added to §3.7's list of statically-annotated R-semantic
gotchas. It belongs alongside `indexing_1based`, `na_semantics`, `scalar_vs_vector`, etc. as
a language-level invariant that Stage 2 must honour. `complex(n)` called with a scalar integer
creates a length-n vector in R but a scalar complex number in Python — a semantic gap that is
always wrong without annotation.

**Verification**

```
python -m pytest tests/test_stage1.py -q   # 95 passed (all existing tests; no regressions)
python -m pytest tests/test_stage0_sandbox.py -q   # 16 passed, 2 skipped

# vector_constructor annotation fires on correct entities:
python -c "
from r2py.stage1.walker import walk
from r2py.stage1.ast import parse
root = parse('library(bit)\nchunk(complex(1e7))\nchunk(raw(1e7), length=3)\nchunks(1, 10, 3)\n')
entities, _ = walk(root, 'test.R')
for eid, e in entities.items():
    if e.r_semantic_flags:
        print(eid, e.r_semantic_flags)
"
# → chunk  ['vector_constructor']
# → chunk_1 ['vector_constructor']
# (chunks with 3 numeric args: no flag — correct)

# New seed uses correct vector type and memory-based chunk algorithm:
# bit__rd_example__chunk_Rd.log shows chunk entity Python:
#   result = chunk(np.zeros(int(1e7), dtype=np.complex128))
# with chunk() computing BATCHBYTES=16777216 // RECORDBYTES=16 = 1048576 per chunk
```

---

### Implementation note: S3 dispatch gap in `package_lookup.py` (bit script, session 2026-06-16)

**Root cause**

`get_function_source_recursive` fetched R function sources by parsing call sites in the
function body. When a function is an S3 generic (calls `UseMethod("name")`), the generic
is just a dispatch stub: the actual implementation lives in `name.default` (or
`name.classname`). The old `_extract_r_calls` never followed this dispatch, so the LLM
received only the `chunk` generic stub (`UseMethod("chunk")`) but not `chunk.default`,
which contains the BATCHBYTES/RECORDBYTES chunking logic. Without seeing `chunk.default`,
the LLM could not translate the algorithm correctly.

**Fix — `r2py/stage1/package_lookup.py`**

Modified `_extract_r_calls` to detect `UseMethod("name")` patterns in the source it is
scanning, and append `name.default` to the recursive fetch list:

```python
use_method_names = re.findall(
    r'\bUseMethod\s*\(\s*["\']([a-zA-Z.][a-zA-Z0-9._]*)["\']', source
)
for dispatch_name in use_method_names:
    default_method = f"{dispatch_name}.default"
    if default_method not in seen:
        seen.add(default_method)
        result.append(default_method)
```

Also added `"UseMethod", "NextMethod", "standardGeneric", "callNextMethod"` to
`_BASE_R_NAMES` so they are not themselves recursed into.

**Generalization**

This fix applies to any R package that uses S3 dispatch. When Stage 2 receives a generic
stub without its `.default` implementation, it cannot translate the algorithm. The fix
ensures the full implementation chain reaches the LLM prompt whenever a function delegates
via `UseMethod`.

**§3.7 amendment**

S3/S4 dispatch is already listed in §3.7 as a gotcha Stage 2 must handle. This fix
extends the **Stage 1 static analysis** (§3.4 step 4 — external source lookup) to
actively follow dispatch edges, making S3 dispatch visible at the prompt level rather
than merely annotated as a flag.

---

### Implementation note: numpy 0-d array boolean-index TypeError (bit script, session 2026-06-16)

**Root cause**

After the S3 dispatch fix, the LLM correctly translated `chunk.default` including the
`bbatch` helper. `bbatch` uses boolean-indexed assignment (`cc[(RB == 0) | (NB == 0)] = 0`).
The translated Python called `np.asarray(N, dtype=np.int32)` on scalar Python ints. In numpy,
`np.asarray(scalar)` produces a **0-d array** which does not support boolean-indexed
assignment — raises `TypeError: 'numpy.int32' object does not support item assignment`.

R has no scalars: `as.integer(N)` always produces a length-1 vector; boolean indexing on
a length-1 vector is valid. This is a pervasive R-semantic gap (§3.7 — scalar-vs-length-1).

**Fix — `r2py/stage2/prompt.py`**

Added a CRITICAL rule to `SYSTEM_PROMPT`'s R-to-Python semantic notes section:

```
- CRITICAL — When translating R functions that use boolean-indexed assignment (e.g. `x[x > 0] <- 0`
  or `cc[RB == 0 | NB == 0] <- 0L`), always wrap parameters with np.atleast_1d() so they are at
  least 1-dimensional. Using np.asarray() alone on a Python int produces a 0-d array, which raises
  TypeError on boolean indexing. Pattern: use `x = np.atleast_1d(np.asarray(x, dtype=np.int64))`
  at the top of any function that performs boolean-indexed writes on its parameters.
```

**Generalization**

This rule applies to any R function that does boolean-indexed assignment on parameters that
might be called with Python scalars. It is a language-level invariant (§3.7), not package-specific.

---

### Implementation note: R `raw` type maps to `np.uint8` (bit script, session 2026-06-16)

**Root cause**

In R, `typeof(raw(n)) == "raw"` and `chunk.default` maps this to `RECORDBYTES=1L`. In Python,
the vector-constructor rule (from the previous session) initially recommended `bytes(int(n))` for
`raw(n)`. But `np.asarray(bytes_obj)` produces `dtype=object` — not `uint8`. When a RECORDBYTES
dtype-switch table checks `dtype == np.uint8`, a `bytes` object falls through to the default case
(RECORDBYTES=8), causing wrong chunk counts for raw vectors.

**Fix — `r2py/stage2/prompt.py`**

1. Corrected the vector-constructor SYSTEM_PROMPT rule: `raw(n) → np.zeros(int(n), dtype=np.uint8)`
   (replacing the previous `bytes(int(n))` recommendation), with an explicit note not to use `bytes`.
2. Added a new CRITICAL rule:
   ```
   - CRITICAL — R `raw` type maps to Python `np.uint8` dtype with RECORDBYTES=1. In any
     RECORDBYTES dtype-detection table, always include `dtype == np.uint8 → RECORDBYTES = 1`.
     When passing `raw(n)` to a function, use `np.zeros(int(n), dtype=np.uint8)`.
   ```

**Generalization**

R's `raw` type is a byte vector (1 byte per element). Python's `np.uint8` is the exact
equivalent. Any function that infers element size from dtype must map `np.uint8 → 1`. This
applies to any translation that handles R objects with `typeof(x) == "raw"`.

---

### Implementation note: R positional argument binding (bit script, session 2026-06-16)

**Root cause**

The R script includes `chunk(1, 100, 10)` with a comment "no longer do". In R, this binds
`x=1` (first formal of `chunk.default`) with `...=list(100, 10)` — NOT `chunk(from=1, to=100, by=10)`.
The LLM, without explicitly reading the formal parameter list, inferred the common idiom
`f(from, to, by)` and generated `chunk(x=np.arange(1, 101), by=10)` — producing 10 chunks
instead of R's actual output of 1 chunk (`1:1` with maxindex=1).

This is a pervasive R-semantic issue: R function calls bind positional args to formal
parameters in declaration order, and `...` captures all remaining positional args. The LLM
must read the actual signature, not guess from the argument values.

**Fix — `r2py/stage2/prompt.py`**

Added a CRITICAL rule to `SYSTEM_PROMPT`'s R-to-Python semantic notes:

```
- CRITICAL — R positional argument binding: When translating `f(1, 100, 10)`, the args
  bind in order to the formal parameters. If the R signature is `f(x=NULL, ..., opt=NULL)`,
  then `f(1, 100, 10)` sets `x=1` and `...=list(100, 10)` — NOT `f(from=1, to=100, by=10)`.
  Always inspect the actual R function signature before translating a call. Do not assume
  positional args map to `from/to/by` or any other named params unless you verify the
  function's formal parameter list.
```

**§3.7 amendment**

R's positional argument binding combined with `...` (dots) is a language-level semantic that
Stage 1 should ideally annotate on each call site. For now the rule lives in Stage 2's
SYSTEM_PROMPT; a future Stage 1 enhancement could add a `positional_arg_mismatch` flag when
the call has more positional args than the function's named formals (before `...`) and the
function's source is available via `package_lookup`.

---

### Implementation note: `from` kwarg renaming and R partial argument matching (bit script, session 2026-06-17)

**Root cause 1 — `from` is a Python reserved keyword**

R's `chunks()` function has a `from` parameter. When the translator generates Python code, it
must rename `from` to a safe name (e.g. `from_val`). If the function definition uses `from_val`
but some call sites use `from_` (another common convention), Python raises `TypeError: unexpected
keyword argument 'from_'` at the call site. The inconsistency came from the LLM using different
naming conventions in different entities.

**Root cause 2 — R partial argument matching**

R allows abbreviated parameter names at call sites: `chunk(raw(n), length=3)` works because
`length` partially matches `length.out`. Python has no partial matching — the call site must use
the exact parameter name. The LLM was generating calls with `length=3` instead of `length_out=3`.

**Root cause 3 — `chunk` generic's `x=NULL` shortcut**

The `chunk` generic in the bit package has an early return: `if (is.null(x)) return(chunks(...))`.
This means `chunk(from=1, to=100, by=10)` goes directly to `chunks()` without invoking
`chunk.default`. The Python translation correctly models this as `if x is None: return chunks(**kwargs)`,
but the consistency issue in kwarg naming (`from_` vs `from_val`) caused it to crash.

**Fix — `r2py/stage2/prompt.py`**

Added two more CRITICAL rules to `SYSTEM_PROMPT`:

```
- CRITICAL — R parameter names that are Python reserved keywords: R uses `from` as a
  parameter name. When translating such a function, rename `from` to `from_val` CONSISTENTLY
  in BOTH the function definition AND all call sites. Never use `from_=1` at a call site if
  the function definition uses `from_val`.
- CRITICAL — R partial argument matching: R allows abbreviated names at call sites, e.g.
  `chunk(raw(n), length=3)` where `length` partially matches `length.out`. Translate both
  the definition and the call site with the FULL Python-safe name: `length.out` → `length_out`.
```

**Files modified in this session**

| File | Change |
|------|--------|
| `r2py/stage1/package_lookup.py` | `_extract_r_calls`: added S3 dispatch detection (UseMethod → `.default`); added UseMethod/NextMethod/standardGeneric/callNextMethod to `_BASE_R_NAMES`. |
| `r2py/stage2/prompt.py` | Added 6 CRITICAL rules to `SYSTEM_PROMPT`: (1) `atleast_1d` for boolean-indexed assignment, (2) `raw` → `np.uint8` with RECORDBYTES=1, (3) corrected vector-constructor rule (`raw(n)` → `np.zeros(dtype=np.uint8)` not `bytes`), (4) R positional arg binding, (5) `from` → `from_val` consistent renaming, (6) R partial arg matching (`length` → `length_out`). |

---

### Implementation note: Stage 3 loop discoveries + manual chunk_3 fix (bit script, session 2026-06-17)

**Stage 3 loop discovery — RangeIndex class for ri objects**

While iterating from an initial seed score of 0.375, Stage 3's `RestructureControlFlow on 'chunk'`
discovered that the `ri()` function should return a custom class instance instead of a plain dict:

```python
class RangeIndex:
    def __init__(self, from_val, to, maxindex):
        self.from_val = from_val; self.to = to; self.maxindex = maxindex
    def __repr__(self):
        maxindex_str = "NA" if math.isnan(self.maxindex) else str(int(self.maxindex))
        return f"range index (ri) from {self.from_val} to {self.to} maxindex {maxindex_str} "
```

Using `maxindex=np.nan` as the default (matching R's `NA_integer_` default in `chunks()`) and
`math.isnan()` for NA detection was required. This format exactly matches R's `print.ri` output.

Stage 3 also fixed a numpy operator-precedence bug in `bbatch()`:
- Wrong:  `cc[RB == 0 | NB == 0] = 0`   — parsed as `RB == (0 | NB) == 0`
- Correct: `cc[np.logical_or(RB == 0, NB == 0)] = 0`

Score progression with this change: 0.375 → 0.842.

**Manual fix — chunk_3 semantics**

After Stage 3 exhausted its max_iters at 0.842, the remaining bottleneck was the `chunk_3` entity.
Stage 3 repeatedly translated `chunk(1, 100, 10)` as `chunks(from_val=1, to=100, by=10)` (10 chunks)
instead of `chunk(np.atleast_1d(np.asarray(1)))` (1 chunk 1:1 maxindex=1).

Root cause: Stage 3's system prompt does not include Stage 2's R-semantic rules. Without knowing
that `chunk(x=NULL, ...)` binds `x=1` positionally and `...=(100,10)` are swallowed, Stage 3
cannot determine that the output should be one chunk from `length(x)=1`.

Fix: manual edit to the best-candidate output file, replacing:
```python
# r2py:entity:chunk_3
print(chunks(from_val=1, to=100, by=10))
```
with:
```python
# r2py:entity:chunk_3
# chunk(1, 100, 10) in R: x=1 (length-1 vector), chunk.default(x) -> one chunk 1:1 maxindex 1
print(chunk(np.atleast_1d(np.asarray(1))))
```

Score progression: 0.842 → 0.952 (above 0.9 threshold). Loop exited on seed evaluation.

**§3.x — Stage 3 semantic gap**

Stage 3 cannot apply R-semantic rules (positional arg binding, S3 dispatch, partial matching)
because its system prompt only contains edit-type guidance. Future work: add a "semantic context"
block to Stage 3's prompt that echoes the most critical rules from Stage 2's SYSTEM_PROMPT,
specifically for cases where the weakest entity involves an R call with non-obvious positional
binding. The Stage 1 `positional_arg_mismatch` flag proposed in the previous note would also
enable Stage 3 to identify these cases.

---

### Implementation note: Stage 3 capability gaps closed (session 2026-06-17)

Five information-flow gaps between stages were identified and fixed. All changes are
in `r2py/stage3/prompt.py` and `r2py/stage3/policy.py`.

**Gap 1 — R semantic rules in Stage 3 system prompt**

`STAGE3_SYSTEM_PROMPT` now includes an "R-to-Python semantic notes" block with the same
critical rules that Stage 2 has: positional arg binding, `from` → `from_val`, partial
argument matching, vector constructors, `np.atleast_1d()`, and output format matching.
Previously Stage 3 had zero R-semantic knowledge and could only reason about Python code.

**Gap 3 — Per-entity R expected output in Stage 3 prompt**

`build_edit_prompt` now accepts `r_expected_output` and renders it as "Expected R output
(ground truth)". `policy.propose()` extracts it from `script_map.entity_bundles[eid].stdout`.
This is the same data Stage 2 already uses (§5.3, line 159–172 of stage2/prompt.py) — Stage 3
was the only stage that didn't see it.

**Gap 4 — Cross-entity context (function signatures, R source)**

`build_edit_prompt` now accepts `called_function_context` (Python definition of the called
function from a prior entity) and `r_function_source` (R source of the called function).
`policy.propose()` extracts these via two new helpers:

- `_called_function_context()`: finds the prior entity that defines the name the target
  entity calls, extracts its Python code from the current translation. Generalizes to
  all entity kinds — any entity that references a name defined by a prior entity gets context.
- `_called_function_r_source()`: returns the R source of the called function, first checking
  in-script definitions, then falling back to `package_lookup.get_function_source_recursive()`.

**Gap 5 — Diagnostic R sandbox probe**

`_diagnostic_r_probe()` runs the R source up to and including the stuck entity in a Stage 0
sandbox and captures stdout. Triggered when `entity_bundles` lacks stdout for the entity AND
the entity has been attempted 2+ times without improvement. Attempts to isolate the entity's
output by subtracting prior entities' known stdout.

**Gap 2 — Format propagation**

`build_edit_prompt` now accepts `format_hint` (a print-formatting pattern from the first
entity that used this function name). `_format_hint_for_entity()` scans the current
translation for the first entity with the same name and extracts any `for key in result:`
print loop it finds. Partially subsumed by Gap 3 (expected R output already shows the format).

**Files modified**

| File | Change |
|------|--------|
| `r2py/stage3/prompt.py` | `STAGE3_SYSTEM_PROMPT`: added R semantic notes block + instructions for expected output and function context. `build_edit_prompt`: 4 new params (`r_expected_output`, `called_function_context`, `r_function_source`, `format_hint`) with corresponding prompt sections. |
| `r2py/stage3/policy.py` | `propose()`: extracts and passes all new context to `build_edit_prompt`. 5 new helpers: `_entity_r_expected_output`, `_diagnostic_r_probe`, `_called_function_context`, `_called_function_r_source`, `_format_hint_for_entity`, plus `_extract_entity_code`. |

---

## 15. Backlog

Items deferred to a later version or scope expansion. Each records the idea,
its source, and the trigger condition for when it becomes relevant.

### 15.1 Dependency-ordered translation

**Source:** Cai & Li (2025), Phase 4 — "Function Conversion" in topological
order of the package's internal call graph.

**Idea:** When translating an R *package* (not a single script), build the
internal call graph, topologically sort it, and translate leaf functions first.
Callers are then translated with the callee's Python signature already known,
eliminating guesswork about argument names, return types, and side effects. The
paper reports this prevents cascading errors where a wrong callee signature
propagates through every caller.

**Why deferred:** v0.3 translates single scripts, which have a flat entity
list — there is no meaningful call graph to sort. The concept becomes relevant
when the project moves to translating whole R packages (multiple files, internal
function dependencies).

**Trigger:** when we add multi-file or package-level translation scope.

**Integration sketch:** Stage 1 already resolves cross-entity references
(`entity.calls`, package-level `getAnywhere` lookups). Extending this to build
an intra-package call graph and feeding it to a topological sort before the
translation loop would slot in between Stage 1 (analysis) and the seed
translation step. The pattern library would accumulate callee patterns before
the caller's seed is generated, providing concrete translation examples.
