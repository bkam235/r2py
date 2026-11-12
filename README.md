<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="banner/banner-dark.svg">
    <img alt="r2py" src="banner/banner-light.svg" width="420">
  </picture>
</p>

<p align="center">
  An agentic R-to-Python transpiler that learns from its own mistakes.
  <br><br>
  <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="architecture.md">Architecture</a>
</p>

---

## What is r2py?

Most code translation tools are either rule-based (precise but incomplete) or LLM-based (flexible but unverified). r2py is a third approach: **translate, execute both versions, compare their behavior, and learn from the results.**

It translates R scripts to Python by combining LLM-powered code generation with execution-based verification. Both versions run in sandboxed environments, and the system compares their observable effects — printed output, data structures, plots, files, environment changes — to produce a decomposed score. A reasoning agent iteratively improves translations until they match.

The reward signal comes from running both scripts and comparing their observable effects side-by-side — if the Python version produces the same stdout, data frames, plots, and files as the R original, the translation is correct.

Verified patterns are extracted into a **Pattern Library** — a collection of Markdown files with evidence, confidence levels, and contradiction tracking. The library is reused on future translations, making the system self-improving without any model fine-tuning. Crucially, the Pattern Library closes the gap between frontier and local models: by front-loading verified R→Python knowledge into the prompt, smaller open-weight models like Gemma 4 can produce translations that would otherwise require a much larger model. Because learning is externalized rather than baked into weights, the same architecture could in principle be applied to other language pairs.

## How It Works

```mermaid
flowchart TB
    subgraph META["Meta-loop: improves the harness (person + strong model, one question per cycle)"]
        direction LR
        O["Observe"] --> DG["Diagnose"]
        DG -- measurement --> SC["Scorer fix:<br/>new epoch"]
        DG -- behaviour --> H["Harness option,<br/>off by default"]
        DG -- capability --> TM["Trained model,<br/>off by default"]
        H --> RG["Register"]
        TM --> RG
        RG --> T["Test"]
        T --> DC{"rule holds on<br/>training + held-out?"}
        DC -- yes --> AD["Adopt:<br/>flip the default"]
        DC -- no --> REC["Record"]
        SC --> REC
        AD --> REC
        REC --> O
    end
    subgraph GROUND["Ground loop: translates one script (Gemma 4 31B)"]
        direction LR
        R["R Script"] --> A["Analyze"]
        A --> S["Seed Translate"]
        S --> V["Verify"]
        V --> D{"score ≥<br/>threshold?"}
        D -- yes --> P["Python Output"]
        D -- no --> AG["Agent Refine"]
        AG --> V
        V -. learn .-> L[("Pattern Library")]
        L -. guide .-> S
    end
    META == "settings: defaults · versions: scorer epoch, policy" ==> GROUND
    GROUND == "telemetry: results, trajectories, health report" ==> META
```

**Analyze** — Parses R via tree-sitter, executes the script and unevaluated branches, catalogs all entities and effects, and flags R-specific gotchas (1-based indexing, NA semantics, vector recycling, non-standard evaluation).

**Seed Translate** — An LLM translates the whole file in one call, guided by relevant Pattern Library entries. Multiple candidates are generated and the best is selected.

**Verify** — Runs both R and Python in sandboxed environments. Compares 10+ effect classes (stdout, data values, graphics, HTML, files, environment, warnings, RNG state) using typed comparators. Produces a per-entity, per-effect score.

**Agent Refine** — If the score is below threshold, a reasoning agent iteratively rewrites the translation. Each rewrite must strictly improve the score — ties are rejected.

**Pattern Library** — Verified improvements are extracted as reusable patterns with confidence levels (`confirmed`, `tentative`, `contradicted`). Contradicted patterns are hidden from future translations. The library is diffable, version-controllable, and fully human-readable.

### The meta-loop

The translation loop above is the **ground loop**. The harness around it (its options and defaults, the scorer, the model) is improved by a second, slower loop: a person and a strong model ask one question per cycle and answer it with a pre-registered experiment.

- **One objective.** The plateau of the production default: the mean final score of the current `default_<date>` policy on 60 frozen training states, confirmed on 46 held-out states.
- **Three tracks.** Each cycle traces a concrete loss to its cause. A *measurement* fault goes to the scorer (a change is accepted by the person and opens a new scoring epoch, after which all past programs are re-scored); a *behaviour* fault becomes a harness option; a *capability* gap is a candidate for training the model on verified translations.
- **Experiments, not edits.** Every change is built behind an option that is off by default, registered in `experiments/registry.jsonl` with its hypothesis, metric and decision rule before any data, and tested with the cheapest instrument that answers it (single steps from frozen states cost under $1; a full replay about $4). It becomes the default only if the registered rule holds on the training pool and again on the held-out pool.
- **Three interfaces.** The meta-loop reaches the ground loop only through settings (an option's default), and reads it only through telemetry (results, trajectories, health reports); every result carries its scorer version and policy name.

The protocol is [`experiments/META_LOOP.md`](experiments/META_LOOP.md); every cycle is logged in [`experiments/IMPROVEMENT_PLAN.md`](experiments/IMPROVEMENT_PLAN.md), with the in-loop score curves in [`experiments/figures/`](experiments/figures/).

## Quick Start

### Prerequisites

- Python 3.10+
- [R](https://cloud.r-project.org/) (>= 4.4)
- An [Anthropic API key](https://console.anthropic.com/) or an [OpenRouter API key](https://openrouter.ai/)

### Install

```bash
git clone https://github.com/yourusername/r2py.git
cd r2py
pip install -e .
```

### Set up the R environment

The verification engine runs R scripts in a sandboxed environment with a project-local package library. The setup script installs all required R packages (~250 packages from the tidyverse, statistical modeling, and infrastructure stacks):

```bash
python scripts/setup_r_env.py
```

This takes 10–20 minutes on a fresh install. Packages are pinned via `renv.lock` for reproducibility. Any packages missing at runtime are auto-installed on first use, so the setup doesn't have to be exhaustive.

### Configure an LLM

Create a `.env` file in the project root with your API key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Or use a model via OpenRouter:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

### Translate

```bash
r2py translate analysis.R analysis.py
```

```
Score: 0.920  Iterations: 4
```

## Usage

### CLI

```bash
# Analyze an R script (writes .map.json and .annotated.R)
r2py analyze script.R

# Translate with options
r2py translate input.R output.py \
  --model claude-sonnet-4-6 \
  --max-iters 12 \
  --score-threshold 0.90

# Use a model via OpenRouter
r2py translate input.R output.py --model openrouter:google/gemma-4-31b-it

# Browse the Pattern Library
r2py library list
r2py library show <pattern_id>
r2py library review

# Harvest R examples from a package
r2py harvest ggplot2
```

### Python API

```python
from r2py import translate, analyze

result = translate(
    "analysis.R", "analysis.py",
    model="claude-sonnet-4-6",
    max_iters=12,
    score_threshold=0.85,
)
print(f"Score: {result.final_score:.3f}")
print(f"Iterations: {result.iterations}")

# Analysis only
script_map = analyze("script.R")
print(f"{len(script_map.entities)} entities, {len(script_map.effects)} effects")
```

## Design Decisions

**Execution equivalence as reward signal.** Translation quality is measured by behavioral equivalence, not textual similarity. This catches semantic errors that look syntactically plausible and prevents reward hacking.

**Strict improvement only.** The agent never accepts a rewrite that doesn't beat the current best score. Greedy hill-climbing prevents regressions.

**Externalized learning.** All knowledge lives in the Pattern Library as Markdown — no fine-tuning, no opaque embeddings. You can read, edit, and diff what the system has learned.

**Falsification-based epistemology.** Patterns are promoted by evidence and demoted by contradictions. Contradicted patterns are suppressed, not deleted, preserving the reasoning trail.

**Harness changes are experiments.** The harness changes only through the meta-loop: off-by-default options, tests registered before any data, decision rules set in advance, confirmation on a held-out pool. A scorer change is made because a measurement is wrong on a concrete program, never to move a result.

**Exact-first data comparison.** Numeric data is compared by dtype, shape, and value within tolerance. Embedding-based comparison is a fallback for infrastructure mismatches only, never for real value disagreements.

## Architecture

| Module          | Role                                                                   |
| --------------- | ---------------------------------------------------------------------- |
| `r2py/stage0/`  | Execution substrate — sandboxes, effect capture, R/Python environments |
| `r2py/stage1/`  | R script analysis — AST parsing, execution, entity cataloging          |
| `r2py/stage2/`  | Translation support — LLM client, data shims, keyword sanitization     |
| `r2py/stage4/`  | Verification — effect comparison, scoring, library updates             |
| `r2py/harness/` | Reasoning agent — iterative rewrite loop                               |
| `r2py/library/` | Pattern Library — storage, retrieval, epistemology                     |
| `r2py/scoring.py` | Scorer version and scoring epochs (meta-loop)                        |
| `scripts/`      | Meta-loop instruments — replay, step A/B, health report, registry, analysis |
| `experiments/`  | Meta-loop protocol, cycle log, experiment registry, pools, curves      |

For the full design rationale, stage specifications, and invariants, see [`architecture.md`](architecture.md).

## Status

r2py is a research prototype demonstrating that execution-verified, self-improving code translation is viable. The Pattern Library currently contains patterns learned from translating examples across the tidyverse, base R, and statistical modeling packages. The harness is developed through the meta-loop; the production default currently reaches a mean final score of 0.816 on the 60 training states (scoring epoch 9).

## License

[MIT](LICENSE)
