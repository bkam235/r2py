# Improvement plan — harness and agent loop

> **Revised 2026-10-01** after reading `r2py_harness_insights.md` (a comparison with agentic coding
> harnesses) and checking its claims against the code and the smoke-test logs. The stage list below the
> next section is unchanged history; **new work is Stages 7-11**, ranked in the table that follows.
> The long status paragraphs that used to open this file are now the *Implementation log* further down.

## Roadmap from 2026-10-03: measurement first, then a harness that learns

**Why a new roadmap.** Of everything built so far, two changes moved scores: whole-loop width (+0.144 on frozen
states) and the seed-environment / data-shim fixes (seeds that run 34% -> 50%). Every *learning* mechanism was null
(pattern library p = 0.057, lesson store, a third seed style). Search works but forgets: each script is solved from
scratch. The data say what a learning harness has to store instead (see the discussion of 2026-10-03):
- the model does not look for information (739 rewrites against 10 R probes; `replace_entity` 1 in 84), so knowledge
  must be pushed by the harness, and prompt text barely moves a small model;
- after width 3 only 1 of 40 final translations crashes; most lost score is in scripts that run with wrong values,
  concentrated in package semantics (caret, broom, pROC, clock) - **to be recomputed after the precision fix**;
- function-keyed knowledge can reach about half of all calls: 57% of held-out call sites call a function also used in
  a training script (44% in >= 2); 778 distinct functions, the top 100 cover 54%;
- seeds of one script fail repeatedly for the same API fact (9 of 16 scripts).

**Measurement defect found 2026-10-03 (fixed first).** R values were captured with `jsonlite::toJSON`'s default of four
decimal places while the data comparator requires agreement to 1e-6: R `x <- 1/3` was stored as 0.3333 and a correct
Python `x = 1/3` scored 0. Every correct translation of a non-round number failed its data comparison - in all scores
so far, including the held-out experiment, the pattern library's 0.9 admission gate, the dev runs and the replays.
Fixed with `digits = NA` in every R JSON writer (data capture, per-entity checkpoints, env, RNG log;
`tests/test_capture_precision.py`). **Scores before and after are not comparable; analysed script maps cached before
the fix are moved to `work/replay/script_maps_digits4`.**

| # | Step | Purpose / gate |
|---|---|---|
| 1 | Capture precision (`digits = NA`) | **done 2026-10-03** |
| 2 | Recalibrate the generic fingerprints (`fingerprint_null_report.py` on a fresh census) | **done 2026-10-03**: full-precision census (309 scripts); a numeric field is informative with >= 5 values of >= 5 significant digits (`PRECISE_DIGITS`, `MIN_PRECISE_VALUES`): chance-match rate 0.0006 against unrelated objects of other packages (target 1e-3), 608 of 4000 fields admitted; with 4 such values 0.003, integer or low-precision fields ~0.6 (shared datasets, pi, 0/1). The first rule (any non-integer) failed at 0.24. Fields that are not informative are not scored |
| 3 | New baseline: paired replay and seed-only evaluation on the fixed harness | **done 2026-10-04** (`work/seed_eval/baseline_v3.jsonl`, `work/replay_v3/`): seeds (96, gate on) P(runs) 54%, P(>=0.5) 47%, mean 0.373, best of 4 per script 0.642, 3/24 scripts with no seed above 0; replay on all 24 states (start mean 0.495): one loop 0.744 (P(final >= 0.9) 44%, 3.3 steps), width 3 0.834 (54%, 9.9 steps), paired +0.090, SE 0.033, 9/0/15, p = 0.002 |
| 3a | Re-check earlier conclusions with the fixed measurement | **done 2026-10-04, smaller than expected**: the same 20 frozen sources score +0.003 on average after the precision and fingerprint changes (largest: broom 0.555 -> 0.599). Exposure is concentrated: 70 of 309 scripts (23%) capture a value that needs more than four decimals (189 of 461 numeric variables), and few of them are among the dev scripts. Loss analysis unchanged: in the width-3 finals 87% of the lost score is in scripts that run; of 361 entities in the best states 234 reach 0.9, 35 are in 0.7-0.9, 92 below 0.7; below 0.9 by package caret 52, broom 16, clock 13, ggplot2 12, pROC 12, timeDate 8 - the semantic loss is real, not a rounding artefact. Pattern library: its admission gate was affected for the 23% exposed scripts; re-measuring it needs a training run, so it is folded into step 10 |
| 4 | Random-draw shim: R's draws recorded and replayed to Python as inputs, like datasets | **done 2026-10-04**: the R reference run records the draws of `runif rnorm rexp rgamma rbeta rbinom rpois rt rchisq rlnorm rweibull rcauchy rgeom rlogis rnbinom sample sample.int` (wrappers attached ahead of base/stats, not global variables; pass-through, so R's own numbers are unchanged; vectors over 100000 values not recorded). The verifier hands them to the Python run: numpy module-level functions, `default_rng()` Generators (a subclass, so isinstance checks in scipy/sklearn still hold), `random` and `choice`/`sample` are served R's next unused draw of the same family with the same count; a different count or no draw left falls through to the real generator; only calls made from the script are served (numpy/scipy/sklearn draw numbers while importing). `RandomState` instances are not hooked (replacing the class broke sklearn's isinstance check). The RNG effect is no longer scored (it was never active). Checked on real R: translations with `np.random.*` and `default_rng` score 1.0 against `rnorm/runif/sample`, a hard-coded translation 0.25. Dev start sources: caret 0.580 -> 0.691, lava 0.587 -> 0.694, no other change. `tests/test_rng_replay.py`. Scores of scripts that draw random numbers (34 of 316) change; not comparable with earlier runs |
| 5 | Learning-curve instrument (D): knowledge snapshots at 0 / N / 2N translated scripts, held-out packages, paired replay + seed-only evaluation, coverage of held-out call sites | **built and first run 2026-10-04** (`scripts/learning_curve.py`, `tests/test_learning_curve.py`): structured seeds only, order randomised over (snapshot, script, seed), per-entity scores, analysis paired by entity on the entities the final snapshot can inform, cluster bootstrap over scripts, smallest detectable effect reported; other mechanisms join with `--snapshots name=path:n_train`. **First measurement, old library checkpoints (0/64/128/192/256 training scripts, 60 held-out scripts x 2 seeds = 580 scored, 20 errors from two script-level failures): no learning curve.** Mean seed score 0.456 / 0.407 / 0.448 / 0.485 / 0.453, P(runs) 63 / 56 / 62 / 65 / 63%. Script level: slope +0.011 per +100 training scripts [-0.014, +0.037], full - empty -0.003 [-0.071, +0.061], smallest detectable ~0.095. Entity level (36 targetable entities that ran in every snapshot, 23 scripts): 0.759 / 0.771 / 0.740 / 0.772 / 0.763, slope +0.0014 [-0.012, +0.014]. Coverage grows 0 -> 11.8 -> 15.1 -> 16.9 -> 19.6% of held-out entities, so coverage is the limit: even a +0.1 gain on every covered entity would be ~ +0.02 on a script. The old library, as a prompt-text store, bends neither the script nor the entity curve; the instrument can see effects of about 0.07-0.10 and rules out anything larger |
| 6 | Harness-located errors (C): the first R call whose value differs from Python's, reported to the agent | **built and replayed 2026-10-04** (`harness/locate.py`, `HarnessTools.locate`, `reason(locate=)`, replay policy `rewrite_loc`, `tests/test_locate.py`). Every call and operator of the entity is probed in R (parse-tree rewrite) and in Python (AST rewrite), each evaluated once in order so side effects and random draws are untouched; probes are aligned by value (name-free, via the fingerprint matcher), the first R call whose value Python never produces is reported with the nearest Python value. Planted `sd`/`np.std` (n vs n-1) bug located exactly; ~3 s per probe pair; found a note in 83 of 119 attempts. Replay, 24 frozen states x 3 samples, current harness: single loop 0.700 (P(final >= 0.9) 39%, 2.9 steps), with located notes 0.729 (40%, 3.0 steps); paired +0.029, SE 0.025, better/worse/tied 8/2/14, Wilcoxon p = 0.084 - **a lean in the right direction, not significant** (smallest detectable ~0.07 at this size); no extra model calls. Off by default until a larger replay or the training run confirms it. (A first run of this replay was invalidated: the provider ran out of credits and 129 agent calls failed with 402; kept as `work/replay_v4/results_invalid_402.jsonl`.) |
| 7 | Verified R-semantics runtime (A): Python functions reproducing R functions, proposed by the small model, accepted only after differential tests against R on generated inputs; failing inputs kept as tests; functions used by a translation pasted into its output (decided 2026-10-03); pilot first: share that passes validation, paired replay with / without, held-out coverage | knowledge that is executable and validated, pushed by the harness | **pilot built and run 2026-10-05** (`r2py/runtime/difftest.py`, `propose.py`, `scripts/runtime_pilot.py`, `tests/test_runtime_pilot.py`; ~10 minutes, 0 provider failures). Candidates come from the pipeline's data: 9 functions of entities still below 0.9 in the best width-3 states plus the 44 most-called base/stats/utils functions without side effects. Cases come from R: the model lists 8 example calls, R runs them, the harness mutates each first argument (tie, scaled, reversed, single value, NA where R accepts it), R's draws inside package code are recorded and replayed to the Python function; an S3 generic is matched against the method that runs. Gemma writes `def r_<name>(...)` and gets up to 3 counterexample rounds. A correct `quantile` passes 16/16 cases, a wrong one 4/16. **Result: of 43 attempted, 17 (40%) pass every case (7 at round 1, 3 at round 2, 7 at round 3); 26 fail; 9 had no usable cases (side effects, non-pure).** Base/stats frequency set 15/36, failing-entity functions 2/7 (as_hms, createTimeSlices). Passing: as.Date, as_hms, createTimeSlices, mean, median, paste, paste0, rowMeans, rowSums, sort, sub, unique, which, readLines, force, local, Sys.setlocale. Nine failures are near misses (<= 2 failing cases: holidayNYSE 9/10, earlyCloseNYSE 12/13, tolower 15/16, table 25/26, charToRaw 9/10, split 30/32, ...), many on exotic model-proposed inputs where R is idiosyncratic (`tolower(data.frame(...))`, `table(matrix(...))`) - the oracle is sometimes unfair, so 40% understates sane-input capability; seven fail completely: the RNG-driven caret resampling functions (createDataPartition/Folds/Resample: a model bug that shadowed `list`, not fixed in 3 rounds), density, sprintf, filter. Accepted code: `work/runtime/pilot/*.py`. Not yet measured: whether translations improve when they use it. **Second pass 2026-10-05** (the 36 functions that had not passed; ~35 min, 0 provider failures): acceptance now needs every *ordinary-use* case (the most common first-argument class among the model's own example calls; calls of other classes, e.g. `tolower(data.frame(...))`, and their mutants are reported, not required), 3 independent attempts x 5 counterexample rounds, and a hint to reach shadowed builtins through `import builtins`. **33 of 43 now pass (77%): corpus-frequency functions 29/36, failing-entity functions 4/7 (as_hms, createTimeSlices, earlyCloseNYSE, holidayNYSE).** 16 passed for the first time: 6 of them (table, earlyCloseNYSE, expand.grid, filter, structure, options) pass even every exotic case, so those came from more attempts and rounds (13 of the 16 within the first attempt, 3 at round 4-5 or attempt 2); 10 needed the fairer criterion (e.g. holidayNYSE exotic 1/5, rep_len 12/16, as.POSIXct 3/10, tolower 2/4). The two changes are not separable in this design. **Paste-in mechanism built 2026-10-05** (`r2py/runtime/store.py`, `tests/test_runtime_store.py`, `tests/test_runtime_wiring.py`; off unless `runtime_dir` is set in `run_loop` / the manifest's translate config, or replay policy `rewrite_rt`): `RuntimeStore` loads the accepted functions; for a script it finds the functions the R code calls (comments and the script's own definitions excluded; package functions need `pkg::` or `library(pkg)`), lists them with their signatures in the structured seed prompt and in every agent turn, and **the harness owns the code**: a block between `# r2py:runtime:begin` and `# r2py:runtime:end` (after the data shim, before the first entity) is regenerated from the `r_*` names the code references after the seed and after every rewrite, so the model can neither drop nor damage it and the saved file is self-contained. End to end on real R: `median`/`sort` called through the block score 1.0, the same code without it crashes. Coverage with the 33 accepted functions: 8 of 24 dev scripts, 17 of 60 held-out, 43 of 256 training scripts call at least one (most used: paste 8, factor 7, table 6, as.POSIXct 5, as.Date 4, mean 4, charToRaw 4). **First measurement, 2026-10-05: it made translations much worse, and the cause is a flaw in the pilot, not in the idea.** Seed-only, the 8 covered dev scripts, 6 structured seeds each, runtime off vs on (48 seeds each, 0 errors): P(runs) 48% -> 12%, mean seed score 0.355 -> 0.085; blob 0.73 -> 0.00, openssl 0.94 -> 0.00, timeDate 0.48 -> 0.00 (paired -0.27, 0 better / 3 worse / 5 tied). The failures are interface errors (`a bytes-like object is required, not 'str'`, `'datetime.datetime' object is not iterable`, `must be a list of raw vectors`). Cause: the differential tests compare *serialised* values and the prompt showed the model R's results as JSON, so it learned to return the serialised form - the accepted `r_charToRaw` returns a base64 *string* (its own docstring: 'the test environment expects ...'), `r_as_POSIXct` returns ISO strings - and downstream code that needs bytes or datetimes breaks. Goodhart on the oracle's representation: the 33-of-43 pass rate overstated usable functions. The replay of this store was stopped (`work/replay_v5/results_flawed_store.jsonl` kept). **Fixed 2026-10-05**: the model is shown R's class and printed form, told to return the natural Python object, and the runner checks the return type against R's class (raw -> bytes, POSIXct/Date -> datetime/date, difftime -> timedelta, data.frame -> DataFrame, matrix -> 2-d array); a base64-string `charToRaw` now fails, a bytes one passes (`tests/test_runtime_pilot.py`). Pilot rerun into `work/runtime/pilot_v2` (900 s wall-clock cap per function): **29 of 44 attempted pass (66%)**, base/stats 28/37, failing-entity functions 1/7 - lower than the 33 of the serialised-form pilot, as it should be; 9 had no ordinary cases. Seed-only on the 8 covered dev scripts (6 structured seeds each, 0 errors): runtime off P(runs) 48%, mean 0.355; first store 12%, 0.085; **fixed store 46%, 0.333** - the regression is gone (blob 0.67 vs 0.73, openssl 0.98 vs 0.94, timeDate 0.56 vs 0.48, lava 0.45 vs 0.69); paired fixed - off -0.022, SE 0.034, better/worse/tied 2/2/4: **no measurable benefit, and no harm** at this size. The 8 scripts mostly call functions they already handled; the covered functions behind the still-failing entities (caret resampling, holidayNYSE/earlyCloseNYSE as_hms) did not pass the stricter tests. Still failing: the RNG-driven caret resampling functions (createResample 0/31, createFolds 2/13, createDataPartition 4/8 ordinary cases), dist 36/43, seq 9/11, split 26/31, format 12/13, smooth 16/17, example, colnames; no ordinary cases: density, ggroc, zoned_time_info, months, date, with, attach, subset, Sys.sleep |
| 8 | Search -> runtime (B): accepted agent fixes become runtime candidates | the harness learns from its own work |
| 9 | Side fixes: seed `FileNotFoundError` (9 seeds) and `RLexer` import (9), data-shim churn (24% of rewrites), catastrophic rewrites (20%), unrecovered sentinels (40% of drops), mapper JSON failures, fingerprint gaps (XML node sets) | cheap, between runs |
| 10 | Pre-registration of every measurement change (precision, fingerprints, random-draw shim, runtime), then the training run with width, trajectories, model calls per run and the learning mechanisms - the first real learning-curve measurement | |

Not pursued on the evidence: more prompt-based retrieval, MCTS (beam search over restarts = independent width),
more seed styles, entity-level width, seed recombination. Model capability is out of scope by design: the point is to
make a small model (Gemma 4) translate well through knowledge and structure in the harness.

## Where we are, and what comes next

**State.** The first held-out experiment is closed (null, p = 0.0569). The measurement instrument has been
repaired (Stage 0), the agent loop has deterministic gates (shim, argument order, syntax, imports, review),
`replace_entity` and a harness-driven entity-repair mode exist, translations run on Python 3.13, and a
parallel development run (`experiments/dev_run/`) plus smoke-test arms give descriptive numbers. The pattern
library is **frozen**: its script-level ceiling is +0.011..+0.035 while per-script run-to-run noise is
SD 0.22, so one library A/B needs ~440 paired runs.

**What the insights document changed.** It argues that the lever is not the agent interface but what the
loop optimises, how entities are attributed, and how we evaluate. I checked the claims it makes about code
and logs; the verified ones are the basis of Stages 7-11:

| Claim | Check | Result |
|---|---|---|
| A crash forces the aggregate to exactly 0.0 | `stage4/verifier.py:~912` (`if r_bundle.exit_code == 0 and py_bundle.exit_code != 0: aggregate = 0.0`) | **confirmed** |
| About half the agent runs start at 0.000 (9 of 21 and 11 of 21) | regex over the two smoke arms' logs | **confirmed** exactly |
| 16 and 14 of 68 agent rewrites ended in a Python crash; 4 and 8 were 0.0 -> 0.0 ties | same | **confirmed** exactly |
| Best-of-two across the replicate arms 0.752 vs mean single run 0.703 | from `rows.w*.jsonl` | **confirmed** (a rough estimate, not a test) |
| Every verification re-maps entities with an LLM call | `harness/tools.py` `verify()` -> `map_entities_to_lines`, same model and temperature as the translator | **confirmed**; the variance this causes is **not measured** |
| On a tie the agent sees a report from a program that is not the source shown | `agent.py`: `report = new_report if new_report.aggregate == best_score else report`; the prompt shows `best_source` | **confirmed in code**, impact not measured |
| Audit findings disappear after about five steps | `build_agent_turn` keeps the last 5 non-probe history items; findings are `history[0]` | **confirmed in code** |
| A state bank can be built "from the recorded 1,424 training rewrites and the smoke runs" | the logs hold scores and line counts, **not sources** | **not possible from existing data**: states must be logged from new runs (Stage 9) |

**How this fits the earlier plan.**

- It agrees with the 2026-09-29 reassessment: the library is not the lever, and the agent loop (45% of
  rewrites lowering the score) is. It sharpens *why*: much of the "catastrophic" class is the crash cliff,
  not model quality.
- It reframes Stage 3. Entity repair is the right unit of change, but it was built on an objective that
  cannot see progress (a repaired entity that still leaves the script crashing scores 0.0, the same as no
  repair) and on attribution that is re-sampled every step. **The entity-repair A/B now running measures it
  without those two fixes; a weak or negative result there is not evidence against the idea.**
- It replaces "run another full-script A/B" with a cheaper, paired design (Stage 9). Full-script arms
  cannot resolve effects smaller than ~0.13 at 24 scripts.
- It reframes the library question: the successor to "coverage" is symptom-keyed guidance, tested at step
  level (Stage 10), not more per-function patterns.

### Revised priority (supersedes the 2026-09-29 table)

| rank | work | why | stage |
|---|---|---|---|
| 1 | ~~Measure attribution noise: verify one fixed source 5x~~ **done 2026-10-01: large, see Stage 8** | | **8a** |
| 1= | ~~Trajectory log + verification cache~~ **built 2026-10-01** | Without it nothing below can be evaluated cheaply, and today's logs cannot be replayed | **9a-b** |
| 2 | ~~Fix the search objective~~ **built 2026-10-01, not yet evaluated:** tie-branch display bug, shaped objective (official score unchanged) | The loop cannot see progress on a crashing script; ~45% of agent runs start there | **7** |
| 3 | ~~Deterministic entity attribution~~ **8b built 2026-10-01** (8c AST ranges open); LLM mapper as fallback | The unit the score is built on is currently sampled | **8b-c** |
| 4 | ~~State bank + paired replay~~ **built and run 2026-10-02** (entity repair: neutral); compare policies from identical frozen states | Removes the 0.22 between-run SD from policy comparisons | **9c-d** |
| 5 | Entity edit as the default action, observation tools, remaining AST gates, ledger | Only meaningful once 7 and 8 are in | **10** |
| 6 | ~~Width (11d)~~ **built and replayed 2026-10-02: +0.144, p=0.001**; open: entity-level width, recombination, scoped workers | Serial depth saturates (runs end by stalling, not budget) | **11** |
| 7 | Model-object comparability (Phase 1+), pattern-library coverage | Library frozen; adapters are scoped by the excluded-entity worklist | Stage 4, 5-6 |

**Sequencing constraint.** Do not edit `r2py/` while a comparison is running: the two arms must share one
harness. Documentation-only changes are fine.

**What this plan deliberately does not adopt** (from the insights document's own "what not to copy"):
subagent fan-out for exploration, automatic compaction and tool-search deferral (contexts here are ~110
lines), LLM-orchestrated multi-agent systems (about 15x the tokens when a deterministic verifier already
selects), and interactive plan/permission modes. With a 31B open-weight model, harness-driven scheduling
stays the default.

---

## Implementation log

*Chronological record of what was built and measured; the stage sections after it hold the designs.
Statements about "what is not done" in this log are historical; the table above is current.*

**Seed stage, replay and sandbox tripwire (2026-10-02).**
*Why seeds fail* (`scripts/diagnose_seeds.py`: 255 logged seed sources re-verified, no model calls). 34% ran;
structured 43%, bare 26%. Failures: import 22% (`shiny` 22 - not installed in the 3.13 sandbox; R package names such as
`googledrive`, `lava`, `textshaping`), type errors 18% (scikit-learn 1.9 `force_all_finite` vs `factor_analyzer` 12;
data frames handed over as dicts 9), attribute errors 16% (`dict.iloc` 10), syntax 3%. The agent loop's cheap gates
would have flagged only 7 (syntax) + 18 (import) of the 168 failures.
*Fixes:* `shiny`, `diskcache` installed and scikit-learn pinned to 1.7.2 in `.venv-sandbox`; the data shim builds a
DataFrame when a variable is a dict of equal-length column lists (`stitch.build_data_shim`); seed gate
(`seed.seed_problems` / `_corrective_round`: syntax and unresolvable imports get one corrective turn, outcomes counted
in `seed_gate_stats`, drained into run rows).
*Seed-only measurement* (`scripts/seed_eval.py`, 96 seeds = 24 scripts x (2 bare + 2 structured), no agent, both
variants have the env and shim fixes): gate off - P(runs) 50%, P(>=0.5) 44%, mean 0.333, best seed per script mean 0.510,
7/24 scripts with no seed above 0; gate on - 54%, 47%, 0.372, 0.566, 5/24 (93 seeds scored: 3 lost to the sandbox tripwire
below). The gate fired on 10 seeds and fixed 8; the 4-point difference is **inside the noise at n=96** - not shown to
help. The env/shim fixes lifted P(runs) from 34% (old logged seeds, not a paired comparison) to 50%. Structured seeds
gain more (60% vs 50% with the gate), bare seeds are flat. Remaining causes: lxml element types 4, numpy indexing 3,
hard-coded file paths (`FileNotFoundError`) 3, `textshaping` 4 (gate off only).
*Paired replay* (`scripts/replay.py`: best logged seed per script frozen, 20 states with start < 0.9, 2 policies x 3
samples = 120 runs, 0 failed, 0 below the start score): rewrite - mean final 0.651, gain +0.256, P(improve) 58%, P(>=0.9)
23%; entity repair with escalation - 0.657, +0.263, 62%, 20%. Paired difference +0.006, SE 0.034, better/worse/tied
8/5/7, Wilcoxon p = 0.78; SD across samples within a state ~0.11. **Entity repair is neutral.** Most of the gain from either
policy is rescuing zero-score seeds, so the seed stage is the larger lever.
*Sandbox tripwire narrowed:* `snapshot_home` hashed up to 2000 files under the whole home folder, so any edit there
during a run (a file on the Desktop) was blamed on the script (`SandboxEscape`; it cost 3 gate-on seeds). It now watches
only the top level of the project and of `$HOME` plus `R_LIBS_USER` (`isolation._watch_roots`); `work/`, venvs and
the IDE folders are skipped. Tests: `tests/test_stage0_sandbox.py`, `tests/test_seed_stage.py` (shim, gate, summarisers).
Suite: 754 pass, 1 pre-existing failure (`test_stage2 ... locale_dataframe_date_column_round_trip`).
*Agent width (Stage 11d; `harness/agent.reason_wide`, `loop.run_loop(agent_width=)`, `smoke_test.py --width`, replay policy `rewrite_w3`).*
Computed offline from the 120 paired-replay runs, the best of k samples per state gave mean final 0.654 (k=1), 0.726 (2), 0.755
(3), 0.801 (6). Live check: three independent rewrite loops in parallel from the same frozen state, each with its own
harness, the verifier picking the best (20 states x 2 samples, 40 runs, 0 failed, 0 below the start score): mean final
**0.795** against 0.651 for one loop; paired by state +0.144, SE 0.047, better/worse/tied 15/0/5, Wilcoxon p = 0.001; P(improve)
88% against 58%; P(final >= 0.9) 40% against 23%; SD across samples within a state 0.016 against 0.108. This is development
evidence on frozen states, not a pre-registered test, and the selection uses the official score, which the loop can
compute at translation time. Cost: k times the model calls and verifications. Wall time: median 5 min, p90 27 min, max 88 min;
in the longest runs the agent steps took ~4 min; **the rest was the machine in Modern Standby**: the three workers (caret, ggplot2,
googledrive) were silent from ~+17 to +85 min and resumed together at 13:36:56, the minute Kernel-Power logged the exit from
connected standby (event 507). Not width and not the pipeline; `r2py/keepawake.py` (`SetThreadExecutionState`) is now called at the
start of replay, seed_eval, smoke_test and run_heldout. Earlier unexplained multi-hour hangs may have been the same cause. Entity repair vs rewrite from the same states: +0.006, p = 0.78 (neutral). **Width is the first change in this
programme with a clear effect.**
*Entity-level width (Stage 11a; `agent._widen_entity_repair`, `--entity-width`, replay policy `entity_esc_ew3`).* Entity repair with escalation, but
three independent repairs of the failing entity sampled, spliced and verified per step, the best kept. Replay, same 20 states x 2
samples (40 runs, 0 failed): mean final 0.678, P(improve) 75%, P(final >= 0.9) 32%. Paired by state: +0.021 over entity repair without
width (SE 0.033, p = 0.53), +0.027 over the plain rewrite loop (p = 0.12), **-0.117 against whole-loop width 3 (0.795; p = 0.22,
3 better / 6 worse / 11 tied)**. Of 156 widened steps, 49 produced three identical fragments and 31 only two distinct ones (the
samples are not diverse), 8 produced no usable fragment. **Entity-level width is not worth its cost; it stays off by default
(`entity_width = 1`); whole-loop width is the width that works.**
**Default (2026-10-02, decided by the user: 3x model cost accepted):** `DEFAULT_AGENT_WIDTH = 3` in `r2py/loop.py`; `run_loop`, the held-out
pipeline (`cfg.agent_width`) and `smoke_test.py --width` use it. Provider concurrency is workers x 3 requests in flight.
*Deterministic sentinel restoration + pinned audit (2026-10-03; `stage2/sentinel_mapper.restore_sentinels`, `HarnessTools._restored_ranges`, `build_agent_turn(audit_feedback=)`).*
Of 2070 scored rewrites in the replay runs 21% dropped sentinels (then attributed by a sampled model mapping). A dropped sentinel is now put back by
aligning unchanged lines with the source being improved (`note_reference` is also called on every accepted candidate); a model is asked only if an entity still
has no range. On logged sources: 239/239 synthetic drops restored to exactly the original ranges; of 155 real candidates that lost sentinels every entity got
a range back in 93 (60%). Audit findings are pinned in every agent turn instead of scrolling out of the last-5 history. Replay, same 20 states, new harness
against the earlier runs, paired by state: **one loop** (3 samples) mean final 0.722 against 0.651 (+0.071, SE 0.036, p = 0.079; better/worse/tied 10/4/6;
P(improve) 77% against 58%; SD within a state 0.076 against 0.108; 4.0 steps against 3.4). **Width 3** (2 samples) 0.796 against 0.795 (+0.001, p = 0.09 on a
mostly-tied sample): no gain on top of width, which already averages the mapping noise out. Reading: less attribution noise makes the single loop better
(borderline), and the single loop at 4 steps now reaches 0.722 against 0.796 for width 3 at 12.7 steps. The old and new runs were made hours apart; the
design cannot separate the two changes.
*Beam search over restarts (Stage 11e; `harness/beam.py`, replay policy `beam3`: rounds of 3 chains x 4 steps, each round restarting from the best
distinct states found, up to 3 rounds).* Same 20 states x 2 samples (40 runs, 0 failed): mean final 0.779, P(improve) 82%, P(final >= 0.9) 42%,
14.7 model steps per run (3 independent chains: 0.795, 12.8 steps; one loop: 0.651, 3.4 steps). Paired by state: +0.128 over one loop (p = 0.003) but
**-0.017 against independent width 3 (SE 0.018, p = 1.0; 3 better / 3 worse / 14 tied)**. Sharing progress between chains did not help at this
scale; independent chains are as good and simpler. Gain per model step: 0.075 for the first loop, 0.031 for width 3, 0.026 for the beam - the
first loop is by far the most efficient and every extra branch pays about a third as much per call. Search allocation is not the lever; MCTS
would face the same: the verifier is deterministic and the budget is a few tens of expansions.
*Seed width and a third seed style (2026-10-03).* Best of k seeds (mean over 24 scripts; 8 seeds per script: 4 bare + 4 structured, gate on):
k=1 0.380, 2 0.488, 3 0.551, 4 0.591, 6 0.632, 8 0.652; +0.07 per extra seed up to 4, +0.015 beyond - about the efficiency of an extra
agent step (width 3: +0.144 for ~9 extra steps). Within one style best-of-4 is 0.491 (bare) / 0.516 (structured), mixing two of each gives
0.602: the two styles fail on different scripts. Diversity of sources is not the limit (all 40 width-3 first candidates distinct, 22 of 24
seed sets without a duplicate, temperature already 1.0); 3 of 24 scripts still have no seed above 0 after 8. **Third style `planned`**
(bare input; the model writes a `# plan:` line per statement naming the Python call and the R/Python differences; stripped before
verification; `seed.translate(style="planned")`, `n_planned_seeds`, `seed_eval --schedule planned:N`): 96 seeds, P(runs) 55%, P(>=0.5) 43%,
mean 0.347 - the same as bare (0.337), below structured (0.422). Best of 4: planned alone 0.439; 2 bare + 1 structured + 1 planned 0.594 against
0.602 for 2 + 2 structured; at six seeds 2+2+2 0.634 against 3+3 0.633. **It adds no diversity beyond bare and structured**; it stays available,
default 0. Recombination of seeds (11b, `harness/recombine.py`): 72 draws of 4 seeds, changed the result in 2; of 729 entity slots 712 had no
donor that did the entity better by 0.05 (seeds fail on the same entities), so it is dropped.
*Lesson-store pilot (2026-10-02; `r2py/lessons.py`, `scripts/mine_lessons.py`, `seed_eval.py --lessons`).* Crash->fix pairs are
mined from the trajectory logs (a step whose traceback vanished in the next candidate without the score dropping), the model
distils each into a lesson keyed by library, and the seed gate offers the lessons for the libraries a draft imports. Mined
from half the dev scripts (20 pairs, 15 signatures -> 6 lessons: pandas x3, numpy x2, shiny); tested on the other 12 scripts
(48 seeds). Lessons were offered on 32/47 seeds and the revision taken each time. Result: P(runs) 53% vs 56% for the same
scripts without lessons, P(>=0.5) 43% vs 44%, mean 0.381 vs 0.383 - **no effect** at +-7 points. The store is too small and too
generic (the pandas lessons overlap the DataFrame shim); the pilot shows the mechanism runs end to end, not that it helps.
A larger mining run is the real test and is deferred to the full training run.
**Open:** a structured-only or wider seed schedule (P(runs) 60% vs 50%), prompt guidance for the remaining API-misuse
causes, hard-coded file paths in seeds, a paired replay of other agent policies on the same frozen states.

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
**Smoke test (2026-09-29, 12 scripts, 4 workers, `work/smoke/20260929_162051`)** found and fixed:
(1) a request stalled 85 min because the client timeout is per-read -> 420 s wall-clock deadline per
LLM request (likely also the unexplained ~107 min steps); (2) the 4 runtime SyntaxErrors: seeds had
entity sentinels/checkpoints landing inside the data shim, which activation then un-commented (shim now
activated BEFORE checkpoint injection, r2py markers stay comments) plus indented sentinels the runner
did not strip; (3) env still scored 0 on Python-only library side effects (KMP_*, sys_path) -> only
what R changed must be reproduced; (4) tempdir cleanup PermissionError killed a whole script.
Stage 0a answer: 29 of 137 entity records (21%) have NO active dimensions, so they score 1.0 by
construction (55% of all entities scoring exactly 1.0 are vacuous); `executed_ok` was true for all.
`replace_entity` was used 1 of 41 times (refused: multi-span entity). Anti-hardcoding review: 9 passed,
0 failed, 0 unavailable. Shadow fixers: 3 `invalid->valid` saves in 12 scripts. Graphics 0.0 on
ggplot2/pROC/isoband: plotnine plots never render at top level (0 Python pages) -- a translation gap,
not a measurement bug. Agent budget exhausted in 9 of 12 scripts.
**Since then:** Stage 4 Phase 0 done (`ScoreReport.excluded` = R class + Python type of each data
entity left out of scoring; per-run `excluded` rows; adapter worklist in `analyze` and the smoke
summary; checked live: `lm` -> `statsmodels...RegressionResultsWrapper`). Stage 0c done (measurement
note appended to `RESULTS.md`; nothing re-analysed). `scripts/analyze_train_log.py` reproduces the
Measurement table's baseline from the run's files (matches: 1.39 patterns/h, 34% at threshold, 16/39/45%
rewrites, 17% catastrophic, 227 syntax rejections, 84.5% single-example). Note its "scripts
contributing" is 26% (library grew), not the 34% the table lists, which is the gate pass rate.
Shim fixes confirmed live on `caret`/`e1071` (0 runtime SyntaxErrors, previously 3).
**Development re-measure (2026-09-30, `experiments/dev_run/`, unpinned provider, 42 train / 24 held-out,
empty vs full, 1 rep; NOT a registered experiment, results descriptive only).** Training 6-way parallel,
35 min wall. Instrument (Stage 0a): 66 of 420 entity records (16%) have no active dimension (score 1.0 by
construction); `side_effects` never scored 0 (262 active) and was 1.0 for only 49; review failed open 0
times (0 llm_error / parse_error / unavailable). Shadow fixers over 46 runs: **16 valid->invalid**
(the fixers corrupted valid source), 14 valid->valid, only **3 invalid->valid** -> deleting them was right.
Training vs first run: 56 patterns from 42 scripts, 62.5% of scripts added a pattern (was 26%), 45% reached
threshold (was 34%), 54% of compute on scripts that taught nothing (was 91%); BUT 94.6% of patterns hold a
single example (was 84.5%), the plan's dilution signal, at n=56. **Decision gate: targetability 17% (<40%)**,
so per the plan do not spend further scoring runs on the pattern library; primary (9 pairs) empty 0.847 ->
full 0.685, p=0.84, dominated by 2 date_time scripts (-0.81): uninformative. Excluded data entities (15):
8 are R `raw` -> Python `bytes` (a serialiser gap, cheap), rest lxml nodes and joblib caches. Graphics mean
0.13 over 10 scripts. Not measured: agent-action mix (train stdout was not saved to a file).
**Agent-loop follow-ups (2026-09-30):** ProgramData now passes the sandbox env scrub (tinytex runs); R `raw`
serialises as base64 on the Python side (was 8 of 15 excluded entities); translations run on a dedicated
Python 3.13 venv (`.venv-sandbox`, preferred by `find_python`; the syntax gate and the prompt follow it);
every run row carries `agent` stats (actions, per-action outcomes, stop reasons) and parallel workers log to
`<workdir>/logs`; import gate (`stage0/env/module_check.py`: imports that are neither installed nor on PyPI
are rejected before a verification is spent); an altered data-shim block is restored from the best source
(prose inside it was the commonest syntax error); `replace_entity` has an A/B switch
(`smoke_test.py --replace-entity off`, `cfg.replace_entity`). Suite: 706 pass, 1 pre-existing failure.
**replace_entity A/B (2026-09-30, 24 scripts, `empty` library, 20 min budget; arms `work/smoke/20260930_152523`
on, `..._191227` off):** the model chose `replace_entity` once in 84 actions (refused), so the arms differ only
by a prompt paragraph nobody follows and are effectively replicates. Mean 0.723 vs 0.684 (paired diff -0.038,
SE 0.046, p=0.94); **per-script run-to-run SD of the difference is 0.22**, 12 of 24 exact ties, 3 scripts swung
by >0.25 (clock, isoband, pROC). Rewrite-outcome rates moved 10+ points between arms (catastrophic 25% vs 15%,
improved 32% vs 44%), i.e. rates at n=68 carry about +-10 pts of noise; smaller differences cannot be attributed.
Shadow fixers over both arms: 23 valid->invalid vs 5 invalid->valid. Power: detecting a +0.03 script-level effect
at SD 0.22 needs ~440 paired runs (~880 scoring runs, ~30 h wall at 6 workers). **Library decision: freeze**
(see `r2py-experiment-state`): no coverage work, no further library A/B, until the agent loop has a stable
baseline. Queued harness changes: AST-based arg-order repair that reports to the agent; a shim block the model
invents when the best source has none; a harness-driven single-entity repair mode (the model does not pick it).
**Queued harness changes built (2026-09-30):** (1) `stage2/argorder.py` reorders positional-after-keyword call
arguments from the token stream (the source does not parse, so no AST), touching only calls, moving exact source
slices, skipping calls with comments inside; used on agent rewrites (the agent is told) and seeds; replaces the
deleted fixer whose text surgery corrupted valid source. (2) `restore_data_shim` also deletes a shim block the
model invents when none was generated. (3) Entity-repair mode (`cfg.entity_repair`, `smoke_test --entity-repair on`,
default off): the harness picks the first crashed entity, else the lowest-scoring one (single-span, <=2 tries),
asks the model for just that, splices, verifies and gates as usual. First live check, 3 scripts, 8 attempts:
12% improved / 50% unchanged / 0% worse / 38% catastrophic (a repaired entity can still crash the script) -
mechanics work, benefit unproven. Suite: 719 pass, 1 pre-existing failure. **Not done:** an A/B of the new harness
(arm without entity repair vs arm with) on the 24 dev scripts; per-script MDE at n=24 is ~0.13, so judge it on
rewrite-outcome rates and on scripts that swing, not on the mean alone.
**Not done:** Stage 4 Phase 1+ (adapters), Stages 5-6 (gated on the re-measure below), the
RecursionError (needs a traceback from a real run: rows now keep one). Nothing left that can be
built and checked without a real scoring run.
**Superseded status text follows.** Not done (earlier): 0c, Stage 4+. Suite: 674 pass; the 4 pre-existing failures remain.
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

### Revised priority (2026-09-29; **superseded by the table at the top, 2026-10-01**)

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

> **Status 2026-10-01:** `replace_entity` and a harness-driven entity-repair mode (`cfg.entity_repair`) are built.
> The model chose `replace_entity` once in 84 actions, so the harness now schedules the entity itself. Their
> first live check had a 38% catastrophic share, which Stage 7 (crash cliff) and Stage 8 (re-sampled
> attribution) predict; judge the idea after those fixes, by paired replay (Stage 9).

> **Update, 2026-10-01 evening - entity repair on the stabilised harness (sentinel attribution, shaped objective,
> arg-order repair; 24 dev scripts, `empty` library; arms in `work/smoke/`: `..._112951` repair off,
> `..._140509` on with crash-traceback targeting, `..._165951` on with fragment re-indenting and escalation to a
> full rewrite after two failed repairs).** Means 0.710 / 0.695 / 0.694; none differs from `off` beyond noise
> (p = 0.88 / 0.97). Findings: (1) with attribution stabilised the SD of paired per-script differences fell
> from 0.40 to 0.22 once the two entity-repair defects were fixed (the earlier 0.40 was largely those defects);
> (2) targeting by the crash traceback's outermost frame raised the entity-repair improve rate from 19% to 30%;
> (3) a real bug, fragments spliced unindented into a block ("unexpected indent"), and the missing escalation
> were what collapsed `googledrive` and `ggplot2`; with escalation both recover and no script collapses;
> (4) the approaches are complementary (per-script best of `off` and `on` = 0.794) but their sum, as built,
> only matches `off`; (5) **seeds are a lottery**: the same script's best seed differed between arms in 10 of
> the 22 scripts whose agent ran (e.g. isoband 0.861 in two arms, 0.000 in the third), so final-score
> comparisons between arms are contaminated by the seed stage, which the agent change cannot affect. Among the
> 12 scripts with an identical starting state in both arms, escalation vs off is +0.045 (2 wins, 1 loss, 9 ties).
> **Conclusion: entity repair with escalation is neutral on this evidence, not an improvement; the comparison
> that can resolve it starts every policy from the same frozen state (Stage 9c-d, now buildable from the
> trajectory logs, which hold each run's seeds and sources).**

> **Entity-repair A/B result (2026-10-01, earlier, before the stabilising fixes; arms `work/smoke/20261001_065131` off, `..._082137` on; 24 dev scripts,
> `empty` library, new harness in both):** mean 0.731 off vs 0.662 on (paired diff -0.070, SE 0.082, p = 0.64).
> The SD of the paired difference is **0.40**, well above the 0.224 replicate noise, so the treatment itself
> moves scores per script. Split by whether the seed ran: **scripts whose best seed ran (start > 0, n = 11):
> -0.006 (3 wins, 2 losses), no effect; scripts whose seeds all crashed (start = 0.00, n = 11): -0.146 (4 wins,
> 4 losses), with three scripts that full rewrites rescued to 0.90-1.00 (ggplot2, googledrive, hms) staying at 0.**
> Mechanism, read from the logs: on a crashing script an entity repair cannot register progress (the aggregate
> is 0.0 before and after), so each attempt looks like a stall; the model also repeated the same failing
> fragment 3-5 times because import/syntax/review rejections never reach the per-entity notes (only score
> outcomes do). Seed start scores are identical to two decimals across all four arms for most scripts, so the
> variance lives in the agent stage. Same comparison, new harness vs old (X vs the earlier replicate arms):
> syntax rejections 13 / 6 -> 1 (argument-order repair), shim restores 12, mean 0.731 vs 0.723 / 0.684, no
> detectable score change. **Conclusion: do not adopt entity repair as built; it needs Stage 7 (a progress
> signal on crashing scripts) first. Cheap stop-gaps: use it only when the best source runs, and feed every
> rejection reason into the entity notes.**

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

## Stage 7 — fix the search objective

*Added 2026-10-01 from `r2py_harness_insights.md`, insight 1; claims checked against the code and logs.*

**Problem.** `verify()` forces `aggregate = 0.0` whenever R succeeded and Python exited non-zero. The loop
accepts a rewrite only if `aggregate` strictly improves. On a script whose current best crashes, every
crashing candidate therefore looks identical, including one that fixed the first of two crash sites. In the
two replicate arms: 9 of 21 and 11 of 21 agent runs started at 0.000; 16 and 14 of 68 rewrites ended in a
crash; 4 and 8 were 0.0 -> 0.0 ties that strict improvement rejects. `decompose.py` already attributes the
crash to an entity and marks the entities before it as executed, so the data for a gradient exists and the
loop does not use it.

**7a. Show the agent the report that belongs to the source it sees.** After a non-improving rewrite the loop
sets `report = new_report` when the scores tie, but the next prompt shows `best_source`; the review-rejected
branch does the same. The agent then reads comparisons and a traceback produced by a program it cannot see.
Rule: the displayed report always belongs to the displayed source. A rejected candidate's traceback goes into
the history entry (it already does), not into the standing report. Not yet measured; cheap to fix.

**7b. A shaped search value, official score untouched.** Rank candidates by the key
`(runs_to_completion, shaped)` where `runs_to_completion = (python_exit_code == 0)` and
`shaped = aggregate` if it ran, else `mean(entity_score of executed entities) * (executed / total entities)`.
Lexicographic, so a candidate that runs always beats one that crashes (no trading a working translation for
a crashing one). Accept when the key improves; improvement of `shaped` among crashing candidates resets the
stall counter. **Reported scores, the 0.9 pass threshold and every analysis keep using the official
aggregate.** Apply the same key to **seed selection**: today the best seed is chosen by the forced-zero
aggregate, so with four crashing seeds the choice among them is arbitrary.

**Built 2026-10-01 (not yet evaluated):** `harness/objective.py` (`search_key`, `better`); the loop accepts a
candidate when its key improves (review only for candidates that run; shaped progress is recorded as the
outcome `shaped_progress` and noted to the agent), seeds are ranked by the same key, and the displayed report
always belongs to the displayed source (a rejected candidate's per-entity scores go into its history entry).
Tests: `tests/test_search_objective.py` (key ordering and a mocked loop). Evaluate by paired replay (Stage 9d)
and by the smoke arms once 8b is in, comparing P(runs afterwards) from crashing seeds.

**Risks.** (a) A candidate can "reach" more entities by wrapping code in `try/except`; the review gate and
the official score still decide the final result, and it is a visible pattern to gate if it appears.
(b) Shaped progress could keep a doomed script alive; the step cap and wall-clock budget bound it.

**How to judge it.** Not with a full-script A/B (MDE ~0.13). Use Stage 9's paired replay: from frozen
crashing states, compare P(runs afterwards) and the final official score under the old and new acceptance rule.

## Stage 8 — deterministic entity attribution

**Problem.** `HarnessTools.verify` strips sentinels, calls `map_entities_to_lines` (an LLM call with one
retry, at the translator's own model and temperature), re-inserts sentinels and scores. Costs: an extra model
call per verification; a `SentinelMappingError` silently drops scoring to aggregate-only (this switches off
per-entity feedback and entity repair; the fallback was added after a run lost eight steps to it); and
possible score variance on identical source, because entity boundaries decide which checkpoint deltas are
compared.

**8a. Measure first (do before anything else in this stage).** Verify one fixed source five times, for
several scripts; compare per-entity scores and the aggregate. Script: `scripts/attribution_noise.py`.
If the variance is zero, 8b-c is an efficiency and robustness change; if not, it contaminates every
comparison made so far, including the replicate noise floor in this plan.

**8a result (2026-10-01; `scripts/attribution_noise.py`, same source verified repeatedly, unpinned provider):**
the aggregate of an *unchanged* source moved in **4 of 5 scripts** when entity attribution was re-derived by
the model: lava 0.469-0.683 (range 0.21), highr 0.438-0.773, rmarkdown 0.734-0.754, timeDate 0.755-0.762,
lubridate constant (0.804) in one session and 0.438 in another. With the mapping held fixed the aggregate
did not move at all (0 of 5 scripts): the sandbox and comparators are deterministic; the whole noise is the
mapping. Two failure modes sit behind it: different line ranges for the same entities, and **mapping failures**
(the mapper's reply truncates at its token limit and yields invalid JSON), after which verification silently
falls back to aggregate-only scoring (0.438 where the mapped score was 0.773), and each failure costs two
8192-token generations (~7 min). **So per-script scores, the 'replicate noise floor' (SD 0.22) and every
strict-improvement decision the loop made were partly mapping noise.** (The first draft of the fixed-map
condition passed ranges from the annotated source into a clean-source verification; that was a bug in the
script, fixed, and does not affect the variance conclusion.)

**8b built (2026-10-01).** `HarnessTools.verify` reads the mapping off the `# r2py:entity:` sentinels when every
entity mapped by the starting source still has one (`sentinel_mapper.ranges_from_sentinels`, numbered like the
sentinel-free source that verification runs), with no model call; otherwise it falls back to the model mapper,
resampled up to 3 times before dropping to aggregate-only scoring; `sentinel_reuse`, `mapping_ok` and
`mapping_failed` are counted in each run row (`verify_cache`), and the agent is told when sentinels were
dropped. Checked live on the same two sources: lava 0.5757 x5 (was 0.469-0.683), highr 0.7729 x5 (was
0.438-0.773), zero mapping calls. **Consequence: scores produced before this change and after it are not
comparable at the level of single scripts**, and the dev-run arms above carry this noise.

**8b (original design text).** Sentinels the model preserved are authoritative. Add "every `# r2py:entity:` line present, in
order" to the gate list and tell the agent which are missing. Use the preserved sentinels as the mapping
and call the LLM mapper only for entities left without one.

**8c. AST ranges for assignments.** For variable-assignment entities, derive the line range from the AST by
target name (the prompt already requires R variable names to be preserved). Also makes `replace_entity` and
entity repair safer: their splice spans stop depending on a model re-deriving them.

## Stage 9 — evaluation infrastructure: trajectories, cache, state bank, replay

**Problem.** Full-script runs have a per-script SD of 0.22 between replicates; 12 of 24 scripts tie exactly
and 3 swing by more than 0.25. At 24 scripts the smallest detectable mean difference is ~0.13, and
rewrite-outcome rates at n = 68 carry about ±10 points of noise. We keep only aggregates and, for the first
training run, lost the per-step record entirely.

**9a. Trajectory log.** One JSONL record per agent step: script, run id, step, action, prompt hash, the
candidate source, per-entity scores, outcome class, tokens, latency, and the stop reason per run. Also save
the stdout of every run next to its rows (the parallel workers now write `<workdir>/logs`).
**9b. Verification cache** keyed by (script, source hash): identical sources are not re-run; also makes 8a
cheap. No behaviour change; do 9a-b first.

**Built 2026-10-01 (9a-b):** `harness/trajectory.py` writes `<outputs>/trajectories/<script>.jsonl` per run
(run_start, every seed with its source and score, every agent step outcome with the candidate source, action,
per-entity scores, crash text and prompt hash, `accepted`, run_end); `HarnessTools.verify` caches by source hash
within a run (`hit` / `miss` in the run row). No behaviour change besides identical sources scoring identically.

**9c. State bank.** Collect `(script, source, report)` states from *new* runs. **Correction to the insights
document:** it proposes building the bank from the recorded training rewrites and smoke runs, but those logs
contain scores and line counts, not sources, so no state can be reconstructed from them.

**9d. Paired replay.** Compare policies (entity edit vs rewrite, k = 1 vs 3 candidates, shaped vs official
acceptance, triage fragments on or off) by sampling continuations from identical frozen states, paired by
state. Each sample costs one model call and one verification instead of a 20-minute run, and pairing removes
the between-run SD. Frozen states ignore learning across steps, so confirm winners with a small whole-script
run. Metrics: P(improve), P(catastrophic), change in the shaped value, change in the official score.
This is development evidence; it is not a pre-registered test.

## Stage 10 — action space, observation tools, gates, ledger

*Only after Stages 7 and 8: entity edits need a usable gradient and stable spans.*

**10a. Entity edit as the default mutating action after the seed**, full rewrite as the escalation (two
failed entity repairs, or several entities sharing a root cause). The harness already schedules the entity
(`cfg.entity_repair`); this stage decides the default from replay evidence. Note the model chose
`replace_entity` once in 84 actions: do not rely on prompting for it.
**10b. Observation tools.** `inspect(entity, variable)`: R and Python values side by side (head, dtypes,
attributes, NA positions, concise by default), built from the per-entity checkpoint data that is already
captured; `probe_py(expr)` at the state after entity k. Keep the standing prompt to a compact scoreboard and
let the agent pull detail. Expect a modest gain at 110-line scripts (focus, not context length).
**10c. Remaining gates.** AST-checkable rules still living in the prompt: no top-level code wrapped in `def`
(unless R defines a function), preserved variable names, sentinels present (8b), no literal equal to a
captured R output. Each gate names the line and the fix; delete the matching prompt paragraphs. Pin the audit
findings in the standing prompt (they currently scroll out of the last-5 history window after ~5 steps).
**10d. Per-entity ledger and restart-on-stall.** Replace history strings with a record per entity (what R
produces, what was tried in one line, why it failed, best score); on a stall restart the turn from the best
source plus the ledger. Put the changing `## Step n/max` line last so a provider's prefix cache can hit.
**10e. Symptom-keyed guidance (the successor to "coverage").** Verifier output already supports a
deterministic triage: crash (with traceback line), type mismatch, value mismatch beyond tolerance, ordering,
NA handling, stdout format, missing output, graphics page count. Classify each failing entity and load a short
class-specific fragment on demand. Unlike the function-keyed library it does not need to have seen the
function. A hypothesis, tested by replay at step level; if it wins, the "failure -> fix" variant of the
library is its natural successor. (The prompt's stock gotcha catalogue, architecture §3.7, is a small
unlearned version.)
**10f. Non-OpenRouter prompt parity** (whole-file JSON string, no `replace_entity`): low priority, not used
by any recorded run.

## Stage 11 — width and scoped workers

*Only after Stages 7 and 8, and decided by Stage 9's replay.*

Seed width already exists (up to six one-shot translations); agent width does not, and runs end by stalling
(17 and 13 of 24) far more often than by budget (1 and 2), so more serial depth would go unused. Best-of-two
across the replicate arms was 0.752 against a mean single run of 0.703 (12 of 24 ties; suggestive, not a test).
**11a.** Entity-level width: for the chosen failing entity, sample *k* independent repairs, splice and verify
each, keep the best non-regressing one.
**11b.** Recombine per-entity best fragments from seeds that crashed in different places, through the
existing splice machinery; verification arbitrates.
**11c.** A scoped worker: given one entity (R snippet, Python snippet, comparison, traceback line, ledger,
and the tools `inspect`, `probe_r`, `probe_py`, `lookup_docs`) it returns a candidate fragment. The
**harness**, not an LLM, orchestrates: triage, parallel workers, splice, gate, verify, merge non-overlapping
fixes with a bisect on regression. This keeps the ~15x token cost of LLM-orchestrated multi-agent systems
away. The agent loop already *is* a refine agent (RepoTransAgent's ablation: removing the repair loop drops
pass rate 45.8% -> 26.5%, removing context gathering to 32.2%, removing retrieval only to 42.9%, which
supports where effort already went), so this is about focus and width, not a new autonomous agent.
**11d.** Whole-script width against the serial loop at equal token cost, last.

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
| Attribution noise: per-entity score spread on 5 verifications of one source | **unknown** | measured, then 0 | **8a** |
| Agent runs starting at 0.000 / rewrites ending in a crash (smoke arms) | 9-11 of 21 / 14-16 of 68 | ↓ | 7, 10 |
| P(improve), P(catastrophic) from identical frozen states, per policy | not recorded | recorded, paired | **9d** |
| Smallest detectable mean difference, whole-script arms at 24 scripts | ~0.13 | no longer the primary instrument | 9 |

---

## Pre-registration impact

**Addendum 2026-10-01.** Stages 7-11 change the loop's objective, attribution and action space, so no
score from them is comparable with the first experiment, and none of them is pre-registered. They are
evaluated as development work (paired replay, Stage 9). Whatever is carried into the next registered
experiment must be frozen first, and the registration should name the official score (forced-zero
aggregate) as the endpoint regardless of the shaped search value.

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
