# Pre-registration 3: Does a library trained by the improved harness improve translation scores?

**Status:** WITHDRAWN 2026-10-07, before any data collection. Registered earlier the same day
(feature set, scoring checkpoints and parallel training confirmed), then withdrawn unrun: the
design tests a learning mechanism that the cheap instruments already show to be about flat
(learning-curve slope +0.011/100 training scripts, 95% CI [-0.014, +0.037]; 20% of held-out
entities informable), and nothing in the roadmap since changed how the library learns. Spending
~15 h of training and ~1 day of scoring to re-measure a known-flat mechanism was judged not
worth it; the work moves to raising informable coverage first. Nothing was run under this
document: `work/heldout3/` was never created. The text below stays unedited as a record.
No results may be reported under it; a future run needs a new registration.
**Date:** 2026-10-07
**Relates to:** `PREREGISTRATION_2.md` (first held-out experiment, closed: primary p = 0.0569, null;
see `RESULTS.md`). That document and its results stay unedited.
**Registered harness hash:** `a88d6b0f9892` (`heldout.harness_hash()`), code at commit `885c833`.
**Manifest:** `experiments/heldout/manifest_3.json`, sha256
`51a1808c3d522a06775d905307710672c0929f0570127f97387391a240d891db` (held-out and training lists
identical to `manifest.json`; `translate` block adds width 3, locate on, runtime store
`work/runtime/pilot_v2`, entity repair off, planned seeds 0). Work directory: `work/heldout3`.
Any later change to `r2py/` invalidates the run (see "Deviations").

## Why a third registration

The first experiment found no significant library effect (+0.038, p = 0.0569) and showed that only
about 20% of held-out entities were informed by the library. Work since then (documented in
`experiments/IMPROVEMENT_PLAN.md`, "Roadmap from 2026-10-03") changed what is *measured* and what
the harness *does*. Scores from this experiment are therefore **not comparable** with the first
experiment's absolute values; the comparison that matters is within this experiment (checkpoints
against each other).

## Hypotheses

**H1 (primary, unchanged in form).** Over the *targetable entities* of the fixed held-out scripts,
the mean verification score is higher with the fully trained library (`full`) than with the empty
one (`empty`). One-sided, same test, same alpha as `PREREGISTRATION_2.md`.

**H2 (secondary, the question the roadmap asks).** Scores improve *with training dose*: the
learning curve over the five checkpoints has a positive slope (see Analysis). This is the
"evolving harness" question and is reported next to H1 whichever way H1 comes out.

Everything else (whole-script score, control entities, per-stratum) is descriptive, as before.

## What changed since the first experiment

### Measurement (changes what a score means)
1. **R values captured at full precision** (`digits = NA`) instead of jsonlite's 4 decimals. Numeric
   comparisons that failed on rounding now pass or fail on the values.
2. **Fingerprint comparator** for R objects that cannot be serialised (model objects, XML/S4,
   environments, ...). Python objects are fingerprinted the same way; numeric fields are matched by
   value, text by canonical form. A fingerprint comparison counts only if informative (at least 5
   values with at least 5 significant digits; calibrated on a chance-match census, see
   `scripts/fingerprint_null_report.py`); otherwise the entity is *uncomparable* as before.
3. **Random-draw shim.** R's random draws are recorded in the R run and replayed to the Python
   run (numpy module functions, `default_rng`, `random`), only for draws originating in the
   script. The RNG effect itself is not scored. Scripts that draw random numbers can change score
   in either direction relative to the first experiment.
4. **Deterministic sentinel restoration** (with fuzzy assignment anchors) recovers entity markers a
   rewrite dropped; the data-shim block is hidden from the model and restored by the harness.

### Harness (changes what the model sees or does)
5. **Agent width 3** (`DEFAULT_AGENT_WIDTH`): three independent repair chains per run, best kept.
   The only clearly effective agent-stage change in the roadmap (paired +0.09 to +0.14).
6. **Imported-name gate:** `from module import name` for a name that does not exist is caught by
   the seed gate (with suggestions from the module and its submodules). **Unknown `r_*` reference
   gate** and a **static audit** that stays pinned in the prompt.
7. **Locator in repair:** the harness runs every call of a failing entity in R and in Python,
   aligns values and tells the model the first divergence. On in this experiment.
8. **Verified runtime store:** R base/stats functions re-implemented in Python, each accepted only
   if it passed differential tests against R (natural return types, mutants, mined real calls,
   purity gate). The store contains **28 pure functions** (`work/runtime/pilot_v2`); it is
   regenerated into the translation as a managed block (`# r2py:runtime:begin/end`), so
   translations stay self-contained. The runtime store is **frozen for this experiment**: it is
   identical for every checkpoint and does not grow during training. (Its effect is therefore part
   of the harness, not of the library, and cancels in checkpoint comparisons.)
9. **Off in this experiment:** entity repair, entity width, beam, recombination, lessons store,
   planned seed style (all null in the roadmap). Seeds: 2 bare, 2 structured, as before.
10. **Provider-outage handling:** a run in which any provider call failed for good (no credits,
    network, 5xx after retries) is *discarded*, never scored; the driver pauses, polls and repeats
    the run. Exit code 3 means it gave up waiting; the same command resumes. In the first
    experiment such outages could not be told from low scores. Counts of outages and repeated
    runs are reported.

### Manifest
The run needs a new manifest (same held-out and training lists, same seed) whose `translate` block
adds the settings of items 5-9 explicitly (width, locator, runtime-store directory, planned seeds
off), so that every row records them. Its sha256 is registered with the commit hash.

### Unchanged
Model `openrouter:google/gemma-4-31b-it`, temperature 1.0, provider pinned `novita/bf16`, no
fallbacks, 300 s request timeout; score threshold 0.9; 20 iterations; 10 stalls; 60 s script
timeout; held-out set and training list byte-identical to `manifest.json` (60 / 256 scripts,
sha256-verified); library semantics (function-keyed, exact retrieval, base-R patterns, verified
fixes, learning only from scores >= 0.9); throwaway library copy per scoring run, learning off in
scoring; randomised run order with recorded seeds.

## Design

### Training
- Library starts empty. 256 training scripts in manifest order, learning on.
- **Parallel, 5 workers.** The first experiment trained sequentially (112 h). Now each script is
  translated against a snapshot of the library taken when it starts, so it does not see patterns
  learned by up to 4 scripts still in flight (maximum staleness 4 of 256). Finished scripts are
  folded into the live library one at a time. This is a deliberate, registered deviation from
  "sequential" in the first experiment; the first experiment's library effect was the same in
  early and late scripts, so staleness is not expected to matter, but this is an assumption, not a measurement.
- A training script that errors is retried once, then skipped; provider outages never count as
  attempts (see 10).
- Checkpoints after 0, 64, 128, 192, 256 scripts: `empty`, `f1of4`, `half`, `f3of4`, `full`.
  Hash-verified before and after scoring. Trajectories, per-run model-call counts and settings
  (width, locator, runtime-store hash) are recorded on every row.

### Scoring
- 60 held-out scripts x 3 reps x **checkpoints `empty`, `half`, `full`** = 540 runs for the primary
  (as in the first experiment). `f1of4` and `f3of4` (a further 360 runs) are scored **only if** the
  first 540 are complete without infrastructure failure and the user approves the extra time;
  H2's slope is computed on whichever checkpoints were scored (at least three).
- 3 workers, randomised order per rep, one throwaway library per run.
- Scoring starts after training has finished.

### Time and cost (estimate, not a commitment)
Training about 13-16 h with 5 workers; scoring 540 runs with width 3 about a day. Neither is
started without the user's go-ahead.

## Endpoints and analysis

**Targetable entity, entity score, primary test, control, secondary analyses:** exactly as in
`PREREGISTRATION_2.md` (targetable = `full` library holds a verified-example pattern for the
entity's key or any base-R function inside it; set read from `full` checkpoint files only;
`suppressPackageStartupMessages` excluded; paired one-sided Wilcoxon, `zero_method = "wilcox"`,
alpha 0.05; `n_paired`, `n_nonzero`, two-sided p, rank-biserial, improved/tied/worse, by-stratum
descriptive).

**Added for H2 (secondary, reported in full whichever way it goes):**
- The learning-curve instrument (`scripts/learning_curve.py`) on the scored checkpoints: entity-level
  paired slope per 100 training scripts with a cluster (script) bootstrap 95% interval, runs in
  randomised order. It is the instrument that gave +0.011/100 [-0.014, +0.037] on the first
  library, so the new value can be compared directly.
- Page's trend test as before.
- **Coverage report:** share of held-out entities that are targetable under the new library, to
  compare with 20%.

## What counts as a positive / negative result
Positive: H1's one-sided p < 0.05. Otherwise the result is reported as null, with H2 and the
whole-script score next to it; no other endpoint is promoted after seeing the data. H2 is
interpreted as supportive only if its bootstrap interval excludes 0; a positive H2 with a null H1
is reported as exactly that.

Analysis runs once, after scoring is complete. `status` is for operations only. The experiment is
not stopped or altered on the basis of running scores, only for infrastructure failure.

## Prior contact with the held-out set (disclosure)
- Everything disclosed in `PREREGISTRATION_2.md`, plus: the first experiment's translations and
  scores on all 60 held-out scripts (`RESULTS.md`).
- Since then, the held-out scripts' translations under the *new* harness have been used in
  development: replay evaluations from frozen states of 24 of the held-out scripts (the
  development manifest `experiments/dev_run`), seed evaluations, and the runtime/locator pilots,
  which used failures from those runs as targets. These measured harness changes on held-out
  *scripts*; some harness choices (width, locator, gates, which runtime functions were built)
  were therefore shaped by seeing those scripts fail. This is a contamination risk for the
  absolute level of scores, but not for the checkpoint comparison, because every checkpoint
  runs under the identical harness. The development training subset overlaps the main training
  list in 12 scripts, and **one development training script is a held-out script** (it was
  translated with learning on in a development directory, never in the registered library; it is
  scored normally here, and its development library is not used).
- The `empty` library has no patterns; the runtime store (item 8) is separate and frozen.

## Known limitations, stated in advance
- All limitations of `PREREGISTRATION_2.md` apply (package coverage, 5 uncoverable packages,
  one realisation of training, temperature 1.0 with 3 reps, floor/ceiling ties).
- Absolute scores are not comparable with the first experiment (items 1-4, 5-8).
- Width 3 raises the ceiling and may leave less room for a library effect (a library example may
  now be found by search anyway).
- Parallel training introduces up to 4 scripts of staleness.
- Runtime-store functions overlap with base-R patterns the library can learn; the store may absorb
  part of the library's possible gain on base functions.
- Fingerprint and RNG changes affect only scripts with unserialisable objects or random draws; the
  per-script effect is not estimated in advance.

## Deviations
Logged in `experiments/heldout/DEVIATIONS.md` with timestamp and rationale, committed separately.
A change to the harness hash after registration invalidates the run and needs a new registration.
Operational interruptions (outage, Ctrl-C, resume) are not deviations; they are recorded in
`train_events.jsonl`.

## Confirmed by the user at registration
Feature set as above; scoring `empty`, `half`, `full` first; parallel training with 5 workers.
