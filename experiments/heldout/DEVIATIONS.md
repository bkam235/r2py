# Deviations from PREREGISTRATION_2.md

Deviations from the second pre-registration (`PREREGISTRATION_2.md`, 2026-09-20, frozen code
`fe0b824eb61c6d675a26b11acafa8b86bef8c7f6`, `harness_hash = 5a2b026daa0a`). That document is
unchanged. Each entry states what was registered, what was actually done, why, and what it
does to the interpretation.

Timeline for context: training completed 2026-09-24 (256 scripts, 112.0 h, 155 patterns).
Scoring started 2026-09-25 ~06:05 UTC with 3 workers.

---

## D1. Restricting `analyze` and `status` to the checkpoints actually scored

**Applied 2026-09-25, while scoring was in progress.**

- **Registered:** the analysis runs over the five checkpoints in the manifest
  (`empty`, `f1of4`, `half`, `f3of4`, `full`).
- **Actual:** `r2py/heldout.py` and `scripts/run_heldout.py` were changed so that `analyze`
  and `progress` take an explicit `checkpoints` list
  (`experiments/patches/05-analyze-restricted-checkpoints.patch`, +27 −11). The default is
  unchanged — omitting the argument reproduces the previous behaviour exactly.
- **Why:** required by D2. `_trend` keeps a checkpoint as soon as *any* scored row mentions
  it, then keeps only the scripts present in *every* listed checkpoint. Leftover rows from a
  checkpoint that is no longer being scored would therefore have silently shrunk the trend
  test's `n` instead of being ignored. Simulated on the exact post-D2 state (60 scripts at
  `empty`/`half`/`full` plus the 8 leftovers at `f1of4`/`f3of4`), the trend test would have
  run on **n = 8** instead of **n = 60**, with no warning.
- **What the patch does:** adds the `checkpoints` argument; filters scored rows to that set so
  leftovers cannot leak into any statistic; records `checkpoints_analyzed` in the analysis
  output; applies the same restriction to `progress` so `status` reports the right
  denominator; adds `--checkpoints` to the `analyze` and `status` subcommands.
- **Effect on the harness:** none. `r2py/heldout.py` is the experiment runner and is excluded
  from `harness_hash()` by design; `scripts/run_heldout.py` is outside `r2py/` entirely.
  Verified before and after: `harness_hash` is **`5a2b026daa0a`**, unchanged, and every scored
  row recorded so far carries that same value.
- **Verification:** all 68 tests in `tests/test_heldout.py` pass. `analyze` was run against the
  partial score files in both modes to confirm the checkpoint list propagates to both trend
  tests and is recorded in the output. Only structural fields (checkpoint lists, sample sizes,
  error counts, harness hash) were inspected; no p-value, effect size or per-checkpoint mean
  was examined in that check.
- **Effect on results:** none by itself. No score is changed, added or removed. With the
  argument omitted the behaviour is identical to the registered version.

---

## D2. Reducing the scored checkpoints from five to three

**Decided and applied 2026-09-25.** Scoring was stopped and restarted at
**2026-09-25 13:44:03 local** with
`score --workers 3 --checkpoints empty half full`.

State at the restart: **40** scoring runs had completed under the registered five-checkpoint
design — **24** at the three retained checkpoints (8 each at `empty`, `half`, `full`, covering
8 held-out scripts) and **16** at the two dropped ones (8 each at `f1of4`, `f3of4`). The 24 are
carried forward and counted; the 16 remain in the score files but are excluded from the
analysis by D1. No run was discarded or re-run, and no score was altered.

- **Registered:** five checkpoints (`empty`, `f1of4`, `half`, `f3of4`, `full`), 3 repetitions,
  **60 × 3 × 5 = 900** scoring runs.
- **Actual:** three checkpoints (`empty`, `half`, `full`), 3 repetitions, **60 × 3 × 3 = 540**
  scoring runs. `f1of4` and `f3of4` are not scored further. Runs already completed at those two
  checkpoints are retained in the score files but excluded from the analysis by D1.
- **Why — compute budget, not results.** Projected wall-clock for the registered design, from
  39 completed runs across 8 distinct held-out scripts: per-script mean run time median
  21.3 min, mean 24.9 min; **bootstrap 90% CI on the total of 110–139 h** (~4.5–5.5 days
  remaining at 3 workers). The trimmed design needs ~61–72 h. The corpus is simply slower than
  the design assumed: 7 of the 8 scripts sampled average 16–48 min per run.
- **Effect on the primary endpoint: none.** The primary test is the paired one-sided Wilcoxon
  on the targetable-entity mean, `full` vs `empty`. Both checkpoints are retained and all 3
  repetitions are retained. Neither dropped checkpoint enters that test.
- **Effect on the secondary trend test:** Page's trend test runs over three ordered points
  instead of five. The dose-response span is preserved, because the dropped checkpoints are
  the least informative ones:

  | checkpoint | patterns | status |
  |---|---|---|
  | `empty` | 0 | kept |
  | `f1of4` | 56 | dropped |
  | `half` | 107 | kept |
  | `f3of4` | 141 | dropped |
  | `full` | 155 | kept |

  `f3of4` adds only 14 patterns over `half`, so the upper part of the curve was nearly flat in
  any case. The retained span is 0 → 107 → 155 patterns. Page's test requires at least three
  levels, which is met. The test is correspondingly less sensitive to a non-linear dose
  response, and that reduction in power is accepted here.

### Disclosure: what had been seen when this was decided

This decision was **not** blind. It is recorded here in full rather than presented as a
pre-specified choice:

- Per-checkpoint running mean scores had been visible in `status` output and in the scoring
  console log throughout, for the first ~40 of 900 runs (8 of 60 held-out scripts). The
  pre-registration permits these as operational monitoring; they were nonetheless seen before
  this decision was taken.
- No test statistic, p-value or effect size was computed on held-out scores before the
  decision. The `analyze` checks described in D1 reported only checkpoint lists, sample sizes,
  error counts and the harness hash.
- The decision rule applied was wall-clock cost against a fixed compute budget, and the
  quantity it was based on (run duration) is independent of the scores.
- The design-level question "is this experiment capable of detecting an effect at all?" was
  answered separately and **blind to all score data**, from the trained library and the
  held-out scripts' static structure alone: **155 patterns carry a translation example**,
  **14.9% of held-out entities (75/504) are targetable**, and **37 of 60 scripts have at least
  one targetable entity**, so the primary test is expected to run at n ≈ 37. This computation
  used no score file. It was used to decide *not* to abandon the experiment.

---

## D3. Re-running 176 scoring runs lost to OpenRouter credit exhaustion

**Occurred 2026-09-27. Recovery applied 2026-09-27 21:30.**

- **What happened:** the OpenRouter account ran out of credits partway through repetition 2.
  Every subsequent request failed with `402 — This request requires more credits`. The harness
  retried each run once, as registered, then recorded it as failed. Scoring ran to 540/540 with
  **176 runs recorded as failed** for this reason. Credits were then topped up.
- **Why this needed intervention:** `_score_loop` builds its skip-set from *all* rows in the
  score files, including error rows, so a failed `(checkpoint, script, rep)` triple counts as
  done and is never retried. Restarting `score` therefore did nothing — it exited immediately,
  having found all 540 triples present.
- **Grounds:** `PREREGISTRATION_2.md` permits intervention "for infrastructure failure (an API
  outage, a full disk, a provider change)". Exhausted API credits are such a failure: no run
  reached the model, so no score was produced, correct or otherwise.

**Extent, before recovery** (runs at the three analysed checkpoints):

| | rep 0 | rep 1 | rep 2 |
|---|---|---|---|
| scored | 177 | 177 | 1 |
| failed (402) | 0 | 0 | 176 |
| failed (other, see Notes) | 3 | 3 | 3 |

Errors were near-perfectly balanced across checkpoints (62 `half`, 62 `empty`, 61 `full`), as
expected from an account-level outage. Of the 62 affected script×rep triples, **61 failed at
all three checkpoints together**; exactly one (`timeDate__rd_example__base-sample_Rd.R`, rep 2)
failed at two of three.

- **Recovery performed:** the three per-worker score files were copied to
  `work/heldout/backup_scores_20260927_213032/`, then the **176 credit-failure rows were
  removed** so those triples become eligible again. Scoring was then restarted with the same
  command. Verified afterwards: 364 rows remain at the three checkpoints (355 scored + 9
  non-credit failures), no duplicate triples, and 176 runs pending.
- **No successful score was altered, discarded or re-run.** Only rows recording a failed API
  call were deleted. The one partially-failed triple keeps its single valid run rather than
  discarding it, so for that script's rep 2 one checkpoint was scored roughly a day earlier
  than the other two.
- **Effect on interpretation:** repetition 2 now runs 1–2 days after repetitions 0 and 1
  (reps 0 and 1 spanned 2026-09-25 06:00 to 2026-09-27 14:32). The design's protection against
  drift is that a script's *checkpoints* run adjacent in time, and that is preserved: the three
  checkpoints of each re-run triple are scored together. The primary contrast is computed after
  averaging over repetitions, so a shift affecting a whole repetition moves all three
  checkpoints equally and cannot masquerade as a library effect. Every row continues to record
  its own timestamp, harness hash and LLM settings.

---

## Notes (not deviations)

- **Nine retained failures, one script.** `tinytex__rd_example__tlmgr_Rd.R` failed at all three
  checkpoints in all three repetitions — 9 runs — and not through the API: the R script itself
  exits 1 with `Fehler in win_app_dir("TinyTeX"): The environment variable 'Pr...' ...`. This is
  a deterministic property of the script in this environment, not flakiness, so it is handled
  exactly as registered: recorded as failed, dropped from the means, and reported here. These
  rows were deliberately **not** cleared in D3, and re-running them would fail identically.
  Effect: that script contributes no paired observation, so the primary and secondary tests run
  on at most 59 of the 60 held-out scripts.

- **Parallel scoring** (3 worker processes) is as registered. The worker count is unchanged;
  raising it was considered and rejected, because the 60 s per-script timeout is wall-clock and
  additional contention could change scores, and because it would split the run across two
  contention regimes.
- **Harness frozen.** `harness_hash` has been `5a2b026daa0a` for every scored row, and
  `git status` reports no modification under `r2py/` other than `r2py/heldout.py` per D1. The
  improvement patches prepared in `experiments/patches/` (01–04) are **not** applied and must
  not be applied until this experiment is complete and analysed; they change what the library
  learns and would require a new pre-registration.
