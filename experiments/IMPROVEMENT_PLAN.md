# Improvement plan — harness changes after the current scoring run

**Implementation status (2026-09-29):** applied in the working tree, uncommitted — patches 01-04,
Stage 0a (per-entity `active_dims` / `dim_scores` / `executed_ok` / `uncomparable` in
`_entity_records`), Stage 0d (review retries, 2048 tokens, fails **closed**, truncated rejections
still reject, outcomes counted in `review_stats`), Stage 2b-1 (fixers run in shadow mode via
`stitch.shadow_autofix`; buckets and review failures land in each progress/score row),
Stage 2b-2 (syntax gate parses the shim-activated source; verifier dumps the assembled file on a
runtime SyntaxError), Stage 2b-3 (429 backoff 5->7 tries, `traceback` stored on error rows so the
RecursionError is diagnosable next time — its cause is NOT yet known, no fix attempted; R-only
names added to the pip skip list), Stage 3 (`replace_entity` action: `stitch.splice_entity`, parser,
loop branch, OpenRouter prompt; multi-span entities are refused, imports go inline).
**0b investigated, not decided** (`scripts/diagnose_comparators.py`, equivalent R/Python pairs
through the real sandboxes): **env** scores a *correct* translation 0.00 whenever R's diff holds an
R-internal option — `library(ggplot2|dplyr|cli)` alone sets `option:callr.condition_handler_cli_message`
— because Python can never emit `option:*` keys (structural bug in comparator+capture). **files**
scored 1.00 on an equivalent write (no bug found). **graphics** scored 0.887 for an equivalent
`plot(1:3)` (discriminating, just harsh; the real zeros are likely ggplot-vs-matplotlib mismatches,
undiagnosed). **0b decided (env):** `option:*` keys are dropped from both sides in `EnvComparator`; graphics and files unchanged. Scores before/after this change are not comparable (0c).
**Graphics (0b, second comparator) done:** every R page is now recorded (`%03d`, one device
segment per entity checkpoint; per-entity bundles carry all pages) and each page on both sides gets a
*content fingerprint* (`stage0.effects.graphics`: point/line data, bar heights, polygon/segment/image
counts, text). R base graphics are read from `recordPlot()` (needs `dev.control("enable")`, which the old
capture never set), ggplot from `ggplot_build(last_plot())`, matplotlib from artists. The comparator
pairs pages in order and compares fingerprints; **SSIM is no longer scored** (it measured white space:
empty axes 0.896 vs correct 0.888). Known limits: grid/lattice non-ggplot pages fingerprint as null and
are skipped; R legends add rects/segments; R default labels are ignored by a regex heuristic; extra
polygon/segment artists in Python are penalised. Graphics scores before/after are not comparable (0c).
**Graphics corpus + null rate:** `experiments/graphics_corpus/` holds 43 labelled R-vs-Python pairs
(16 correct incl. styled/zero-based/noise variants, 27 wrong: off value, dropped points, wrong type,
empty, swapped axes, wrong labels, wrong order); `evaluate.py` scores them and `tests/test_graphics_corpus.py`
guards it. It exposed three comparator defects, fixed: one wrong value in eight passed (verdict threshold
0.9 -> 0.99), right values in the wrong order scored 1.0 (ordered comparison, 0.85 credit for unordered),
and per-panel index shifts failed (series-aware x shift). Caveat: the comparator was tuned on this
same corpus, so its perfect separation is in-sample. `scripts/graphics_null_report.py` on the 60
held-out scripts: 9 plot (82 R pages), 91% of pages fingerprint usably (base 65%, ggplot 27%, null 9%);
Python side 74/74 pages fingerprinted; page count matches R in only 5 of 9 translations.
**Not done:** 0c, Stage 4+. Suite: 674 pass; the 4 pre-existing failures remain.
Original status line follows.

**Status:** nothing here is applied. The first experiment is **finished, analysed and written up**
(`experiments/heldout/RESULTS.md`; primary test p = 0.0569, H0 not rejected), so the harness is no
longer frozen. `harness_hash` is `5a2b026daa0a` at the time of writing.

Derived from the first training run (256 scripts, **112.0 h**, 155 patterns;
`experiments/train_stdout.txt`, `work/heldout/train_progress.jsonl`) and from the held-out
scoring run (496 scored runs; `work/heldout/scores.w*.jsonl`).

**Order of work — revised 2026-09-29 after the strategic reassessment below:**
**Stage 0 → Stages 1-3 → re-measure → then decide** whether the pattern library deserves more
investment at all. Stages 4-6 are conditional on what Stage 0 finds.

Patches and the approach note live in [`experiments/patches/`](patches/).

---

## Preconditions before applying anything

1. ~~Scoring complete~~ — **done**, 540/540 attempted, 496 scored.
2. ~~`analyze` run and written up~~ — **done 2026-09-29**: primary p = 0.0569, H0 not rejected
   (`experiments/heldout/RESULTS.md`). That run is the baseline for every metric below.
3. Commit the analysis output, `RESULTS.md` and `DEVIATIONS.md` **before** applying any patch, so
   the frozen run stays archived and reproducible.
4. Note that `r2py/heldout.py` and `scripts/run_heldout.py` already carry patch 05; everything
   else under `r2py/` is untouched.

---

## Evidence base

| Finding | Number |
|---|---|
| Training scripts reaching the 0.9 gate (taught the library) | **34%** (85/250) |
| Compute spent on scripts that taught nothing | **90%** (100.9 h of 112 h) |
| Rewrites that improved / unchanged / worsened the score | **16% / 39% / 45%** |
| Rewrites taking a positive score to 0.000 | **17%** (204) |
| Rewrites rejected for a Python syntax error | **227** (19%) |
| — of those, f-string backslash (legal from CPython 3.12; runtime is **3.10.6**) | 14 |
| Agent actions: rewrite / probe_r / lookup_docs / done | **1424 / 18 / 1 / 10** |
| Agent loops ending by stalling out (10 non-improving rewrites) | **61%** (85/139) |
| Step at which the best rewrite was first reached | median **2**, mean 4.7 |
| Rewrite steps taken *after* the best was already found | **40%** |
| Productive rewrite steps overall | **7.7%** (92/1196) |
| Worst three scripts | 10.7 h / 10.2 h / 5.5 h — **26 h**, none reached threshold |
| Auto-fixes for R calling conventions (arg order + reserved kwargs) | **328** |
| Scripts with unserialisable data entities | **30%** (51/169), 1278 warnings |
| Mean score: scripts with exclusions vs without | **0.522 vs 0.723** (8% vs 43% pass) |
| Pattern growth per quarter | 56 → 107 → 141 → **155** |
| Held-out entities targetable by the trained library | **20.0%** |
| Structural ceiling on targetability (key or base call) | **91.8%** |
| Library patterns the held-out set actually needs | **41 of 155** (74% irrelevant) |
| Script-level gain implied at the 91.8% ceiling | **+0.011 to +0.035** (base 0.683) |
| `env` / `graphics` / `files` observations scoring above 0 | **0 of 619** |
| Share of `by_effect` shortfall from those three | **69.8%** |
| Held-out runs reaching the 0.9 threshold | **28.8%** (143/496) |
| Anti-hardcoding review verdict on LLM error or truncated JSON | **passes** (fail-open, review.py:108/120) |
| Review call token cap (truncation → fail-open) | `max_tokens=512` |

---

## Strategic reassessment (2026-09-29)

Prompted by the question: *pattern coverage is low and retrieval was not shown to help — should we
increase coverage and re-test, or is the pattern library the wrong feature?* The honest answer is
neither: **the library works better than it looks, is aimed at the right failure mode, and is still
worth far less than three other things on this list.** The numbers below are recorded so the
decision is auditable later.

### Coverage is not architecturally capped

Computed exactly from the pipeline's own entity records for the 60 held-out scripts (499 entities,
package resolution including the R probe):

| | |
|---|---|
| Entities with a resolvable pattern key | **89.6%** |
| Entities with ≥ 1 informative nested base-R call | 37.5% |
| **Structural ceiling** (key or base call) | **91.8%** |
| Unreachable by any pattern, ever | 8.2% |
| **Actually targetable by the trained 155-pattern library** | **20.0%** |

An earlier static estimate put the ceiling at 38%; that was **wrong** — the static walker lacks the
R probe that resolves packages for unqualified calls. Use 91.8%.

### But the library learns largely irrelevant patterns

| | |
|---|---|
| Patterns in the trained library | 155 |
| Of those, keys the held-out set actually needs | **41** |
| Patterns for functions no held-out script calls | **114 (74%)** |
| Needed keys still missing | **179** |

So the gap is not "not enough patterns" but "patterns for the wrong functions". Worse, the missing
ones are long-tailed: the biggest misses unlock many entities each yet barely occur in the corpus —
`timechange.time-add` (22 entities, 0 of 700 sampled pool scripts), `grdevices.devasknewpage` (20,
0/700), `timechange.time-subtract` (16, 0/700). **Caveat:** the pool side was measured *without* the
R probe and therefore undercounts, so "76% of missing keys never appear" is an upper bound on
unlearnability (`ggplot2.geom-point` at 0/700 is certainly an artifact). Treat the direction as
established and the magnitude as unreliable.

### The arithmetic ceiling on the whole feature

Held-out entity-level effect × coverage = script-level gain:

| per-targetable-entity effect | at today's 20% coverage | at the 91.8% ceiling |
|---|---|---|
| +0.038 (headline estimate, p = 0.0569) | +0.0076 | **+0.035** |
| +0.0115 (robust, complete-reps subset) | +0.0023 | **+0.011** |

Against a base script score of 0.683 that is a **1.6%–5% relative improvement at perfect
coverage**. This is the most decision-relevant number in the project: it bounds the pattern
library's value even if every remaining engineering problem with it were solved.

For comparison, untouched: 45% of agent rewrites *lower* the score, 17% take a working translation
to 0.000, 19% emit invalid Python, and the reasoning loop is 7.7% productive.

### A measurement doubt that makes all of the above provisional

`env`, `graphics` and `files` scored **exactly 0.000 in all 619 observations** where they were
active — not one above zero. `env` is a binary exact-dict-equality comparator
(`r2py/stage4/comparators/env.py`), active in 487 of 496 runs. Together the three account for
**69.8%** of the total `by_effect` shortfall while carrying no discriminating signal.

**What was checked and refuted:** the hypothesis that this caps the aggregate, making the 0.9
threshold unreachable. It does not — 139 of the 143 runs that reached 0.9 had `env` active, and runs
with two pinned dimensions still score 1.000. The aggregate is computed over *entities*, not over
`by_effect` classes, so pinned effect classes do not impose a simple ceiling.

**What remains open, and is the reason for Stage 0:** how much these comparators depress the
*entity-level* endpoint cannot be determined from stored data, because per-entity `active_dims` are
not recorded. **The discriminating power of the dependent variable is currently unknown.**

### Revised priority

| rank | work | why | plan stage |
|---|---|---|---|
| 1 | Repair + validate the measurement instrument — comparators **and** the review fail-open | Nothing else can be evaluated without it; cost is hours | **Stage 0** |
| 1= | Delete both auto-fixers (shadow-instrumented) and check the assembled file | 328 silent fixes discard the feedback the library learns from; gate checks the wrong string | **Stage 2b** |
| 2 | Targeted edits (`replace_entity`) | Attacks the 45% regression and 17% catastrophic rate; acts on the whole score | Stage 3 |
| 3 | Agent-loop repairs + learn from sub-threshold scripts | Cheap, verified, independently justified | Stages 1-2 |
| 4 | Model-object comparability | 30% of scripts measured hollowly | Stage 4 |
| 5 | Pattern-library coverage | Bounded at +0.011 to +0.035 script-level | Stages 5-6 |

**Do not abandon the pattern library.** The control contrast — +0.038 on targetable entities
(r = +0.377) against +0.001 on non-targetable ones (r = +0.020) — is the only mechanism evidence the
project owns, and it cost 112 h to obtain. Demote it to fifth and stop treating coverage as the
central question.

---

## Stage 0 — repair and validate the measurement instrument

**Do this before applying any other patch.** It changes no translation behaviour, so it can land
while the rest of the plan is still being decided, and it is the precondition for reading any
later result.

### 0a. Record what the score is actually made of

`_entity_records` in `r2py/heldout.py` stores `id`, `name`, `key`, `calls`, `score` — and discards
the breakdown. Add per entity:

- `active_dims` — the dimensions actually compared;
- the per-dimension scores behind `entity_score`;
- whether the entity had any variable excluded as uncomparable (ties into Stage 4 Phase 0).

`entity_score` already reads `es.active_dims`, so the data exists at the point the record is built.
A few lines; changes no score. **This is the prerequisite formerly listed under Stage 5, promoted
here.**

Then answer, from the next run: what share of the entity-level endpoint can move at all?

### 0b. Decide what the three non-discriminating comparators should do

For `env`, `graphics` and `files`, each needs one of:

- **repair** — if the comparison is simply wrong (e.g. `env` comparing session state Python can
  never reproduce, or graphics compared byte-wise rather than structurally);
- **partial credit** — `env` is currently all-or-nothing on exact dict equality; a per-key score
  would at least discriminate;
- **exclusion** — if the dimension genuinely cannot be matched, it should not be scored. Note the
  verifier already excludes `uncomparable` verdicts from the aggregate, so the machinery exists.

Whichever is chosen, it must be a deliberate, documented decision rather than the current
accident, and it changes the meaning of every score — so it must precede the next pre-registration,
not follow it.

### 0d. Close the fail-open in the anti-hardcoding review

Found in the scoring log, then **confirmed in code**. `review_translation`
(`r2py/harness/review.py`) returns `True, ""  # fail-open` in two places:

- **line 108** — any exception from the LLM call (including the upstream `429` seen in the
  scoring log);
- **line 120** — any `json.JSONDecodeError` on the reviewer's response.

The review call uses `max_tokens=512`, and the reason string is free text, so a verbose
rejection truncates mid-JSON and then **passes**. This is not random: the longer the
explanation, the likelier the fail-open — i.e. exactly the more complex hardcoding cases.
The scoring log caught one in the act, where the response began

```
{"pass": false, "reason": "The Python code hardcodes the expected console output of the
'core' and 'core_layers' bundle objects as string literals (e.g., print(\"/* Sass Bundle */...
```

and the next line printed `[Review]  PASSED`.

**Why this is a Stage 0 item, not a Stage 2 one:** a hardcoded translation copies R's expected
output, so it scores *high*. A gate that fails open therefore admits high-scoring translations
that compute nothing — it inflates scores in a way that is invisible in the results. The review
gate is part of the measurement instrument, not just the agent loop.

Minimum fix: raise `max_tokens`, return a *structured* verdict instead of free-form JSON, and
**fail closed** (or retry) rather than open. Any change here alters which translations are
accepted, so it must land with 0b, before the next pre-registration.

### 0c. Re-derive the baseline

After 0a/0b, recompute the first run's numbers where possible and state plainly which baseline
metrics are comparable across the change and which are not. Scores before and after a comparator
change are **not** comparable; say so once, in `RESULTS.md`, rather than silently re-basing.

### Decision gate

If Stage 0 shows the endpoint is mostly movable, the first experiment's null stands as measured and
Stages 1-3 proceed. If it shows a large share of the endpoint is pinned, then **the first
experiment measured translation quality through channels that cannot respond**, the null is
uninformative rather than negative, and `RESULTS.md` needs a correction note to that effect.

---

## Stage 1 — patches 01–03 (built and verified, ready to apply)

Apply in order, then run the suite:

```bash
git apply experiments/patches/01-learn-from-subthreshold-scripts.patch
git apply experiments/patches/02-agent-loop-efficiency.patch
git apply experiments/patches/03-unlock-nonrewrite-actions.patch
python -m pytest tests -q
```

Already verified: every anchor matches exactly once, all edited files parse, all three apply
cumulatively via real `git apply`, and `test_patched_fns.py` passes. **Not** verified: the full
test suite, and anything needing a live translation. Note 4 tests already fail on the
unpatched tree (2 `test_stage0_effects`, 1 `test_stage0_sandbox`, 1 `test_stage2`) — they are
pre-existing and unrelated.

### 01 — learn from sub-threshold scripts
`r2py/__init__.py`, `r2py/heldout.py` (+16 −3)

Removes the script-level learning gate; `seed_from_translation` already filters per entity.
Includes the guard that makes this safe: `_score_in` returned **1.0** for an entity with no
active dimensions, so without it the library would fill with patterns learned from statements
that verify nothing.

- **Expected:** many more patterns per hour. The 51 exclusion-heavy scripts (8% pass rate)
  and the 137 scripts in the 0.3–0.9 band start contributing their verified statements.
- **Risk:** more but *thinner* patterns. 131 of the current 155 already have only one example.
- **Measure:** pattern count, **examples per pattern**, and share of patterns whose single
  example comes from a script that scored < 0.7.
- **Abort if:** median examples-per-pattern falls while pattern count rises — that is dilution,
  not learning.

### 02 — agent-loop efficiency
`r2py/harness/agent.py`, `r2py/heldout.py` (+39 −4)

- `max_stalls` 10 → **3** in `DEFAULT_PROTOCOL` (the module default was already 3).
- **Catastrophic-rewrite feedback.** The loop already re-prompts with `best_source`, so bad
  rewrites were always discarded — the agent was simply never told, and kept iterating against
  a version it believed was current. It now gets an explicit DISCARDED/REVERTED message.
- **Usable syntax feedback.** `_check_syntax` threw away `exc.text`/`exc.offset`; it now shows
  the offending line and a caret. It also silently mis-numbered lines (`ast.parse` runs on a
  copy with `# r2py:` lines stripped); showing the text sidesteps that.
- Correct hint for the 3.10 f-string error instead of a blanket "reserved keywords" guess.

- **Expected:** ~30–40 h saved; catastrophic-rewrite share and syntax-reject share both fall.
- **Risk:** `max_stalls=3` truncates the rare long climb — 12 of 92 improving loops first
  reached their best at step ≥ 13. Those scripts will now stop earlier, keeping the best found
  so far. Judged a good trade at 7.7% productive steps, but it is a real loss.

### 03 — unlock non-rewrite actions
`r2py/harness/prompt.py` only (+9 −2)

**The parser is not at fault.** `_parse_action` step 0 (`_ACTION_TAG_RE`) already handles
`ACTION: probe_r` / `done` / `lookup_docs` correctly and runs before every fallback, and *zero*
responses failed to parse in 112 h. Verified by test. The cause is the prompt:

- "REWRITE FIRST. When the score is low, rewrite immediately." → scoped to the first step.
- "Keep your analysis to 1-2 sentences. **ALL your output tokens should go to code.**" →
  replaced with a request to state which entities fail and what will change (2–4 sentences).
- New rule: a second *blind* rewrite is the most common way to lose score.
- States the runtime is **CPython 3.10** and that f-string expressions may not contain a
  backslash there.

- **Expected:** probe_r and lookup_docs rise from ~1% to something non-trivial; syntax rejects
  fall; the 45% worsening rate falls.
- **Risk:** more planning tokens per step means fewer steps per hour. If probing rises without
  the improvement rate rising, revert this one — it is the most speculative of the three.

---

## Stage 2 — patch 04, wall-clock budget

`r2py/harness/agent.py`, `r2py/loop.py`, `r2py/heldout.py` (+14 −0).
`agent_budget_s = 2700` (45 min), checked at each step boundary.

A step cap would never have caught the worst cases: `fansi__strwrap_ctl` burned 10.7 h in
**6 rewrites** (~107 min/step). Separable from Stage 1 because it changes only where compute is
truncated — apply it together with Stage 1 unless you want the two effects separated.

- **Limitation:** step-boundary check, so one pathological verification can still overrun.
- **Open question:** ~107 min for a single step is itself unexplained. The budget caps the
  symptom. Worth instrumenting the split between LLM latency, `harness.verify`, and
  `review_translation` before assuming it is the model.

---

## Stage 2b — auto-fixer removal, plus two defects the scoring log exposed

From the second scoring run's stdout. **Caveat on quantification:** that log was not saved to a
file (only the training log was), so the counts below are read off a pasted excerpt, not the
whole run. **Save the scoring stdout next time** — `score ... > experiments/score_stdout.txt`.
The mechanisms, however, are confirmed in code.

### 2b-1. Delete both auto-fixers — in shadow mode, so the cost is measured

**Decision (2026-09-29): remove `sanitize_keyword_args` and
`reorder_positional_before_kwargs` from the pipeline, but keep computing them and record what
they *would* have done.**

The two instructions "delete them" and "instrument before/after" pull against each other — once
deleted there is no after. Shadow mode satisfies both: stop applying the transforms, keep
measuring them. After one run you know exactly what deletion cost, and can revert on data rather
than argument.

#### Why delete

Every silent fix is a mistake the model is never told about. The fixers fired **328 times** in
training (255 arg-order, 73 reserved-keyword) — 328 pieces of discarded feedback, in a project
whose mechanism is *learning from verified translations*. The prompt already states both rules
explicitly (`prompt.py:159-167`) and the model violates them anyway; patching over that hides
both the rate and the correction signal. Patch 02 now shows the agent the offending source line,
so its own repair step is far better informed than when these fixers were written.

Two smaller reasons: the arg-order fixer **rewrites already-valid code**
(`f(k=1, *args)` → `f(*args, k=1)`, legal either way but a change in argument **evaluation
order**, observable when arguments have side effects); and it reports `changed=True` on files
that remain broken, which makes the log actively misleading — that is what produced the false
"the fixer corrupts source" claim this section previously carried.

#### Call sites

Four, in two files:

| file | line | context |
|---|---|---|
| `r2py/harness/agent.py` | 213 | `sanitize_keyword_args` on each agent rewrite |
| `r2py/harness/agent.py` | 216 | `reorder_positional_before_kwargs` on each agent rewrite |
| `r2py/seed.py` | 113 | `sanitize_keyword_args` on each seed translation |
| `r2py/seed.py` | 117 | `reorder_positional_before_kwargs` on each seed translation |

Both the seed path and the agent path must change together, or seeds and rewrites stop being
comparable.

#### Shadow mode

At each of the four sites, replace *apply* with *observe*: run the transform on a copy,
syntax-check the source before and after, record the outcome, then continue with the
**original** source. Four buckets:

| bucket | meaning |
|---|---|
| `valid → valid` | the fixer was unnecessary |
| `invalid → valid` | a genuine save — the cost of deleting |
| `valid → invalid` | corruption (never reproduced in 14 probes, but cheap to keep watching) |
| `invalid → invalid` | no help; some other error dominates |

Record per run alongside the entity records, with the fixer name and the site (seed vs agent).
Keep the transforms in `stitch.py` and their tests — only the call sites change — so reverting
is a three-line edit if `invalid → valid` turns out to dominate.

#### What to expect, and the honest risk

Syntax rejections will **rise**, and scores may fall, because errors the fixers were absorbing
now reach the gate. That is the point: the rate becomes visible, the agent gets told, and — if
the corrections mechanism works — those failures become learnable patterns rather than silent
repairs. But it is a real risk, and `invalid → valid` is the number that decides it. If that
bucket is large, the fixers were doing genuine work and should come back, ideally reimplemented
as AST-*located* text splices (find argument spans via `col_offset`/`end_col_offset`, splice,
re-parse) rather than token surgery.

**Do not** reimplement via `ast.parse` → `ast.unparse`: `unparse` discards comments, and the
pipeline depends on `# r2py:entity:` sentinels for entity mapping (`stitch.py:9`,
`rebuild_entity_line_map`). A round-trip would silently destroy them.

#### Pre-registration impact

This changes which translations are produced, so a run using it is not comparable to the first
experiment and it must be described in the next pre-registration. It pairs naturally with 0d and
0b, which are also accepted-output changes.

### 2b-2. The syntax gate checks a different file than the one that runs

Last session I flagged runtime `SyntaxError`s that had passed `_check_syntax` and said the
mechanism was unexplained. The scoring log identifies it:

```
File "..._r2py_script.py", line 251
    _r2py_prev_ns = set(k for k in globals() if not k.startswith('_r2py'))
IndentationError: expected an indented block after 'if' statement on line 250
```

`_r2py_prev_ns` is **harness-injected instrumentation**. The executed file is
`preamble + model source + injected code`, while `_check_syntax` parses the model source alone.
When the model's source ends mid-block — or puts bare prose where the data shim belongs — the
*concatenation* is invalid even though the fragment parsed.

The prose case is common and lands in the same place (lines 245-251, the shim boundary):
`No data shim needed for this script`, `The system will insert the data shim here`,
`(The shim will be inserted here by the system)`, `Simulated datasets from the diagram package`.
The model is describing the shim instead of preserving it, un-commented.

Fix: syntax-check the **assembled** file rather than the fragment, and on any runtime
`SyntaxError` dump the assembled source next to the run output so this is never guesswork again.

### 2b-3. Operational failure modes worth handling

- **Upstream shared-pool 429:** `google/gemma-4-31b-it is temporarily rate-limited upstream`
  — distinct from the account-level 429 that `RATE_LIMIT_TRIES` handles, and it reached both the
  agent and the reviewer. Worth its own backoff, and it is an argument for a provider key.
- **`RecursionError: maximum recursion depth exceeded`** killed whole runs (htmltools
  `capturePlot`, diagram) as a run-level ERROR, not a translation failure.
- **pip installs attempted for R package names** — `modeldata`, `googledrive`, `shinyapp`,
  `_curses` (the last is not even a legal package name). The "known unavailable" cache works, but
  the first attempt per name costs a network round trip and guarantees failure. An R-package
  denylist, or requiring evidence the name exists on PyPI, removes it.

---

## Stage 3 — the full-rewrite half (answering: should this be in 03?)

**No — it should be its own change, but it is the highest-value one.**

Reasons to separate it:

- **There is no cheap version.** The prompt says the rewrite must be the complete file *because*
  partial output would otherwise be spliced wrongly ("You MUST include ALL entities — do not
  stop early"). Relaxing that wording without splice machinery makes truncated rewrites legal
  and would be actively harmful. The constraint and the mechanism have to change together.
- **Attribution.** Stages 1–2 change learning, loop budget and prompt at once. Adding a new
  action type on top makes a changed outcome uninterpretable. These are cheap, verified and
  measurable; that one needs its own before/after.
- **Risk class.** Stages 1–3 are ~65 changed lines with pure-function tests. A new action needs
  splice logic, parser support, prompt support and end-to-end runs.

### Why it matters most

Every step forces regeneration of the whole file (median 110 lines) — that is simultaneously
the syntax-error generator and the reason 45% of rewrites lose score: the model must reproduce
working code perfectly in order to change three lines of it. Patch 03 relaxes only the
token-suppression half of this.

### Design sketch — `replace_entity`

The machinery already exists:

- `r2py/stage2/stitch.py:9` — `_SENTINEL_RE` matches `# r2py:entity:<eid>`.
- `r2py/stage2/stitch.py:270` — `rebuild_entity_line_map(source)` → `{eid: [(start, end), ...]}`.
- `r2py/__init__.py:169` — `_extract_entity_snippet` already slices an entity's span.

Proposed action:

```
ACTION: replace_entity
entity: e17
```python
<new Python for that entity only>
```
```

Loop handling:
1. `rebuild_entity_line_map(best_source)`; unknown eid → tell the agent, do not count a stall.
2. Splice the new body over that entity's line span, leaving every other line byte-identical.
3. Syntax-check the **whole spliced file** (not the fragment), then verify as usual.
4. Same accept/reject/keep-best path as `rewrite`.

Open design questions to settle first:
- **New imports.** A replacement may need an import that lives at the top of the file. Either
  allow an optional `imports:` block appended to the import section, or expose the preamble as
  a targetable pseudo-entity.
- **Multi-span entities.** `rebuild_entity_line_map` returns a *list* of ranges; replacing a
  multi-span entity needs a defined rule (replace first span, delete the rest?).
- **Helper functions** defined outside any entity span.
- Keep `rewrite` available for the first step and as a fallback.

**Expected:** near-elimination of the catastrophic class (17%), since untouched lines cannot
break, and a large drop in syntax rejects (a 5-line fragment is far easier to get right than
110 lines).

---

## Stage 4 — approach 5, model objects

Full design in [`patches/APPROACH-05-model-objects.md`](patches/APPROACH-05-model-objects.md).
Both sides emit a canonical **fingerprint** (normalised coefficients, fitted, residuals, n_obs,
family …) compared field-wise inside the existing DATA dimension.

### Phase 0: do the warnings go to the agent?

**No.** Phase 0 output is a *developer* worklist, not agent feedback. Three reasons:

1. **The agent cannot fix it.** The correct translation of `glm(...)` *is* a statsmodels object
   that `json` cannot serialise. The gap is in our capture layer, not in the translation.
2. **Telling it to would actively corrupt translations.** The only way for the agent to make
   the warning go away is to replace a real model fit with something serialisable — a dict of
   numbers. That is precisely the hardcoding failure `review_translation` exists to catch. We
   would be paying the model to degrade its output.
3. **It is a measurement-coverage fact, not a correctness fact.** It belongs in the score
   report and in `analyze`, next to error counts.

So Phase 0 is: record the **R class** and the **Python type** alongside the variable name
(today only the name is logged — 1278 warnings and 75 names, not one type), surface it as a
structured field rather than a `print`, and aggregate it in `analyze`. That converts guesswork
into a ranked adapter worklist.

The payoff comes at Phase 1+: once adapters exist, the fingerprint produces *real mismatches*
("coefficient `wt`: R −0.87, Python −0.41"), and **those** go to the agent as ordinary
comparison feedback. That is useful signal the agent can act on, unlike "could not serialise".

### Direction of the score effect is uncertain — measure it

I previously assumed this would lower scores. The training data does not support a confident
claim either way: scripts with exclusions already score **0.522 vs 0.723** and only 8% reach
threshold, so these are mostly failing already rather than coasting on skipped checks.
Treat the direction as unknown and measure it on a fixed subset before adopting.

Either way it is a **validity fix, not a score improvement**, it makes scores
non-comparable across the change, and it must be pre-registered.

### Cheaper partial step
Report excluded-entity counts per script in the score report and in `analyze`, so any claim
about the corpus carries "N% of data entities were not comparable". A few lines, no score
change, removes the silent part of the problem.

---

## Stage 5 — partially-verified patterns (the "lower the threshold" question)

The obvious way to grow library coverage is to lower `entity_score_threshold` from 0.9. This
stage says why that must not be done as a blind coverage fix, and what the testable version
looks like.

### It is a large lever, which is the reason for caution

Pooled over 4,327 scored entity observations from the first held-out run:

| entity score | share |
|---|---|
| 0.00 exactly | 7.6% |
| 0.00–0.30 | 9.0% |
| 0.30–0.50 | 1.9% |
| 0.50–0.70 | 11.5% |
| **0.70–0.90** | **25.9%** |
| 0.90–1.00 | 6.8% |
| 1.00 exactly | 37.3% |

Entity-observations clearing the bar: **0.9 → 44.1%**, 0.8 → 61.9%, 0.7 → 70.0%. So moving to
0.7 would qualify **59% more** entities. This is not a marginal knob.

### Why not simply lower it

1. **It is not the binding constraint.** The script-level gate is. Stage 1 (patch 01) unlocks
   the 137 sub-threshold scripts whose entities *already clear 0.9* — more patterns at the same
   evidence standard. That strictly dominates. Do it, measure, then ask whether more coverage is
   still needed.
2. **A pattern's value is that it is verified.** The prompt tells the model "See verified example
   below — prefer it over guessing from the R source alone." At 0.78 that sentence is false. The
   harm concentrates rather than dilutes: retrieval is exact-keyed, so a bad example for function
   `f` is shown on *every* occurrence of `f`.
3. **It corrupts the primary endpoint.** `targetable_ids` (`r2py/heldout.py`) counts any pattern
   holding a translation example, with no reference to quality or confidence. Lowering the
   threshold expands the targetable set with weaker patterns while reducing the expected benefit
   per targetable entity — growing the denominator and shrinking the numerator at once, so the
   measured effect gets *smaller* while coverage looks better.

### The safety valve exists but is currently switched off

`r2py/library/epistemology.py` already implements `confirmed` / `tentative` / `contradicted`
with promotion, demotion and conflict detection, and `_usable`
(`r2py/library/retrieval.py:36`) requires a tentative pattern to have **≥ 2 positive evidence**
before it may be shown. But every seeded pattern is created `confidence="tentative", seed=True`,
and `_usable` short-circuits on `seed` — *"Seeds are always kept regardless of evidence count."*
All 155 patterns therefore bypass the evidence requirement. The mechanism that would make a
lower threshold tolerable does not currently apply to the patterns in question.

### Prerequisite: Stage 0a

The 0.70–0.90 band is **not** uniformly "wrong translations". An entity at 0.85 may differ only
on a dimension irrelevant to the pattern's teaching value — stdout formatting, say — while the
translation itself is idiomatic and correct. Those examples would be worth learning from.

Answering that needs the per-entity `active_dims` and per-dimension scores, which **Stage 0a**
now provides (that instrumentation was originally specified here and has been promoted, because
it turned out to gate the validity of the endpoint itself, not just this stage).

**Do not tune the threshold before Stage 0 has run.** If a large share of the endpoint turns out
to be pinned at zero by non-discriminating comparators, the 0.70–0.90 band means something quite
different from what it appears to mean here.

### The testable design, if pursued

Not "lower the bar" but "add a second, clearly-marked tier":

- Keep **0.9** as the bar for a pattern that counts as *verified*.
- Store 0.70–0.90 examples with their score, and with **`seed=False`** so the existing `_usable`
  evidence rule actually gates them — they must accumulate ≥ 2 positive interactions before the
  translator ever sees them.
- Label them in the prompt with what is known: "partially verified (0.78): R and Python agreed
  on 3 of 4 compared effects" — not as guidance to prefer over the R source.
- **Exclude them from `targetable_ids`**, so the primary endpoint keeps measuring what it claims.
- Prefer a second *verified* example over a first partial one: 131 of 155 patterns currently
  hold exactly one example, so depth is likely worth more than breadth here.

Then it is a real experimental arm — does partial verification help, hurt, or do nothing — rather
than a coverage fix applied blind.

### Decision rule

Run it only after Stages 1–3 have been measured. If Stage 1 plus a repaired agent loop already
lift patterns-per-hour substantially, Stage 5 is probably not worth its complexity. If coverage
is still the binding constraint, the arm above answers the question honestly, and needs its own
pre-registration because it changes both what the library holds and the definition of a
targetable entity.

---

## Stage 6 — resolve the dose-response (the half-beats-full observation)

The first held-out run produced a non-monotonic dose-response on the primary endpoint
(`RESULTS.md`):

```
empty 0.697   ->   half 0.746   ->   full 0.735        (107 and 155 patterns)
n = 39:  non-decreasing 17, strictly increasing 2,  Page L p = 0.1825
```

Stepwise, `empty → half` accounts for more than the whole (+0.0487) while `half → full` is
slightly negative (−0.0106). **Neither is the registered contrast and neither may be promoted to
a result** — they are recorded because "more patterns did not help more" is worth understanding.

### Already ruled out

Three mechanisms were tested against the run's own data; none is supported:

| hypothesis | test | verdict |
|---|---|---|
| Patterns added `half`→`full` are weaker | example scores 0.985 (n=119) vs 0.978 (n=49); examples/pattern 1.11 vs 1.02; base-R share 35% vs 33% | **no** |
| Prompt crowding / cap truncation | no held-out script reaches the 8-base-pattern or 5-correction cap at either checkpoint; matched patterns/script 0.83 → 1.17 (max 4 → 5) | **no** |
| The added patterns actively mislead | 16 scripts gained a pattern (−0.0222) vs 23 unchanged (−0.0025); Mann-Whitney **p = 0.6381** | **no dose relationship** |

The remaining explanation is **sampling noise**: at n = 39 with 15 ties, 3 repetitions and
temperature 1.0, a −0.011 step sits inside the noise floor (`half → full` two-sided p = 0.41).

### What this actually means for the plan

The finding is about **power, not saturation**. The run could not resolve the dose-response, so:

- **Do not** design around a "patterns start hurting" effect. There is no evidence for one, and
  acting on it would be fitting to noise.
- **Do** treat per-run pattern-count/score curves as uninformative at this n, and stop reading
  the checkpoint means as a dose-response until the endpoint is better powered.

### How to resolve it properly

Cheapest first, and none of it needs a new held-out run:

1. **Raise targetability.** At 20% targetable, most entities cannot move, so the dose-response is
   measured on a thin slice. Stage 1 plus a repaired agent loop is the direct lever; measure
   targetability *before* committing to another scoring run (it is computable from the trained
   library and the held-out scripts' static structure alone, with no scoring — the method used in
   `RESULTS.md` matched the realised 20% from a blind pre-estimate of 14.9%).
2. **Reduce per-run noise at fixed cost.** More repetitions on fewer checkpoints buys more than
   more checkpoints on fewer repetitions, given ties dominate: 16 of 39 primary pairs were exact
   ties. Two checkpoints (`empty`, `full`) at 5 repetitions costs the same as three at ~3.3 and
   would sharpen the primary contrast, at the cost of abandoning the trend test entirely — a
   deliberate trade to consider rather than a default.
3. **Only then** re-introduce intermediate checkpoints, and pre-register the dose-response as a
   real hypothesis with a stated minimum detectable step, rather than as a descriptive trend.

### Decision rule

Run Stage 6 diagnostics (step 1) after Stages 1–3 land. If targetability does not clear roughly
40%, do not spend another scoring run on a dose-response question — the answer will again be
"cannot resolve".

---

## Measurement — how we will know each stage worked

Compute these from the training log for the current run (the baseline) and for each run after.
Worth productising as `scripts/analyze_train_log.py` so the comparison is reproducible rather
than ad hoc.

| Metric | Baseline | Target | Tests |
|---|---|---|---|
| Patterns per compute-hour | 1.38 (155 / 112 h) | ↑ | 01 |
| Median examples per pattern | 1 | not worse | 01 (dilution guard) |
| Share of scripts contributing ≥ 1 pattern | 34% | ↑ | 01 |
| Rewrites improving score | 16% | ↑ | 02, 03, Stage 3 |
| Catastrophic rewrites (positive → 0) | 17% | ↓ | 02, Stage 3 |
| Rewrites rejected for syntax | 19% | ↓ | 02, 03, Stage 3 |
| Productive share of rewrite steps | 7.7% | ↑ | 02 |
| Non-rewrite actions | 2% | ↑ | 03 |
| p95 wall-clock per script | ~85 min | < 45 min | 04 |
| Entities in the 0.70-0.90 band, by failing dimension | not recorded | recorded | 5 (prerequisite) |
| Share of held-out entities that are targetable | 20% | > 40% | 1-3, gate for 6 |
| Share of the entity endpoint that can move at all | **unknown** | measured | **0a** |
| `env` / `graphics` / `files` observations above 0 | 0 of 619 | discriminating, or excluded | **0b** |
| Review verdicts lost to fail-open (error or truncation) | **not recorded** | recorded, then 0 | **0d** |
| Auto-fixers applied | 328 (seed + agent) | **0** (shadow only) | **2b-1** |
| Shadow bucket `invalid → valid` (true cost of deleting) | **unknown** | measured | **2b-1** |
| Runtime `SyntaxError` after passing the gate | occurs | impossible (gate checks assembled file) | **2b-2** |
| Library patterns relevant to the target set | 41 of 155 | ↑ | 1, 6 |
| Total training wall-clock | 112 h | ↓ | all |

---

## Pre-registration impact

**Stage 0b is the most consequential change in this document.** Repairing, re-weighting or
excluding a comparator changes the meaning of every score, so results either side of it are not
comparable and no metric may be carried across it silently. It must land *before* the next
pre-registration and be described in it, not treated as an implementation detail.


01, 02 and 03 all change what the library learns or how well the translator performs, so a run
using them is **not** comparable to the current one and needs a new pre-registration. 04 changes
only where compute is truncated, but it too alters outcomes on slow scripts. Stage 2b-1
(deleting the auto-fixers) and Stage 0d (closing the review fail-open) both change which
translations are produced or accepted, so they belong in the same registration as 0b. Stage 3 and
Stage 4 are larger still.

Revised sequencing (2026-09-29), replacing the original suggestion:

1. **Stage 0** — instrument first. Changes no translation behaviour, so it needs no registration
   of its own, but 0b must be settled before the next one is written.
2. **Stages 1–2** — cheap, verified, independently justified.
3. **Re-measure**: targetability, and the share of the endpoint that can move.
4. **Decision gate.** Below ~40% targetability, do not spend another scoring run on the pattern
   library; go to Stage 3 instead, which acts on the whole score rather than 20% of entities.
5. **Stage 3**, then Stage 4 — each with its own before/after measurement.
6. **Stages 5–6** last, and only if coverage is still the binding constraint after all of the above.

The first experiment is closed and archived. Nothing in this plan may be used to re-analyse it;
`RESULTS.md` stands as written, with the one exception named in the Stage 0 decision gate — if the
endpoint turns out to be largely pinned, that is a correction to record, not a re-analysis to run.
