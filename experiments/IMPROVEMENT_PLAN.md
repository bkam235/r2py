# Improvement plan — harness and agent loop

> **Revised 2026-10-01** after reading `r2py_harness_insights.md` (a comparison with agentic coding
> harnesses) and checking its claims against the code and the smoke-test logs. The stage list below the
> next section is unchanged history; **new work is Stages 7-11**, ranked in the table that follows.
> The long status paragraphs that used to open this file are now the *Implementation log* further down.

**Training/scoring operations, 2026-10-07 (parallel and resumable).** `run_heldout.py train --workers N` already trained N scripts at once (each against a snapshot of the library taken when it starts, up to N-1 scripts stale; the parent seeds the live library from finished tasks one at a time). The library has shown no measurable effect, so the staleness does not matter for the results; provider load does: each script runs width-3 agent loops, so N workers mean about 3N requests in flight (18 gave `402 in_flight_budget_exhausted` when credits were low; use 4-5). **A provider outage is no longer a result.** A call that fails for good after its retries (credits/402, rate limit, 5xx, network) is recorded (`llm.provider_failures`), `_translate_once` raises `ProviderUnavailable` for a run that saw one, and the drivers discard it: no progress/score row, no attempt counted, nothing taught to the library, the script goes back to the front of the queue, submission pauses, and the driver polls one tiny request every 60 s (`--poll-s`) for up to 6 h (`--max-wait-h`) and carries on by itself once the provider answers; if the wait runs out the command returns exit code 3 and the same command resumes. Before this, a run on an exhausted account came back as a normal row with score ~0 (seeds empty, agent stopped) and was recorded and learned from. Scoring (`score`) has the same protection (`SystemExit(3)` after giving up). Ctrl-C loses only the scripts in flight (rows are appended when a script finishes; the library write follows its row). Events are logged to `train_events.jsonl`. `tests/test_train_resilience.py`.

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
| 7 | Verified R-semantics runtime (A): Python functions reproducing R functions, proposed by the small model, accepted only after differential tests against R on generated inputs; failing inputs kept as tests; functions used by a translation pasted into its output (decided 2026-10-03); pilot first: share that passes validation, paired replay with / without, held-out coverage | knowledge that is executable and validated, pushed by the harness | **pilot built and run 2026-10-05** (`r2py/runtime/difftest.py`, `propose.py`, `scripts/runtime_pilot.py`, `tests/test_runtime_pilot.py`; ~10 minutes, 0 provider failures). Candidates come from the pipeline's data: 9 functions of entities still below 0.9 in the best width-3 states plus the 44 most-called base/stats/utils functions without side effects. Cases come from R: the model lists 8 example calls, R runs them, the harness mutates each first argument (tie, scaled, reversed, single value, NA where R accepts it), R's draws inside package code are recorded and replayed to the Python function; an S3 generic is matched against the method that runs. Gemma writes `def r_<name>(...)` and gets up to 3 counterexample rounds. A correct `quantile` passes 16/16 cases, a wrong one 4/16. **Result: of 43 attempted, 17 (40%) pass every case (7 at round 1, 3 at round 2, 7 at round 3); 26 fail; 9 had no usable cases (side effects, non-pure).** Base/stats frequency set 15/36, failing-entity functions 2/7 (as_hms, createTimeSlices). Passing: as.Date, as_hms, createTimeSlices, mean, median, paste, paste0, rowMeans, rowSums, sort, sub, unique, which, readLines, force, local, Sys.setlocale. Nine failures are near misses (<= 2 failing cases: holidayNYSE 9/10, earlyCloseNYSE 12/13, tolower 15/16, table 25/26, charToRaw 9/10, split 30/32, ...), many on exotic model-proposed inputs where R is idiosyncratic (`tolower(data.frame(...))`, `table(matrix(...))`) - the oracle is sometimes unfair, so 40% understates sane-input capability; seven fail completely: the RNG-driven caret resampling functions (createDataPartition/Folds/Resample: a model bug that shadowed `list`, not fixed in 3 rounds), density, sprintf, filter. Accepted code: `work/runtime/pilot/*.py`. Not yet measured: whether translations improve when they use it. **Second pass 2026-10-05** (the 36 functions that had not passed; ~35 min, 0 provider failures): acceptance now needs every *ordinary-use* case (the most common first-argument class among the model's own example calls; calls of other classes, e.g. `tolower(data.frame(...))`, and their mutants are reported, not required), 3 independent attempts x 5 counterexample rounds, and a hint to reach shadowed builtins through `import builtins`. **33 of 43 now pass (77%): corpus-frequency functions 29/36, failing-entity functions 4/7 (as_hms, createTimeSlices, earlyCloseNYSE, holidayNYSE).** 16 passed for the first time: 6 of them (table, earlyCloseNYSE, expand.grid, filter, structure, options) pass even every exotic case, so those came from more attempts and rounds (13 of the 16 within the first attempt, 3 at round 4-5 or attempt 2); 10 needed the fairer criterion (e.g. holidayNYSE exotic 1/5, rep_len 12/16, as.POSIXct 3/10, tolower 2/4). The two changes are not separable in this design. **Paste-in mechanism built 2026-10-05** (`r2py/runtime/store.py`, `tests/test_runtime_store.py`, `tests/test_runtime_wiring.py`; off unless `runtime_dir` is set in `run_loop` / the manifest's translate config, or replay policy `rewrite_rt`): `RuntimeStore` loads the accepted functions; for a script it finds the functions the R code calls (comments and the script's own definitions excluded; package functions need `pkg::` or `library(pkg)`), lists them with their signatures in the structured seed prompt and in every agent turn, and **the harness owns the code**: a block between `# r2py:runtime:begin` and `# r2py:runtime:end` (after the data shim, before the first entity) is regenerated from the `r_*` names the code references after the seed and after every rewrite, so the model can neither drop nor damage it and the saved file is self-contained. End to end on real R: `median`/`sort` called through the block score 1.0, the same code without it crashes. Coverage with the 33 accepted functions: 8 of 24 dev scripts, 17 of 60 held-out, 43 of 256 training scripts call at least one (most used: paste 8, factor 7, table 6, as.POSIXct 5, as.Date 4, mean 4, charToRaw 4). **First measurement, 2026-10-05: it made translations much worse, and the cause is a flaw in the pilot, not in the idea.** Seed-only, the 8 covered dev scripts, 6 structured seeds each, runtime off vs on (48 seeds each, 0 errors): P(runs) 48% -> 12%, mean seed score 0.355 -> 0.085; blob 0.73 -> 0.00, openssl 0.94 -> 0.00, timeDate 0.48 -> 0.00 (paired -0.27, 0 better / 3 worse / 5 tied). The failures are interface errors (`a bytes-like object is required, not 'str'`, `'datetime.datetime' object is not iterable`, `must be a list of raw vectors`). Cause: the differential tests compare *serialised* values and the prompt showed the model R's results as JSON, so it learned to return the serialised form - the accepted `r_charToRaw` returns a base64 *string* (its own docstring: 'the test environment expects ...'), `r_as_POSIXct` returns ISO strings - and downstream code that needs bytes or datetimes breaks. Goodhart on the oracle's representation: the 33-of-43 pass rate overstated usable functions. The replay of this store was stopped (`work/replay_v5/results_flawed_store.jsonl` kept). **Fixed 2026-10-05**: the model is shown R's class and printed form, told to return the natural Python object, and the runner checks the return type against R's class (raw -> bytes, POSIXct/Date -> datetime/date, difftime -> timedelta, data.frame -> DataFrame, matrix -> 2-d array); a base64-string `charToRaw` now fails, a bytes one passes (`tests/test_runtime_pilot.py`). Pilot rerun into `work/runtime/pilot_v2` (900 s wall-clock cap per function): **29 of 44 attempted pass (66%)**, base/stats 28/37, failing-entity functions 1/7 - lower than the 33 of the serialised-form pilot, as it should be; 9 had no ordinary cases. Seed-only on the 8 covered dev scripts (6 structured seeds each, 0 errors): runtime off P(runs) 48%, mean 0.355; first store 12%, 0.085; **fixed store 46%, 0.333** - the regression is gone (blob 0.67 vs 0.73, openssl 0.98 vs 0.94, timeDate 0.56 vs 0.48, lava 0.45 vs 0.69); paired fixed - off -0.022, SE 0.034, better/worse/tied 2/2/4: **no measurable benefit, and no harm** at this size. **Hard pass on the 9 failing-entity functions, 2026-10-05** (options 1+2: cases mined from the real calls in the scripts - the arguments the script's own environment gives them, plus the draws they consume - and 4 attempts x 8 rounds, 15000 characters of source; ~1 h wall clock including retries after transient connection errors): **createTimeSlices 21/21, as_hms 9/9, earlyCloseNYSE 7/7 pass; holidayNYSE 5/6; createFolds 5/10, createDataPartition 4/9, createResample 0/19 fail; zoned_time_info and ggroc have no testable ordinary cases.** Two oracle defects were found on the way and fixed: a mined call that depends on the clock (`as_hms(Sys.time())`: R's value has microseconds the serialised argument lost) is skipped, and a classed R object serialised as its slots (a timeDate: Data/format/FinCenter) now matches the vector a natural Python return gives (its Data component) - the holidayNYSE/earlyCloseNYSE values were right from the start. The RNG-driven caret functions need caret's stratified-sampling algorithm and stay out of reach. **Seed-only re-measure with the updated store, same 8 scripts, 6 structured seeds each:** first run 38% P(runs), mean 0.297 - timeDate fell from 0.48 to 0.00 in all 6 seeds because the model, told `r_earlyCloseNYSE` exists, wrote `r_holidayNYSE` too (not in the store, a NameError). Guard added: `RuntimeStore.unknown_references` - the seed gate's corrective round and the agent's rewrite gate reject calls to `r_*` names that nothing defines and the store lacks (9 found, 9 fixed in the seed gate). With the guard: **P(runs) 50%, mean 0.378 against 0.355 without the runtime**; timeDate 0.70 against 0.48, others within 0.04; paired +0.023, SE 0.028, better/worse/tied 2/2/4 - no harm, a first small gain on the one script whose function it covers. **Function-level locator in the repair loop** (`r2py/runtime/locate_fn.py`; `runtime_pilot.py hard --locate`; 4 attempts x 8 rounds): the R function's body is rewritten so every call and operator reports its value (each evaluated once, in order, with R's draws; the instrumented function is installed in the namespace and every attached copy), the model's Python is instrumented the same way and run on the same case with R's draws replayed, and the first R value Python never produces is added to each repair message with the nearest Python value. First version: no gain (createDataPartition 4/9, createFolds 4/18, createResample 0/17, holidayNYSE 5/7): the locator reported 'every R value also appears in your Python' because **pooled value matching cannot discriminate index vectors** (small integers occur everywhere). Fix: vectors of two or more values are matched as *sequences*; the same values in another order is reported as an order divergence (`harness/locate.py`, also used by the entity-level locator). On the real caret case it now says: the first step where your Python departs is `dlply(data.frame(y = y, index = seq(along.with = y)), .(y), subsample, p = p)`: R computes [72, 7, 38, 73, ...], your nearest value is [1, 1, 1, 1, 2, 2, ...] - class-local instead of original positions. Second run: **createDataPartition 8/11 ordinary cases (was 4/9), createFolds 9/22 (was 5/10), createResample 0/31; no function passes; holidayNYSE produced no ordinary cases that run** (the model's invented calls differ between runs, so case sets are not identical). The locator makes the failures informative and moves two functions closer, but the caret resampling algorithms (stratified sampling by class, index mapping, fold labelling) are still not reproduced. Inspection of the caret functions before adding a source-lookup tool: createDataPartition 1603 characters of R source, createFolds 1485, createResample 561, and the only own-package helper they call is `prettySeq` - the full source was already in the prompt; source is not what the model lacks. The 8 scripts mostly call functions they already handled; the covered functions behind the still-failing entities (caret resampling, holidayNYSE/earlyCloseNYSE as_hms) did not pass the stricter tests. Still failing: the RNG-driven caret resampling functions (createResample 0/31, createFolds 2/13, createDataPartition 4/8 ordinary cases), dist 36/43, seq 9/11, split 26/31, format 12/13, smooth 16/17, example, colnames; no ordinary cases: density, ggroc, zoned_time_info, months, date, with, attach, subset, Sys.sleep |
| 8 | Search -> runtime (B): accepted agent fixes become runtime candidates | **built and run 2026-10-06** (`r2py/runtime/mine_fixes.py`, `runtime_pilot.py fixes`, `tests/test_mine_fixes.py`): an entity lifted from < 0.7 to >= 0.9 between two consecutive accepted sources of a run is a fix; the R call that keys it, its R text and the Python before/after are read off the trajectory logs (718 logs, 91 distinct fixed (script, entity) pairs, 37 candidate functions not in the store); the fixed fragment goes into the proposal prompt as *evidence* (not as the answer), the real call is mined as a test case, and acceptance is still R's differential tests (6 rounds x 3 attempts, locator on). Result (32 functions tried): 6 pass, 8 fail (auc 11/12, as.POSIXct 10/11, data.frame 14/15, output_format_dependency 8/9, roc 2/37, knit_meta_add 1/20, pluck, tlmgr_search), 13 no testable cases (graphics layers, network, session), 5 R timeouts (googledrive: the network). **Purity gate** added after inspecting the 6: `try`, `suppressPackageStartupMessages`, `tlmgr` 'passed' as vacuous wrappers (control flow, system calls); functions whose body (outside error messages) uses system calls, unevaluated-argument constructs (substitute, match.call, sys.call, eval), error handlers or session state are not candidates (`difftest.IMPURE`, `runtime_pilot.py purity`, the store skips entries with `impure`). It also removes 6 earlier entries (local, options, replicate, smooth, Sys.setlocale, table). Merged into the store: hms::hms, lubridate::floor_date, shiny::httpResponse. Store now 28 pure functions. Seed-only on the 8 covered scripts, v5: P(runs) 50%, mean 0.368 vs 0.355 without the runtime (v4 0.378); paired +0.014, SE 0.035, 1/1/6 - no harm, no measurable gain; the hms script still scores 0 for other reasons |
| 9 | Side fixes: seed `FileNotFoundError` (9 seeds) and `RLexer` import (9), data-shim churn (24% of rewrites), catastrophic rewrites (20%), unrecovered sentinels (40% of drops), mapper JSON failures, fingerprint gaps (XML node sets) | cheap, between runs | **done 2026-10-07, partly**: (a) *FileNotFoundError seeds (12 of 12 are one script, tinytex `tlmgr`)*: the translation shells out to TinyTeX's `tlmgr`, which the sandbox does not have; an environment gap of that script, not a harness defect - left. (b) *Imported names that do not exist* (`from pygments.lexers import RLexer`, `from shiny import http_response`; the installed module imports, the name does not): new generic gate `module_check.missing_import_names` (runs once per (module, name) in the translation interpreter, suggestions from the module and its submodules) in the seed gate's corrective round and in the agent's rewrite gate (`import_name_rejected`). Seed-only, bare 6 + structured 6 per script: shiny P(runs) 25% -> 58% / 83% (two runs; the model stops inventing `http_response`), highr unchanged at ~8% - told that `RLexer` does not exist the model still writes it, because the suggestions (`pygments.lexers.r.RdLexer` ...) do not name `SLexer`; the right name needs API knowledge the harness does not have. (c) *Data-shim churn* (24% of rewrites altered the block): the block is now hidden from the model behind one placeholder comment and restored by the harness after every rewrite (`stitch.hide_data_shim` / `show_data_shim`; the prompts say to keep the line); effect on scores not measured, tests added. (d) *Sentinels the restoration could not recover*: unmatched assignments are anchored by their target name inside the gap between matched lines: every entity recovered in 165 of 256 real candidates (was 157; +3 points). (e) *Catastrophic rewrites (20%)* and *mapper JSON failures at 8192 tokens*: not addressed (no cheap fix; the shaped objective already discards catastrophic rewrites) |
| 10 | Pre-registration of every measurement change (precision, fingerprints, random-draw shim, runtime), then the training run with width, trajectories, model calls per run and the learning mechanisms - the first real learning-curve measurement | |

**Step 10 result (2026-10-07): registered, then withdrawn unrun, and why.** `PREREGISTRATION_3.md` was written and
registered (width 3, locator, runtime store frozen at 28 functions, 5-worker training, scoring `empty`/`half`/`full`),
then withdrawn before any data collection: it would have spent ~15 h of training and ~1 day of scoring to re-measure a
learning mechanism that is unchanged since the null result. Instead the question "what could the library ever reach?"
was answered offline from data already paid for (`scripts/coverage_probe.py`, no LLM calls, no new translations):
entity scores of the first experiment's 164 `empty` runs, the trained library, and a parse-only
(package, function) inventory of the 256 training scripts (`work/coverage_probe/`).

| supply available to retrieval | held-out entities | of the 142.8 lost points |
|---|---|---|
| the library as actually trained (155 patterns) | 20% | **17%** |
| everything in the 85 training scripts that scored >= 0.9 | 23% | 22% |
| everything in all 250 training runs, harvested per entity | 47% | **52%** |
| ... plus the same function name in any package | 47% | 54% |
| ... plus anything at all from the same package (the tier removed in 2026-09) | 85% | 86% |

Two findings, both against the current design:

1. **The ceiling is a harvest problem, not a retrieval problem.** Loosening the key buys ~2 points (52% -> 54%);
   harvesting per entity from *every* run instead of only whole scripts scoring >= 0.9 buys 30 (22% -> 52%). The
   >= 0.9 script gate, not the exact (package, function) key, is what throws the corpus away. 52 held-out entities
   (11.2 lost points, 8%) have no key at all under `pattern_key` and can only be reached by a snippet-level unit.
2. **Where the library did apply, it recovered none of the loss.** On the 100 informable entities, lost points go
   23.9 -> 23.9 from `empty` to `full` (net +0.058 points; 56 of 100 entities move, by up to +-0.46, and the moves
   cancel). Entity-weighted pooling therefore shows 0% recovery where the registered, script-weighted endpoint showed
   +0.038 - the registered effect sits on a few small scripts. Noise over 100 entities excludes recovery above
   roughly 12% of reachable loss. **Diagnostic recomputation on a closed experiment, not a re-analysis of record:
   `RESULTS.md` stands as written.**

So raising coverage multiplies a factor currently measured at zero, and the decision gate of 2026-09-29 ("below ~40%
targetability, do not spend another scoring run on the library") is met on the ceiling but not on the efficacy. The
next test is therefore efficacy, not coverage: an **oracle-library replay** - paired frozen states, `rewrite_w3` with
and without a library holding a verified example of exactly the functions the failing entities call. It is an upper
bound on every retrieval scheme (perfect coverage, perfect retrieval) and costs one replay. If it moves nothing,
retrieved text is finished as a learning mechanism for this model, and the evolving-knowledge path is the verified
runtime (A/B of steps 7-8), which also reaches the ~48% of loss that no training script covers.

**Oracle-library replay (2026-10-07): null, and retrieval work stops here.** The efficacy test proposed above was
run. Preparation: the 265 saved training translations were re-verified per entity offline
(`scripts/reverify_training.py`, 250 scripts, **5 model calls in total** because attribution is read off the saved
sentinels; mean aggregate 0.669 against 0.676 in the original run, the same 85 scripts >= 0.9). 558 of 1,850 entities
verify at >= 0.9 with a usable Python snippet, giving **260 keys against the library's 155**. That revises the ceiling
above: counting only entities whose translation actually verified, a per-entity harvest reaches **31%** of the
held-out loss, not 52% (the 52% counted keys whose translations were wrong).

From that corpus, `scripts/oracle_library.py` built one library per script holding verified examples (<= 3, from other
scripts only) for exactly the functions that script calls: 721 examples over 260 keys, answering 29% of lookups; 15 of
the 20 frozen replay states get >= 1 pattern, 10 get >= 2, 5 get none and serve as a noise control with identical arms.
`replay.py --policies rewrite_w3 rewrite_w3_oracle --samples 3` (120 runs, `work/replay_oracle/`):

| arm | runs | mean final | P(improve) | P(>= 0.9) |
|---|---|---|---|---|
| `rewrite_w3` | 60 | 0.766 | 75% | 40% |
| `rewrite_w3_oracle` | 60 | 0.755 | 75% | 40% |

Paired by state: all 20 states **-0.011** (Wilcoxon p = 0.534, better/worse/tied 3/5/12); the 15 covered states
**-0.010** (SE 0.058, p = 0.441); the 10 states with >= 2 patterns **-0.013**; the 5-state control **-0.013**
(SE 0.116), which is the instrument's noise floor. Entity-level diagnostic
(`scripts/oracle_entity_analysis.py`, from the `per_entity` scores in the trajectory log, computed after seeing the
script-level result): entities that got an example **+0.022** [-0.215, +0.207], recovering 6% of their 22.6 lost
points; entities without one -0.042. Both intervals are wide enough to be uninformative on their own.

**Not a wiring artifact.** With an oracle library the agent prompt carries a 2,456-character pattern section with
four entities' verified examples, where the empty library yields "(no patterns available)" - checked directly through
`_prefetch_patterns` + `format_patterns` on `hms__rd_example__hms_Rd`. (Prompt hashes cannot be used for this check:
the audit section is itself a model call, so the two arms' prompts differ in every state regardless.)

**Where this leaves learning from past translations.** Three independent tests are now null: the registered experiment
(0% of reachable loss recovered, bound ~12%), the lesson store, and an oracle with perfect coverage and perfect
retrieval. The pattern across everything built so far is that **pushing text at the model does not work, while search,
verified executable knowledge and error localisation do** (width 3 +0.09..+0.14; locator +0.029 n.s.; runtime store
no harm). The evolving-harness path is therefore the verified runtime (steps 7-8): its unit is a differential-tested
`r_*` function rather than a suggestive snippet, it needs no retrieval, and it is the only mechanism that can reach
the ~69% of held-out loss no training script's verified entity covers. Open caveat: this replay is underpowered
(+-0.1 at script level) and the oracle is bounded by the corpus, so it bounds what *these* 256 training scripts could
teach, not what an unlimited corpus could.

**Runtime ceiling, step 1 of the runtime pilot (2026-10-07).** `scripts/runtime_ceiling.py`, offline, no model calls:
each held-out entity's loss is attributed to the function that would have to be implemented and that function is
classified in R. (`difftest.impure_calls` cannot be used directly: it returns an empty impure list both for a pure
function and for one R cannot find, so the script runs its own probe - see the open task on that defect.)

| class | entities | lost points | share |
|---|---|---|---|
| candidate (found, closure, no impure call) | 259 | 71.1 | **50%** |
| impure (IO, environment, NSE, error handling) | 97 | 42.3 | 30% |
| not found (uninstalled, S4/R5, local helper) | 54 | 12.3 | 9% |
| graphics / device | 58 | 11.8 | 8% |
| primitive (no R body to read a spec from) | 23 | 4.2 | 3% |

The structural ceiling is 50%, which clears the pre-committed >= 25%. But candidate loss is 52.7 points on *package*
functions against 18.4 on base/stats/utils, and the pilot's measured pass rates are 59% (30/51) for base/stats/utils
and 22% (10/45) for package functions. Discounted by those rates the expected reach is **22.5 points = 16% of the
loss** - the same order as the pattern library's 17%. The criterion did not say whether to discount by
implementability; both readings are recorded here rather than choosing the favourable one. The largest candidates are
`time_add@timechange` (3.79), `tempfile@base` (3.11), `predict@stats` (3.09), `time_subtract@timechange` (2.97),
`page_fillable@bslib` (2.50), `createTimeSlices@caret` (2.41) - mostly package functions with complex semantics, and
`predict` is a generic over model objects that no standalone function can reproduce.

**Why every knowledge-injection mechanism is null: the model does not read the examples**
(`scripts/imitation_probe.py`, from the oracle replay, no new runs). For the 52 entities that had an example in one arm
and not the other, the share of the example's distinctive identifiers (in its Python, absent from the entity's R,
not builtins) that appear in the entity's final Python:

```
example in the prompt : 6.3%
example never shown   : 6.6%   <- chance
difference            : -0.3%      44 of 52 entities unchanged, 3 more similar, 5 less
```

Exactly one entity visibly adopted its example (`holidayNYSE`, recall 21% -> 77%) and its score *fell*, 0.90 -> 0.81.
So the nulls are not about which example is retrieved or how it is keyed: the content never reaches the output. For
context, the agent prompt is ~8,800 characters and the pattern section begins **69% of the way through it**, after the
R source, the whole current translation, the verification result, the entity list and the data variables, introduced
by a soft "use ... to inform your rewrite".

**Working hypothesis, consistent with everything measured so far:** this model acts on information *about the code in
front of it* - a diverging value (locator +0.029), a missing import, a syntax error, a crash - and not on *analogies
it has to transfer* (library, lessons, oracle: all null). Width works because it is more attempts, not more reading.
The next tests separate "the examples are useless" from "the behaviour is broken": (1) mechanically substitute an
example into its entity and re-verify - no model calls at all, so it is nearly free, and it bounds whether the content
helps when it *is* used; (2) only if that is positive, make the knowledge about the code in front of the model
(example rewritten into the script's own variable names, placed last, as a required edit) and re-run the paired replay.

**Why package functions fail (same day, all offline).** Decomposing the pilot's attempts by best result per
function: base/stats/utils (49 functions) 61% passed, 12% within 80% of their core cases, 8% clearly wrong, 18% never
tested; **package functions (34) 21% passed, 9% near, 21% wrong, 50% never tested** (`no_cases`: R accepted fewer than
three of the proposed calls). So the dominant obstacle for package functions is **getting three valid test cases**,
not implementing them. Two things that might have been the lever are already in place and are not: the model is shown
the function's R source (`propose.SOURCE_LIMIT` 6000, 15000 in the pilot) and 49% of all held-out loss is on candidate
functions whose whole R source is <= 6000 characters (68.7 of 71.1 points are <= 2000); and real calls are already
mined from the target script (`difftest.mine_cases`; 4 of the 10 package passes used mined cases).

Corpus-wide mining will not fix it, because **the loss is in the long tail**: scripts in the 3,988-script corpus
containing a call to the biggest candidates - `time_add@timechange` 1, `createTimeSlices@caret` 1,
`time_subtract@timechange` 1, `ggroc@pROC` 2, `font_feature@systemfonts` 2, `page_fillable@bslib` 5 - while the
recurring ones (`matrix` 116, `tempfile` 73) are base functions that mostly pass already. Cases for the tail have to
come from R rather than from our corpus: every exported function ships an Rd examples block, and the harness can
already intercept calls in a whole R namespace (`difftest._R_INTERCEPT_RNG`). Measuring the yield of
"run the package's own examples, record the real calls" on the top-loss functions is free and is the next step for
coverage.

**What keeps the model from using knowledge: the unit, not the prompt (2026-10-07, two free measurements).**

*Mechanical substitution* (`scripts/substitution_probe.py`, 51 substitutions over 15 frozen states, no model calls):
each oracle example was pasted into its own entity, keeping the sentinels, and the result verified.

```
entity worse (stopped running)  22      mean entity score     0.496 -> 0.143
entity unchanged                21      mean script aggregate 0.431 -> 0.101
entity worse                     6
entity better                    2
```

Restricted to the 45 substitutions where the example was for the entity's **own** (package, function) key, not just
a base-R call inside it: 2 better, 19 unchanged, 24 worse.

**This instrument is invalid as a test of the examples' content, and the positive control is what showed it.**
Substituting the *same entity's own code taken from a run that scored it 1.0* - a correct translation of that very
statement, in that script's own variable names - behaves the same way: 48 substitutions, 29 unchanged, 13 stopped
running, 3 worse, 3 better, mean entity score 0.237 -> 0.057 (`--source self`). An entity's code depends on the rest
of its program (earlier imports, helper definitions, names), so splicing lines between two programs breaks the
program whatever their quality. Nothing about the usefulness of example *content* can be read off either run, and the
earlier claim that examples "are not drop-in usable" stands only in the narrow sense that the harness cannot paste
them in - not as evidence that their content is worthless.

*Does the model call a pasted verified function?* (existing `rewrite_rt` trajectories, `work/replay_v5/`, the older
store.) Five runs had sources and 8 opportunities between them - an entity whose R call matches a store function -
and the model called the `r_*` function in **8 of 8**, already in its first rewrite:
`r_charToRaw`, `r_createTimeSlices`, `r_sort`, `r_table`, `r_factor`, `r_as_POSIXct`, `r_as_hms`, `r_expand_grid`.
Small sample and an old store, and being called is not the same as scoring better (the `rewrite_rt` replay remains
inconclusive), but it is the opposite of the examples' chance-level adoption.

**Was the model ignoring the examples because they were unrelated?** Asked 2026-10-07 after the matplotlib case
above, and answered no, from the same runs (`imitation_probe.py`, stratified; no new runs). 43 of 52 entities got an
example of **their own function**, median R-statement relatedness (identifier Jaccard between the two R statements)
0.33, 29 of 52 at or above 0.3. The difference between arms is zero in every stratum:

| stratum | n | shown | not shown | difference |
|---|---|---|---|---|
| all entities | 52 | 6.3% | 6.6% | -0.3% |
| example for the entity's own function | 43 | 7.0% | 7.3% | -0.3% |
| example only for a base-R call inside | 9 | 3.0% | 3.1% | -0.1% |
| R statements related (Jaccard >= 0.3) | 29 | 9.7% | 10.2% | -0.5% |
| **own function AND related** | **27** | **10.4%** | **10.9%** | **-0.5%** |

Absolute recall rises with relatedness, which is mechanical (a related example shares more identifiers with the R, so
an independent translation coincides with it more often); the arm difference does not. A second, independent measure
agrees: of the library calls the example used (`np.quantile`, `pd.to_datetime`, ...), 14.3% appear in the output when
the example is shown and 16.8% when it is not (n = 43, 3 entities adopted a shown call, 4 the opposite). The
distinctive-token sets are not small enough for this to be noise (median 15 unrelated, 18 related).

So retrieval relatedness is **not** the explanation: the matplotlib case was real but atypical. What remains open is
narrower: the examples may have been related yet not have contained the fact the entity was missing. That is testable
and is the next step - a **one-step paired A/B**: for entities a frozen state scores below 1.0 and for which some run
scored 1.0, show the model the correct translation *of that very statement, in the script's own variable names* as the
example, ask for a single rewrite, and measure whether the rewrite adopts it. One model call per arm per case (~290
calls, far cheaper than a full replay) and it isolates behaviour from search dynamics.

**Conclusion so far.** The obstacle is not prompt position, framing, attention or retrieval relatedness. What is
established: the model does not adopt examples of its own function from other scripts, and it does call a pasted,
self-contained verified `r_*` function on sight (8 of 8). The two dimensions separate: *coverage* (how to verify
functions for the long tail, where half of package attempts never get three test cases) and *behaviour*, which is
solved for callable units and, for analogical ones, has one test left before it is called unsolvable.

**Prompt-treatment experiment with a model control (2026-10-08, `scripts/prompt_arms.py`).** 37 cases (a frozen
state plus one entity it gets wrong, 14 scripts), content held fixed at the strongest value - the correct Python for
that very entity from a run that scored it 1.0 - and only the presentation varied; one model call per case per arm,
the action applied through the harness and verified. Gemma 4 31B and Haiku 4.5 as a control for the model factor
(Haiku is an instrument here, not a candidate translator). 294 calls, no provider failures.

| model | arm | n paired | score vs control | adoption vs control |
|---|---|---|---|---|
| Gemma | library section | 32 | **+0.099** [-0.076, +0.263] p = 0.21 | +0.3% |
| Gemma | imperative, last in prompt | 32 | +0.017 [-0.140, +0.168] p = 0.85 | -0.4% |
| Gemma | imperative + one-entity answer | 30 | +0.058 [-0.098, +0.218] p = 0.44 | **+7.8%** |
| Haiku | library section | 18 | +0.010 [-0.224, +0.236] p = 0.86 | -3.4% |
| Haiku | imperative, last in prompt | 22 | -0.039 [-0.252, +0.161] p = 0.63 | +3.0% |
| Haiku | imperative + one-entity answer | 21 | +0.032 [-0.194, +0.257] p = 0.94 | **+6.9%** |

1. **No presentation moves the score significantly for either model**, even with content that *is* the answer. Every
   interval spans zero and is about +-0.2 wide: this run decides the adoption question, not the score question.
2. **The one lever that works is the same in both models: restricting the action.** Demanding a single-entity answer
   raises adoption by 7.8 points (Gemma) and 6.9 (Haiku). Position and imperative framing move adoption by less
   than a point. So where guidance *is* used, it is because the model was not asked to regenerate the whole file.
3. **Information-seeking is model-bound, not harness-bound.** Of 148 runs, Haiku answered with `probe_r` or
   `lookup_docs` instead of rewriting in 39 (26%), Gemma in 10 (7%); only 8 and 2 were truly unparsable. The claim
   from 2026-10-03 that "the model does not look for information" is a fact about Gemma, not about the prompt.
4. **Consequence: this rig is the wrong instrument for Haiku.** A single step truncates its investigate-then-fix
   strategy, so its arms are conditioned on "chose to rewrite immediately" (n = 18-22 of 37) and its score effects
   are not comparable with Gemma's. A fair Haiku comparison needs up to three steps.

Next, in order: (a) power up Gemma's `library` and `entity_only` arms to 3 samples (n about 90-100, interval about
+-0.1) before anything is built on +0.099; (b) only then swap the content from the correct translation to what a real
mechanism can produce - the recorded real calls of that function with their evaluated arguments and R's returns.
If perfect content cannot move the score, recorded content will not either.

**Correction to the table above, found 2026-10-08 by splitting the cases by how much content the guidance
actually held.** 16 of the 37 cases hand the model 0-1 real code lines: a comment ("# (No-op in Python)"), or a `def`
line truncated at the sentinel boundary with no body ("def pluck(x, key, index, subkey):"). The donor code is cut
from sentinel ranges, which do not always enclose a complete construct, so in 43% of cases the "silver plate" was
empty or malformed. Split on that (n per cell 6-18, so directional):

| model | guidance | library | imperative | entity_only | adoption, entity_only vs control |
|---|---|---|---|---|---|
| Gemma | >= 2 real code lines | -0.020 | +0.057 | +0.007 | **23.4% vs 3.9%** |
| Gemma | 0-1 lines | +0.252 | -0.034 | +0.116 | 0.0% vs 5.6% |
| Haiku | >= 2 real code lines | **+0.107** | +0.076 | **+0.111** | 30.8% vs 21.1% |
| Haiku | 0-1 lines | -0.143 | -0.286 | -0.167 | 0.0% vs 0.0% |

1. **Gemma's pooled +0.099 is an artifact**: it comes from the cases where the guidance was trivial, i.e. where it
   cannot have caused anything. On real guidance Gemma is flat (-0.020).
2. **Haiku gains about +0.1 from real guidance in all three arms** - and loses 0.14 to 0.29 when handed a broken
   fragment. Bad guidance is worse than none.
3. **Gemma copies the guidance when the action is restricted (3.9% -> 23.4% adoption) and still gains no score.**
   Compliance is not the bottleneck for Gemma; the surrounding program is. A correct statement inside an otherwise
   wrong 137-line file does not score, which is the same fact as the crash cliff (42% of training loss is entities
   that did not execute) and the same fact the substitution probe ran into.

**Implication.** The unit of value is the whole program, not the statement, so knowledge must arrive in a form that
does not depend on the rest of the program being right. A self-contained callable function is such a form (called
8 of 8 when available); a statement-level example is not, however correct it is. Before any power-up run, case
construction has to require complete, non-trivial donor code.

**Clean rerun with usable cases only, and the failure diagnosis (2026-10-08).** Case selection now requires a
donor snippet that dedents and parses on its own and holds >= 2 real code lines (`usable_guidance`): 37 cases become
**21** over 9 scripts, median 4 code lines. Arms `none` and `entity_only`, both models, 2 samples, 168 calls, no
provider failures; every run saves its produced source and why the entity scored what it did.

| model | n paired | control -> entity_only | p | adoption |
|---|---|---|---|---|
| Gemma | 32 | 0.609 -> 0.608 (**-0.001**) | 0.81 | 0.3% -> **11.7%** |
| Haiku | 23 | 0.510 -> 0.617 (+0.107) | 0.33 | 15.1% -> 13.1% |

Gemma copies the guidance when the action is restricted and gains **nothing**. Haiku's +0.107 comes with *no* rise in
adoption, so it is not an effect of copying the guidance, and at p = 0.33 it is most likely noise.

**The diagnosis, which is not what was predicted.** Of the 15 runs that demonstrably used the guidance
(adoption >= 50%), **9 took the entity to 1.0** and the group mean went 0.564 -> 0.775: guidance that is actually used
helps a lot (selection caveat: adoption is not randomly assigned). The 6 that used it and still failed break down as
3 "ran, but values still differ", 2 "entity did not execute", 1 "program crashed in another entity" - so the
"surrounding program is broken" story explains 1 of 6, not the bulk. What the feedback actually shows is
**side-effect mismatch in context**:

```
blob    gemma   0.50 -> 0.50   stdout: R printed '' but Python printed '<blob[2...'
months  gemma   0.51 -> 0.73   stdout: R printed '' but Python printed '[datetime...'
x_3     haiku   0.56 -> 0.00   stdout: R printed '' but Python printed '<zoned_...'
as.POSIXct haiku 0.00 -> 0.00  files:  R wrote no files but Python wrote some
```

The snippet is correct *as a statement* and wrong *as a statement in this position*: in its source script the call
sat at top level, where R auto-prints, so the example carries a print; in the target the same call is an assignment,
where R prints nothing. The extra line scores 0 on stdout. This is a mechanical, harness-fixable mismatch (normalise
a snippet's printing and file side effects to the target position) rather than something a model must infer - and it
is a much narrower notion of "adapting to context" than the one considered earlier.

**So the two live problems are now separate and both concrete:** (1) Gemma adopts guidance only 12% of the time even
when the action is restricted to a single entity; (2) when guidance *is* adopted, roughly 40% of the remaining
failures are auto-print/file side-effect mismatches introduced by the snippet's original position.

**Output side effects, sized on the whole training corpus (2026-10-08).** The re-verification pass was repeated with
per-entity comparison feedback recorded (`scripts/reverify_training.py`, `work/reverify/rows_v2.jsonl`, 247 scripts,
1,672 entities, 613.4 lost points, no model calls). Every output class is strongly one-directional:

| class | items | dominant direction |
|---|---|---|
| stdout | 1,283 | 885 (69%) "R printed '' but Python printed ..." |
| files | 885 | 804 (91%) "R wrote no files but Python wrote some" |
| graphics | 273 | 145 R drew figures and Python drew none; only 4 the reverse |

Loss on entities that are *otherwise* correct and lose only on output:

- only complaints are output **Python produced and R did not** (stray prints, stray files): **125 entities, 50.1
  points, 8% of all loss**. This is the deterministically fixable class: R's reference run already records, per
  entity, whether that statement printed or wrote anything.
- only complaints are output side effects of any kind, including mixed directions: 302 entities, 110.1 points, 18%.
- only complaint is a figure R drew and Python did not: **0 entities** - a missing plot never comes alone, so
  graphics cannot be fixed by normalisation; it travels with other failures.

So normalising stray output is worth up to 8% of the loss (50 points), it needs no model cooperation, and the signal
it needs is already captured. It is not a snippet-delivery artifact: these 134 runs include the no-guidance controls.
Caveat from the shadow auto-fixers (16 valid -> invalid against 3 invalid -> valid): any such normaliser is measured
on the paired instruments before it is trusted, and the 8% is an upper bound that assumes a perfect fix.

**Rd-example harvesting: the long tail does have test cases (2026-10-08, `scripts/rd_harvest.py`).** For each
target function the probe loads its package, replaces the function in its own namespace and in the attached package
environment with a recorder, runs the package's own `\examples` block statement by statement under `try`, and keeps
every call whose arguments and return value serialise. No model calls; 0.6-3 s per function.

Top 15 candidate functions by held-out loss:

| function | distinct cases | | function | distinct cases |
|---|---|---|---|---|
| time_add@timechange | **38** | | createTimeSlices@caret | **7** |
| timeDate@timeDate | **17** | | matrix@base | 3 |
| time_subtract@timechange | **16** | | charToRaw@base | 3 |
| time_update@timechange | **12** | | font_feature@systemfonts | 2 |
| ggroc@pROC | **7** | | auc@pROC | 2 |

**8 of 15 reach the three distinct cases `propose.attempt` needs, covering 17.8 of the 32.9 targeted points (54% of
the targeted loss, 12% of all held-out loss).** The wins are exactly the functions corpus mining cannot reach:
`time_add` appears in **one** script in the 3,988-script corpus and its own examples yield 38 cases;
`createTimeSlices`, which defeated the pilot twice, yields 7 real calls with real arguments.

What stays out of reach: `predict@stats` and `augment@broom` (generics over fitted models - no examples recorded, the
arguments are model objects that do not serialise), `drive_create@googledrive` (examples need authentication, so they
sit in `\dontrun`), and functions whose Rd examples are one line (`tempfile`, `page_fillable`).

This is the missing input for the runtime path: the pilot's dominant failure for package functions was `no_cases`
(50% of attempts), and for more than half of the targeted loss that is now fixable from R itself rather than from our
corpus. Next: feed the harvested cases to `propose.attempt` for those 8 functions and count how many produce a
*verified* implementation - the first test of the pilot's 22% package pass rate under decent cases.

**Rd-harvested cases through `propose.attempt` (2026-10-08, `scripts/rd_pilot.py`, 8 functions, 4 workers,
1800 s budget each, locator on).** Case supply was the problem; it was not the only problem.

| function | status | core cases | rounds | held-out loss |
|---|---|---|---|---|
| createTimeSlices@caret | **passed** | 32/32 | 2 | 2.41 |
| charToRaw@base | **passed** | 13/13 | 7 | 2.25 |
| matrix@base | **passed** | 28/28 | 2 | 1.50 |
| ~~ggroc@pROC~~ | *void* | 7/7 | 4 | 2.00 |
| time_subtract@timechange | failed | 20/23 | 6 | 2.97 |
| timeDate@timeDate | failed | 19/24 | 6 | 1.50 |
| time_update@timechange | failed | 13/18 | 8 | 1.38 |
| time_add@timechange | failed | 12/28 | 8 | 3.79 |

**`ggroc`'s pass is discarded.** All 8 of its cases have a `roc` object as first argument, which the R serialiser
does not reject but *fingerprints* (`__r2py_fp__`), so the model's function was handed a hash of a model and
"passed" vacuously - the trap predicted when probing `predict`. `rd_harvest` now drops any case with a fingerprint
argument (10 of 113 harvested cases, all in pROC).

Honest scoring: **3 of 7 usable functions passed, 6.16 points = 4.3% of all held-out loss.** Of the five *package*
functions with usable cases only `createTimeSlices` passed - 20%, no better than the pilot's old 22% - but
`createTimeSlices` is the function that had failed twice at 8/11 and 9/22 with invented calls and now passes 32/32.
So harvesting removed the `no_cases` barrier (all five got real cases) without removing the implementation barrier.

**What the failures are is specific and consistent:** the Rd examples exist to demonstrate edge behaviour, so the
harvested cases are the hard ones. Every timechange failure is a rolling rule -
`time_add(x, hour = 1, minute = 50, roll_dst = ...)` expected `01:52`, got `02:52` (a DST spring-forward boundary);
`time_update(time, month = 2, mday = 31, roll_month = ...)` expected `2015-03-01`, got `2015-03-03`. Three of the
four failures are near misses (20/23, 19/24, 13/18) that yield nothing under all-core-cases acceptance.

So the next question for the runtime path is the **acceptance rule and the repair loop**, not case supply: whether
targeted repair on the one failing rolling rule (the locator already ran) closes 83% to 100%, and whether a function
that is right on everything except one documented edge rule is worth admitting with its failing inputs recorded.

**Regime-restricted admission (2026-10-08, `scripts/regime_admit.py`, `tests/test_regime_admit.py`).** A near-miss
function can be admitted with the option values it fails on fenced behind a guard that raises
`NotImplementedError` instead of guessing; the runtime store loads such entries (`status passed_restricted`) and the
translator is told the exception. The fence rule took three tries, each caught by printing what it fenced:

1. fencing every scalar keyword in a failing call also fenced `hour = 1`, `minute = 50`, `month = 2` - numeric
   *inputs*, so the function would have refused every February. **Numeric amounts are never fenced.**
2. fencing only option values that never pass rejected `time_add`, which is right with `roll_dst = "pre"` until a
   call crosses a DST boundary. **An option value that fails on some inputs is unverified, and is fenced.**
3. the check ran only on the Rd cases, which are scalar - but the pilot had *recorded* vectorisation failures for
   `time_subtract` and `time_update` (R returns 3 values, Python 1). **Every recorded failure must be covered by the
   fence, or the function is not admitted**; vectorisation is a bug, not a regime.

And the pilot record itself was incomplete: `propose` saved only the first five failures (`res.failures[:5]`), and
`time_add` had sixteen - including, by arithmetic, all eight of the model-invented cases, which is exactly where its
siblings' vectorisation bugs were. Admission now refuses any incomplete record, and `propose` keeps every failure
(up to 60) plus `n_failures`.

| function | verdict |
|---|---|
| time_add | record incomplete (5 of 16): re-run |
| time_subtract | vectorisation failures outside the fence |
| time_update | vectorisation, NA and negative-second failures outside the fence |
| timeDate | value failures with no option value |

**Admitted today: none**, and that is the correct outcome - every one would have shipped a known or unknown wrong
case. Only fenced DST/month rolling is a regime; the rest is repair work. Full suite 913 passed, 12 skipped, the one
pre-existing `test_stage2` locale failure.

**Compiled-source experiment (2026-10-09, `scripts/csource_pilot.py`).** `time_add`, `time_subtract` and
`time_update` are ~1,600-character R wrappers around `.Call(_timechange_C_time_add/_update)`; the rolling rules are in
C++. Arm `with_cpp` added the routine (193 / 261 lines from `src/update.cpp`), the `RollDST`/`RollMonth` enums and the
DST resolver `civil_lookup_to_posix` (`src/common.*`), and cctz's `civil_lookup` struct with its worked example
(17.7-20.9 KB per hint; source: CRAN `timechange_0.4.0.tar.gz`, 103,966 bytes, `src/` read as text, never compiled).
Same Rd cases, one run per arm, every failure recorded:

| function | arm | core | failures: rolling rule / vectorisation / other |
|---|---|---|---|
| time_add | r_only | 17/30 | 8 / 5 / 0 |
| time_add | with_cpp | 21/30 | 8 / 1 / 0 |
| time_subtract | r_only | 15/19 | 0 / 1 / 4 (array truth-value errors) |
| time_subtract | with_cpp | 17/23 | 5 / 0 / 1 |
| time_update | r_only | 15/20 | 2 / 1 / 2 |
| time_update | with_cpp | **18/20** | **0** / 1 / 1 (return type) |

1. **The C++ fixed `time_update`'s month rolling (2 -> 0)** and its NA/minute errors; it now fails only two
   model-invented cases (one vector input, one return type).
2. **It did not fix `time_add`'s DST rolling (8 -> 8), and the failures say exactly why.** In every DST case Python
   returns the *same* time whatever `roll_dst` says - `02:52:03` where R gives 01:52 (pre), 03:00 (boundary) or
   03:52 (post). On 2010-03-14 in Chicago 02:xx does not exist: the code does naive local arithmetic, lands in the
   spring-forward gap without noticing, and its `roll_dst` branch never runs. The C++ says what to do with a
   SKIPPED civil time; nothing in Python *tells* the code a time was skipped, and `zoneinfo` has no lookup call -
   detecting a gap takes a fold-and-offset round trip the model did not write.
3. **It helped vectorisation** (`time_add` 5 -> 1): the C++ loops over elements explicitly.
4. **Run-to-run variance is large**: `time_subtract` got its one Rd DST case right without the C++ this time and
   wrong with it. One run per arm cannot rank arms on that case.

No function is admissible: every one fails at least one case with no option value to fence (vector input, return
type, NA), which is a bug. (Fixed in passing: `regime_admit` reported "passes every Rd case already" without checking
the pilot's other recorded failures.)

**What this points to is a verified primitive, not more context.** Everything in timechange goes through one
operation - cctz's `lookup(civil_second) -> {kind, pre, trans, post}` - and the C++ is a set of branches on its
result. A verified Python `civil_lookup(tz, y, m, d, H, M, S)` (differential-tested against R on DST gaps and
overlaps) would let the model translate the branching it can now read, on top of a primitive it cannot get right
alone - and the same primitive serves `force_tz`, `floor_date`, `update`, `round_date`. That is composition one level
down: verify the shared primitive once, then the functions built on it.

**Backlog (user, 2026-10-09): inter-script versus intra-script improvement.** If knowledge learned in one script
does not recur in others (flat recurrence curves), the harness cannot get much better *globally*, across scripts - but
that does not mean it cannot get better *within* a script, inside the agent loop. If the focus moves intra-script, it
will rely less on recorded knowledge and much more on verification, lookup and tools that work out automatically how a
package function behaves (probing R, harvesting a function's own examples, locating the first diverging call).

**Measurement bug: the data-shim sidecar counted as a file the program wrote (found and fixed 2026-10-09).**
`PySandbox.run` took its files snapshot *before* staging sidecar files, so every script with a data shim "wrote" its
own `<stem>.r2py_data.json` and drew "R wrote no files but Python wrote some" (the `_r2py_` prefix filter does not
match a sidecar name). Fixed by staging sidecars before the snapshot (`tests/test_sidecar_files.py`; both tests fail on
the old code). Re-verifying the 250 training translations (`rows_v3.jsonl`): those complaints fall **774 -> 45**, but
the loss does not move (599.6 -> 600.4 points; mean aggregate 0.674 -> 0.671, 24 scripts up, 8 down). Entity scores
mostly do not use the files effect; the damage was to the **feedback**: since the shim was introduced the agent has
been told about a phantom file write on hundreds of entities - sometimes as the *only* message on an entity that
lost points for another, unexplained reason (`data` entities scoring 0 on every dimension). Scores before and after
are comparable; agent feedback is not. The stray-output estimate above (8%) included this artifact.

**Recurrence curves (2026-10-09, `scripts/recurrence_curves.py`, no model calls).** The question: does what one
translation could teach recur in the next? Experience = the first N of 183 training scripts (20 random orders, mean
[min-max]); evaluation = the last 64 training scripts, and the real held-out loss for the function curve. On the
corrected `rows_v3`:

| N scripts | 8 | 16 | 32 | 64 | 128 | 183 / 247 |
|---|---|---|---|---|---|---|
| function, held-out loss reachable | 3.3% | 5.8% | 9.2% | 13.8% | 19.2% | 25.1% |
| ... discounted by measured pass rates | 1.5% | 2.6% | 4.0% | 5.6% | 7.4% | 9.3% |
| function, unseen training scripts | 3.6% | 6.3% | 9.8% | 16.3% | 24.9% | 28.3% |
| failure *kind* (20 coarse kinds) | 29% | 51% | 78% | 89% | 99% | 100% |
| failure *instance* (which var, which exception) | 17% | 26% | 39% | 51% | 64% | 69% |

Distinct kinds after 8 / 32 / 128 / 247 scripts: 7 / 13 / 20 / 20. Distinct instances: 8 / 30 / 103 / 210.

1. **Function-level learning is not flat - it rises with every doubling and has not saturated at 250 scripts** -
   but slowly: about +5 points of reachable held-out loss per doubling, **+1.5-2 after discounting by what we can
   verify today** (9% at 250 scripts). The held-out curve matches the within-training one, so package sharing in the
   split does not flatter it much. This is the only unit measured so far that keeps improving with more translations.
2. **Failure kinds saturate almost immediately**: 20 kinds, 13 of them met within 32 scripts, all by 128. Rules
   keyed by failure kind transfer to new scripts at once - which also means they are a one-off investment, not a
   learning curve: after ~100 translations there is nothing new to learn at that level. And most of the large kinds
   are not rule-shaped (crash 12%, warnings differ 12%, printed text differs 11%, data variable missing 11%).
3. **Failure instances keep arriving**: 210 distinct after 247 scripts, still growing linearly. That is the long tail
   again, and no inter-script store catches it.

**What follows.** Global learning has a real but slow ceiling, and the long tail has to be handled where it occurs:
inside the script (the backlog note above). The two are not alternatives - the same machinery serves both. If each
translation verifies the functions *it* needs while it runs (harvest the function's own examples, propose, verify,
fence what fails), it gets per-script competence immediately, and the store accumulates those functions as a side
effect, which is exactly the rising function curve. "Learn by doing, keep what you verified."

**Intra-script runtime: built (2026-10-09, commit 5c65561).** `r2py/runtime/ondemand.py` runs between the best seed
and the agent loop (`run_loop(ondemand=...)`, manifest key `translate.ondemand`): for the entities the seed still
gets wrong it takes the R function each depends on, keeps pure candidates the store lacks (`runtime/purity.py`),
builds cases from R (the script's own calls via `mine_cases`, then the package's Rd examples via
`runtime/harvest.py`), runs `propose.attempt`, admits strictly or with fenced option values (`runtime/admit.py`),
and adds the function to the store (`RuntimeStore.add`, atomic; `reload`). The agent reads its runtime section once,
at the start, so the new functions are in its prompt and the harness pastes their code. Because the store directory
persists, the same step is how the store grows across scripts. Per-script cost is capped (`max_functions`,
`budget_s`). `replay.py` gains `rewrite_w3_ondemand` (private copy of the starting store per run, so no run can
hand a function to another) and `rewrite_w3_store` (a fixed store, no on-demand: the inter-script arm).

Smoke test on three frozen states (one function each, 400 s cap): `createTimeSlices@caret` - 10 cases, passed 30/30,
admitted in 156 s, listed in the agent prompt; `as_hms@hms` - 13/14 core, not admitted (a bug, not a regime);
`months` in the lubridate vignette attributed to *base* by stage 1 (the known masking limitation: lubridate::months
masks base::months), so only 1 case - **fix before any thorough run**.

**Experiment design: two curves, cheap first, then thorough.**

*Intra-script curve* - does verifying the functions a script needs, during its translation, raise its score?
- Cheap (C1): paired replay on the 20 frozen dev states, `rewrite_w3` vs `rewrite_w3_ondemand` (empty starting store),
  2 samples, 80 runs, ~2 h. Primary: paired final-score difference. Secondary: functions admitted per state, whether
  the agent calls them (`r_*` calls in its sources, as in the 8-of-8 measurement), cost in seconds and model calls.
  A dose-response arm (`max_functions` 0 / 1 / 2 / 4) is the within-script curve proper, if C1 shows an effect.

*Inter-script curve* - does a store grown on earlier scripts help later ones? The recurrence curve predicts the
size: about 5.6% of held-out loss reachable after 64 scripts, discounted. No cheap score experiment can resolve that,
so the cheap step measures the mechanism instead:
- Cheap (C2): run the on-demand step alone over the first 64 training scripts' saved translations (re-verified for
  their failing entities; no new translations), store persisting, snapshots after 8 / 16 / 32 / 64. Measure the
  **hit rate**: the share of held-out failing candidate loss whose function is in each snapshot (structural, no
  model calls), against curve 1's prediction made with hypothetical functions. ~1 h of on-demand model calls.

*Thorough* (pre-registered): a **fresh held-out set** drawn from the 3,988-script pool and never touched in
development (the dev states are held-out scripts and have been replayed many times); training on 256 scripts with
on-demand on and the store persisting, snapshots 0 / 64 / 128 / 256; held-out scoring, 3 reps, arms:
A baseline (no runtime), B on-demand from an empty store (intra-script only), C each store snapshot with on-demand
off (inter-script curve), D full store plus on-demand (both). Primary tests: B vs A (intra), the slope of C over
snapshots (inter). Endpoints, power and the masking fix are settled in the registration, after C1 and C2.

**C1 - intra-script curve, cheap (2026-10-09, `work/replay_ondemand/`).** Paired replay on the 20 frozen dev states,
`rewrite_w3` vs `rewrite_w3_ondemand` (empty starting store, at most 2 functions, 900 s), 2 samples, 80 runs, no
provider failures. Run time 5.9 -> 7.9 min (the on-demand step 2.5 min).

| | n | paired diff | p | better / worse / tied |
|---|---|---|---|---|
| all states | 20 | **+0.033** (SE 0.037) | 0.20 | 5 / 3 / 12 |
| something admitted | 5 | +0.083 (SE 0.089) | 1.00 | 1 / 1 / 3 |
| nothing admitted | 15 | +0.016 (SE 0.040) | 0.26 | 4 / 2 / 9 |

- **The step rarely fires.** 56 attempts: **28 no_cases (50%)**, 19 failed, **9 passed (16%)**, in 5 states.
- Where it fires it can matter: `hms` went **0.000 -> 0.439** with `hms@hms` admitted in both samples. The other
  admissions changed nothing (`blob` was already 1.0, `isoband`, `xml2`, `caret`).
- The admitted functions were called in the agent's final source **5 of 9** times - less than the earlier 8 of 8.
- The nothing-admitted states are the noise floor: identical treatment, yet `ggplot2` +0.465 and `clock` -0.348.
  At n = 20 and 2 samples this cannot resolve +0.03.

**C2 - inter-script curve, mechanism (`work/store_growth/`).** The on-demand step alone over the first 64 training
scripts' saved translations, store persisting.

| after N scripts | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| functions in the store | 0 | 0 | 1 | 3 |
| held-out loss covered | 0.0% | 0.0% | 0.0% | **1.1%** |
| recurrence prediction (discounted) | 1.5% | 2.6% | 4.0% | 5.6% |

43 attempts: **24 no_cases (56%)**, 16 failed, **3 passed (7%)** (`row.match@prodlim`, `rowMeans.dist@proxy`,
`matrix@base`). Real coverage is about a fifth of the prediction, because the prediction assumed the pilot's pass
rates on attempted functions, while the real step first loses more than half its attempts to missing test cases.

**Reading.** Both mechanisms work end to end and both are throttled by the same thing: **per failing function,
P(admitted) is 7-16%, and the largest single loss is `no_cases` (50-56% of attempts).** That is a general
constraint, not a package-specific one, and it caps both curves at once - intra-script (few functions admitted per
script) and inter-script (3 functions after 64 scripts). **Why the cases are missing** (37 distinct `no_cases` functions from C1 and C2, Rd harvest re-run alone, no model
calls): 12 got only 1-2 cases from their Rd examples (thin examples, below the threshold of 3); 8 ran their examples
but recorded no call - `as.POSIXct@base`, `group_by@dplyr`, `separate_rows@tidyr`, `months` (masked) - where the
recorder either did not intercept (base namespace) or silently dropped an argument it could not serialise (data
frames, tibbles); 6 have no examples; 4 have only object arguments (fingerprints); 5 harvest errors or timeouts.
The two largest groups are general, not package-specific: **mutants of the real calls** (the first-argument
variants `difftest` already makes for invented calls, applied to harvested and mined calls, with R's answer for
each) would lift the thin-example functions over the threshold, and **telling "not intercepted" from "not
serialisable"** in the recorder would show which of the silent eight are fixable.

Neither curve is ready for the thorough experiment: the
inter-script arm would measure ~1-3% coverage, and the intra-script effect (+0.03) is about 1.3 standard errors at 60
held-out scripts. Raise the yield first; case supply is where most of it goes.

**What limits runtime admission, and what was fixed (2026-10-09, commit 518571d).** Of 99 on-demand attempts in C1+C2:
52 never got cases, 35 got cases and failed, 12 were admitted. Every cause found, in order of size:

1. *My own gate* (52 of 99). `ondemand` skipped a function with fewer than three **real** cases before calling
   `propose.attempt` - which already adds model-written calls and first-argument variants answered by R. Removed:
   real cases (zero or more) go to `propose`, which gives up itself below three ordinary cases.
2. *Synthetic calls ignored the examples* (user's idea). `propose_calls` wrote calls from the usage line alone, and
   R rejects many such calls for package functions (wrong object types). With the package's Rd example code and the
   real calls recorded from it, the model now writes new calls in their style; R validates each and supplies the answer.
3. *The recorder broke the examples it observed.* Its wrapper forced the arguments (`list(...)`) before calling the
   function, so every function with unevaluated arguments (`group_by(cyl)`: there is no variable `cyl`) failed, and
   with it the example statement and everything after. It now calls first and captures after; NSE arguments are
   counted as unrecordable instead of breaking the run.
4. *`\donttest{}` examples never ran.* `utils::example` defaults to `run.donttest = interactive()`, false under
   Rscript, so those blocks came back commented out (`##D`) - base R keeps nearly all its examples there (`seen 0`
   for `as.POSIXct` until then; 60 cases after). `\dontrun{}` stays off.
5. *Variants of real calls.* The recorder applies difftest's first-argument variants (NA inserted, tie, scaled,
   reversed, single value) to each intercepted call, answered by R (`createTimeSlices`: 7 calls -> 35 cases).
6. *An acceptance bug.* With real cases present, invented cases were never labelled core/exotic, and `core` defaults
   to True: every invented call and variant, odd input classes included, silently became a required case, against
   the stated rule. Now always labelled; admission (`admit.assess`) also judges core cases only.
7. *Near misses failed all-or-nothing on input classes.* The pilot's near misses were mostly vectorisation and NA
   failures. A fence can now refuse an input class of the first argument (vector, NA) as well as an option value -
   correct where verified, an explicit `NotImplementedError` elsewhere - and admission uses the full case list
   `propose` built, so every failure is judged directly.
8. *Depth did not pay.* The best version was the first in 14 of 35 failures. Default now 4 independent attempts x 2
   rounds (the same 8 calls) instead of 2 x 4; `propose` records the per-round history so this can be checked.

Recorder diagnostics on the 37 previously case-less functions, Rd harvest alone after fixes 3-5: 6 now >= 3 real
cases, 10 with 1-2 (now passed on to `propose`), 7 with unevaluated (NSE) arguments, 6 without examples, 5 errors,
3 still unseen. Structural limits that remain: NSE functions (dplyr, tidyr verbs), object arguments (fingerprints),
functions without examples, compiled-code semantics (the DST gap), and genuinely wrong implementations.

Yield meter: C2 rerun as `store_growth.py --tag v2` on the same 64 scripts, fresh store, every attempt logged in
`work/store_growth_v2/attempts/`. Before: 3 of 43 attempts admitted (7%), 1.1% of held-out loss covered.

**Yield meter after the admission fixes (C2 v2, 2026-10-09, `work/store_growth_v2/`).** Same 64 training scripts,
fresh store, every attempt logged.

| | C2 v1 | C2 v2 |
|---|---|---|
| attempts | 43 | 43 |
| no test cases | 24 (56%) | **7 (16%)** |
| failed implementation | 16 | **29** |
| admitted | 3 (7%) | **4 (9%)** - 3 passed, 1 restricted |
| skipped for the 900 s budget | 0 | 4 |
| held-out loss covered after 64 scripts | 1.1% | **0.0%** |

*A flaw found and fixed on the way:* the option-value fence fenced **data** - `read_xml` was admitted with
`x = '<!DOCTYPE doc ...>'` fenced and `encode_native` with `colour = 'grey10'`, refusing those exact strings and
staying silently wrong on every other input. An option is now a flag or an enum keyword (logical, or a short
identifier-like string such as "pre"), never the first argument (`admit.option_values`, 4 tests). Re-judging all
logged attempts under the corrected rule leaves only `state_at_end@fansi` (normalize = TRUE fenced, 17/17 inside,
1/1 refused); the two wrong entries were moved out of the store (`store_growth_v2_invalid/`).

**The case-supply fixes worked, and moved the bottleneck.** No-case attempts fell from 56% to 16%, but the 17
functions that now reach the implementation stage almost all fail there, so admission barely moved (7% -> 9%). The
248 core-case failures of the failed attempts are genuine semantics, not harness artefacts: **wrong value 63%**,
wrong length or shape 11%, raised an exception 25% (TypeError, ValueError, ImportError, ...); none were "code does
not run" or "serialised instead of natural object". Later attempts or rounds beat the first version in 16 of 32
attempts, so breadth still pays, but from a low base: 15 of 29 failures pass under 30% of their core cases.

**What this says about the inter-script curve.** With Gemma building the functions, about 1 in 10 failing functions
gets admitted, the long tail means admitted functions rarely recur (0 of 6 in v2 touch held-out loss), and the
recurrence ceiling (25% of held-out loss at 250 scripts with perfect admission) shrinks to about 2-3%. The store
mechanism is sound - cases, verification, fences, sharing all work - but at this implementation success rate it
cannot produce a learning curve worth a thorough experiment. The binding constraint is now **the quality of the
implementations the model writes for package functions**, and the decision about it is a scope decision (whether
anything other than Gemma may write verified harness knowledge), not an engineering one.

**Gemma vs Haiku for building the store - design and decision rule, fixed before the run (2026-10-09).** The C2 yield
meter twice, identical except for the model that writes the synthetic calls *and* the implementations: the first 64
training scripts in manifest order, fresh store per arm, `max_functions` 2, **8 attempts x 2 rounds**, and a 3,600 s
budget per script so that attempts, not seconds, bind (a slower model must not get fewer tries). Both arms run at the
same time with 4 workers each. Haiku is an instrument for the question "does the model limit admission?", and a
candidate only for writing verified harness knowledge offline - every translation stays with Gemma.
Fairness fixes made first (commit 2551a29): the Anthropic path now retries and records every API error as the
OpenRouter path does, and a truncated answer is kept on both paths instead of ending the attempt on one of them.

- Primary: admission rate per attempted function (passed, or restricted under the corrected fence rule), Fisher's
  exact test; also paired on the functions both arms attempted.
- Secondary: no-case rate, held-out loss covered after 64 scripts, model calls, worker-hours.
- **Decision:** C2 builds the store with Haiku if Haiku's admission rate is at least twice Gemma's **and** at least
  25%; otherwise with Gemma, accepting that the inter-script curve is shallow. Then C1 is decided.

**Result (2026-10-10): no model effect - C2 stays with Gemma.** Both arms ran all 64 scripts and attempted the
same 43 functions. (The runs were interrupted twice: Haiku ran out of Anthropic credits, and Gemma froze when the
laptop went into standby. Both resumed from `results.jsonl`. Neither interruption left a truncated attempt or a
budget skip.)

| | Gemma 4 31B | Haiku 4.5 |
|---|---|---|
| admitted (passed + restricted) | 7/43 = 16.3% (5 + 2) | 6/43 = 14.0% (1 + 5) |
| no cases | 6 | 5 |
| held-out loss covered after 64 scripts | 1.6% | 1.1% |
| model calls | 580 | 636 |
| worker-hours | 5.3 | 2.5 |

- Fisher's exact test gives p = 1.0.
- Paired on the 43 functions:
  - both arms admitted 4;
  - neither admitted 34;
  - only Gemma admitted 3;
  - only Haiku admitted 2.
- Haiku is neither twice Gemma's rate nor at 25%, so under the fixed rule C2 uses Gemma. It falls short on both counts.
- The functions that resist are the same ones for both models (`as.POSIXct`, `time_force_tz` and the rest).
- Gemma got more outright passes; Haiku got more fenced near-misses.
- The limit is therefore not this model swap. It is the task as posed: write a whole package function from its usage,
  its source and a few cases, then make up to 2 repairs per attempt.
- Haiku's only advantage was speed (2x per worker).
- Gemma's admission rate (16%) is higher than in v2 (9%). That is consistent with 8 attempts instead of 4: more tries
  help a little, and the model does not matter.

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

**Depth instead of breadth - design fixed before the run (2026-10-10).** Same C2 yield meter as the Gemma arm:
- Gemma, the first 64 training scripts, a fresh store (`--tag rounds4`).
- **4 attempts x 4 rounds**, the same 16 calls per function as the A/B arm's 8 x 2.
- The locator was already on in both runs (`ondemand.verify_needed` passes `locate=True`), so rounds are the only
  change.

Why rounds: in the A/B Gemma arm, round 2 improved on round 1 within an attempt in 67 of 268 attempts (same in 194,
worse in 7).

Primary: admission rate per attempted function against 16.3% (7/43), Fisher, and paired on the functions both runs
attempted.

Then the C2 estimate: held-out loss covered after 64 scripts, extrapolated along the recurrence curve. If admission
reaches about 30% or more, the thorough C1 experiment is worth running.

**Result (2026-10-11): depth barely helps - 8/43 (19%) against 7/43 (16%), Fisher p = 1.0.** Paired on the 42
functions both runs attempted: both admitted 6, neither 34, only the 4x4 run 2 (fansi `substr_ctl`, proxy
`rowMeans.dist`), only 8x2 none (proxy `rowSums.dist` was not attempted in the 4x4 run).
- Later rounds keep improving the code, but rarely: round 2 improved on round 1 in 37 of 126 attempts, round 3 in
  28 of 124, round 4 in 19 of 123.
- 3 of the 5 outright passes came at round 3 or 4.
- No provider failures; 558 calls; 4.1 worker-hours.
- Held-out loss covered after 64 scripts: 1.6%, the same as the 8x2 run.

**C2 estimate.** Across four runs and two models, admission is 9-19% per attempted function. At 64 scripts the store
covers 1.6% of held-out loss, against 5.6% if every attempt were admitted (29%).

Along the recurrence curve (25.1% of held-out loss at 247 scripts with perfect admission), that projects to roughly
4-7% after the whole training set. Discounted for functions that are reached but not used, it is about 2%.

The inter-script curve exists but is shallow. A thorough C2 experiment would measure a slope too small to detect at a
feasible held-out size, so it is not run. The store stays on as part of the harness. Next: C1.

**C1 step 1 - where loss sits in the agent loop (2026-10-11), from existing logs.** Data: the `rewrite_w3`
trajectories of the C1 replay and the oracle replay. That is 100 runs from frozen states (99 complete), 296 branches
and 1,111 steps; no new model calls.
- **The loop works, then gives up early.** Mean score goes from 0.414 to 0.766; 40 of 99 runs reach 0.9.
- **How branches stop** (logged reasons): 62% stall (3 non-improving rewrites in a row), 37% reach the threshold, 1%
  run out of budget. The median run takes 374 s of its 1,200 s budget, and a branch takes 3.8 steps on average. Time
  is not the limit; ideas are.
- **Steps:**
  - 27% improve the score; 7% more make shaped progress (the per-step improved count can be lower than the outcome
    count: one step can log several outcomes).
  - 26% leave it unchanged.
  - 17% make it worse, and 13% are catastrophic.
  - 10% are rejected by a gate (review, import or syntax).
- **Lookups:** 12 `probe_r` actions in 1,125. The agent almost never looks things up.
- **What remains at the end** (149 loss units over the final states):
  - 66% is partial entities: score between 0.1 and 0.9, most often 0.8.
  - 18% is entities that never score above 0.1 in any candidate.
  - 8% is entities that some candidate got right (≥ 0.9) but the accepted one lost. That is the ceiling for
    recombining candidates per entity.
- **Reading:** the remaining loss is mostly *nearly right* entities that 3 independent rewrites fail to finish, not
  missing knowledge or missing time. The trajectories do not say which score dimension the partial entities lose
  (value, type, shape, printing). That needs the final sources re-verified, the next measurement.

**C1 step 1b - the final translations re-scored per dimension (2026-10-11).** `scripts/rescore_finals.py`: the
best accepted source of each of the 100 `rewrite_w3` runs (or the start state, for the 20 that never improved),
verified again with the replay's settings.
- **Fidelity:** re-scored aggregates match the logged ones (mean |diff| 0.016; 5 runs differ by > 0.05). 1 error.
- **Model calls:** 17 rows used a sentinel-mapping model call.

Remaining loss, 178.6 entity units, by kind:

| Kind | Share |
|---|---|
| Values wrong (data, type, variable), side effects fine | 34% |
| Side effects only (values all ≥ 0.9) | 24% |
| Both | 20% |
| Not executed | 16% |

What the side-effect-only entities get wrong:
- **Mostly printed output:** right values, wrong print format. Examples: R prints a tibble and the Python prints a
  pandas frame (`broom` `tidy`, stdout 0.19); clock's zoned time printed differently (0.44); highr's highlight class
  `def` vs `kwc` (0.74).
- A few graphics figure counts and data details.

**A feedback bug found on the way.** Stage 1 sinks R's output into per-entity checkpoints, so the whole-script R
stdout the verifier compares is empty: in 42 of 59 replay scripts, R prints per entity but the script-level R
stdout holds nothing.

Scoring is not affected: entity scores use the per-entity bundles. What the agent reads is:
1. The script-level comparison "R printed '' but Python printed <its correct output>", broadcast as a feedback item
   to every entity. `format_score_report` shows the first 10 feedback items. In the broom final state all 10 are
   this false claim, attached to unrelated entities (`set.seed`, `import_dplyr` ...), and they crowd out real
   feedback.
2. The per-entity stdout comparisons, which show the right R and Python text but carry the script-level score
   (0.000 instead of the entity's 0.191).

So for the 24% side-effects-only loss, the agent is told both "R printed this tibble" and, ten times, "R printed
nothing". This is the same class of defect as the sidecar bug: the score is right, the feedback is corrupted.

**Step 2 follows from this.**
1. Fix the feedback: build the script-level R stdout from the per-entity outputs, or drop the broadcast when
   per-entity bundles exist, and give per-entity comparisons their own score. Scoring is unchanged, so replays stay
   comparable.
2. Replay the fix against the baseline on the same frozen states.

**C1 step 2a - stdout feedback fix and its replay; design fixed before the run (2026-10-11).**

Fix (`r2py/stage4/verifier.py`, 2 tests in `tests/test_stage4.py`):
- The script-level STDOUT result is no longer broadcast as feedback to every entity when R's per-entity bundles
  hold output.
- Per-entity stdout comparisons carry their own score.

Scoring is unchanged. Checked on 12 final states: aggregate |diff| 0.0, the false items gone. In googledrive R
really prints nothing, and its stray-output items rightly stay.

Replay:
- Policy `rewrite_w3`, the same 20 frozen dev states as C1 (the arms `20261001_112951 140509 165951` reproduce
  all 20 start hashes), 3 samples, 6 workers.
- Output in `work/replay_feedback/`.
- Baseline: C1's `rewrite_w3` runs (`work/replay_ondemand/`, 2 samples, run 2026-10-09 after the sidecar fix;
  harness changes since then touch only the runtime store and the Anthropic path). This is a historical baseline,
  not a concurrent arm.

Primary: per-state mean final score, fixed minus baseline, paired over 20 states (mean, SE, Wilcoxon).

Secondary:
- P(final ≥ 0.9);
- share of branches that stop by stalling;
- the side-effects-only share of remaining loss (`rescore_finals.py` on the new finals).

Runs with provider failures in the log are reported and excluded.

**Result (2026-10-11): correct feedback, no measurable effect.** 60 runs, 0 errors, no provider failures.
- **Primary:** per-state mean final score 0.767 fixed against 0.747 baseline. Paired diff +0.020, SE 0.038,
  better/worse/tied 5/4/11, Wilcoxon p = 0.58.
- **Large swings are noise:** hms +0.60 and clock -0.41 are states that start crashed (0.0) and either get unstuck
  or not, with both outcomes in both arms across samples.
- **Secondary:**
  - P(final >= 0.9) 0.43 against 0.40.
  - Stalled share of branches 0.59 against 0.64.
- **Print-only loss did not move:** 0.45 against 0.48 entity units per run; 22% of remaining loss in both. The
  re-scored finals are in `work/rescore_finals_feedback/`.

The fix stays: the feedback was false, and the change costs nothing.

Telling the agent the truth about print format does not make it fix print format. This is the same pattern as
every prompt-side measurement before: information in the prompt barely changes what the model writes; code the
harness owns and verifies does. The intra-script lever for the side-effect loss is therefore not feedback but a
harness-owned, R-verified way to print, analogous to the runtime store.

**Correction (2026-10-11).** Two earlier conclusions counted the false "R printed ''" broadcast as real:
- the corpus sizing "stray output Python produced and R did not: 8% of loss" (2026-10-08);
- the blob/months rows of the prompt-arms failure diagnosis.

Both rest on feedback that, in about 70% of scripts, was the broadcast fixed above, not a real per-entity
mismatch. Treat both as unreliable.

**Prompt-load experiment - why Gemma does not follow guidance; registered before it is built (2026-10-11).**
Hypothesis (user): the agent prompt overloads the model, and guidance is lost in it.

Measured first, on the 20 frozen states: the agent prompt is median 12,950 characters, about 3,500 tokens, range
7,300-23,700, including a 5,000-character system prompt. That is not long for the model's context. Dilution is
still possible: 30% of the turn is output comparisons for every entity and 11% verifier feedback. So the
experiment scales the prompt both down and up. **Gemma only** (user's decision).

*Cases:* about 40 entities from the 20 frozen states, at most 3 per script, each wrong in the frozen state.
- **Snippet cases:** the 21 usable donor cases of the prompt-arms rerun. Guidance is the correct code for that
  entity.
- **Print cases:** up to about 20 entities that run with all value dimensions >= 0.9, side effects < 0.9, R
  printing something for the entity, and Python printing something else. Guidance is R's exact printed output for
  that entity. They are selected by verifying the frozen states, with no model calls.

*Guidance:* every prompt ends with the same guidance block naming the entity.
1. **Canary:** "include the comment `# ack-<random token>` in this entity's code". This is neutral and harmless,
   and measures whether an instruction is read and followed at all.
2. **Substantive:** the fix itself, as an instruction.

*Arms:* 3 samples each. The system prompt is the agent's, as in the prompt-arms rig: whole-file arms get the
variant without `replace_entity`. Every prompt says not to probe or look anything up.

| arm | the model reads | it writes |
|---|---|---|
| A1 full/whole | today's agent turn | the whole file |
| A2 full/entity | today's agent turn | one entity (`replace_entity`) |
| A3 trim/whole | R source, full Python, only this entity's scores, comparisons and feedback | the whole file |
| A4 trim/entity | as A3 | one entity |
| A5 local | this entity's R lines, Python lines, scores, comparisons and feedback | one entity |
| A6 local+pad | A5 plus another script's R and Python as labelled unrelated material, to A1's length | one entity |
| A7 full x2 | A1 plus the same padding, to twice A1's length | the whole file |

Padding goes before the case material, so the guidance stays last in every arm.

*Outcomes, per call:*
- canary present in the entity's code (and anywhere in the answer);
- **adoption:**
  - snippet cases: share of the donor's distinctive tokens, adopted if >= 0.5;
  - print cases: the entity's stdout similarity to R after verification, adopted if >= 0.95;
- entity score change;
- "no code" answers;
- prompt characters.

Provider outages are discarded and the case repeated, as in the prompt-arms rig.

*Decision rule (Gemma), on the adoption rate:*
- **Overload:** A5 >= 2 x A2 **and** padding takes back at least half of that gain (A5 - A6 >= (A5 - A2) / 2).
  The fix is then a lean, entity-local agent prompt.
- **Clutter, not length:** A5 >= 2 x A2 but A6 stays near A5. Remove irrelevant sections; do not just shorten.
- **Answer scope:** entity arms clearly beat whole-file arms at equal length (A2 vs A1, A4 vs A3) and length has
  no effect. Build the loop around entity edits.
- **Neither:** adoption flat across arms while the canary is followed. The model reads the guidance and declines
  it, so the problem is trust, not attention. Next: framing with verification evidence.
- The canary on its own failing in long arms and passing in short ones is direct evidence of an attention deficit.

*Changes after a 14-call smoke test, before any data (2026-10-11).* The smoke calls are not part of the results.
1. **Cases.** 21 of the first 42 cases were entities split over several places in the file. `splice_entity`
   refuses those, which would fail the one-entity arms for reasons unrelated to the prompt, so cases now require a
   single span.
   - Drawn from all 24 dev states (not only the 20 with start < 0.9), at most 3 per kind per script.
   - Result: **21 cases (10 snippet, 11 print)**.
   - To keep the planned number of calls, **5 samples instead of 3**: 735 calls.
2. **Sizes are total prompt sizes.** The 5,000-character agent system prompt kept "local" at 6.7k against 9.4k.
   - The local arms (A5, A6) now use the harness's own one-entity system prompt (`ENTITY_REPAIR_SYSTEM`).
   - A6 is padded to A1's total and A7 to twice A1's total.
   - Medians over the 21 cases: A1 13,974, A2 14,034, A3 9,906, A4 9,969, **A5 2,894**, A6 14,112, **A7 28,026**
     characters.
3. **Local answers are always spliced.** In a local arm, an answer is spliced into the entity whatever action it
   names, since the model saw only that entity.

**Prompt-load result (2026-10-11): 735 calls, no provider failures. The decision rule is NOT applied (user's
decision).** The smoke-test change gave the local arms (A5, A6) a different system prompt, so "short prompt" and
"short system prompt" are confounded. Descriptive only:

| arm | chars | canary | adopted | snippet | print | entity score change |
|---|---|---|---|---|---|---|
| A1 full/whole | 13,974 | 19% | 16% | 4% | 27% | +0.119 |
| A2 full/entity | 14,034 | 32% | 27% | 36% | 18% | -0.100 |
| A3 trim/whole | 9,906 | 38% | 32% | 30% | 35% | **+0.241** |
| A4 trim/entity | 9,969 | 53% | 16% | 26% | 7% | -0.143 |
| A5 local (short system) | 2,894 | **67%** | **42%** | 50% | 35% | -0.019 |
| A6 local+pad (short system) | 14,112 | 61% | 41% | 54% | 29% | -0.071 |
| A7 full x2 | 28,026 | 39% | 41% | 48% | 35% | +0.100 |

- **Length alone is not it.** A6 is as long as A2 and behaves like A5.
- What separates A6 from A2 is the system prompt (1,200 vs 5,000 characters) and relevant clutter (the whole
  script and every entity's results) against unrelated padding. This run cannot tell which.
- **A7 is unexplained.** Padding the full prompt raises adoption (16% to 41%) and the canary (19% to 39%).
- Even in the best arm, a third of canaries are ignored.
- **One-entity answers adopt more often but score worse.** All four one-entity arms lose score; all three
  whole-file arms gain. A one-entity answer cannot fix what the entity depends on elsewhere.
- 18 print-case answers pasted R's output as a literal.

**Entity markers - why they get lost, and what the agent then sees (2026-10-11).**

*Correction first.* The trajectory logs a rewrite's raw candidate at `accepted`, before the loop restores the
markers (`best_source = harness.last_annotated_source`). `rescore_finals.py` took those raw candidates as the final
states. The "29.5% of remaining loss in unmarked entities" figure therefore overstates the problem. The step 1b
breakdown by dimension is unaffected in aggregate: re-scored aggregates matched the logged ones.

What happens, traced over the 374 accepted rewrites of the 100 baseline runs:
- **The model kept every marker in 249.**
- **It dropped some in 125.**
  - In 87 of these, the deterministic alignment (`restore_sentinels`) puts all of them back.
  - In 38, alignment cannot place them all, and `HarnessTools.verify` asks a model to re-map the entities. Its
    instructions let it omit entities, and it then sets `_mapped_eids` to the subset it returned. **Omitted
    entities are dropped from the tracked set for good**, and are never restored by later steps.
- **67 entities in the start states never had a marker.** The seed-stage mapping left them out. In isoband, for
  example, `df_bands`, `isobands`, `g` and `grid.*` have no Python code at all ("missing in Python output").

What the agent gets for an unmarked entity:
- Its score in the per-entity list, and "missing in Python output" data feedback where applicable. Most
  comparisons are absent.
- `replace_entity` refuses it ("unknown entity ... no `# r2py:entity:` line"), and so does harness entity repair.
  Only a whole-file rewrite can reach it, and nothing tells the agent where the code for it should go.

The size of the model re-mapping loss needs those 38 mappings re-run, about 38 model calls, not done yet.

**Follow-up: system prompt vs content, a 2x2 registered before the run (2026-10-11).** Same 21 cases, Gemma, 5
samples. All four cells run together into `work/prompt_load_sys2x2/`; A2 and A5 are re-run, not reused.

| | agent system prompt (5,003 chars) | one-entity system prompt (929 chars) |
|---|---|---|
| full agent turn | A2 (median total 17.0k) | B1 (12.9k) |
| this entity only | B2 (7.0k) | A5 (2.9k) |

Every cell asks for a one-entity answer and ends with the same guidance block.

Outcomes: canary followed, guidance adopted (as before), entity score change.

Main effects on adoption, each averaged over the other factor:
- system effect = short - agent;
- content effect = local - full;
- 95% interval by bootstrap over cases.

A factor **matters** if its effect is >= 10 points and its interval excludes 0. The canary is reported the same
way.
- System matters, content does not: slim the agent system prompt. This is cheap and applies to every package.
- Content matters, system does not: give the loop entity-local context.
- Both: both.
- Neither: the A2/A5 gap of the main run was not one of these two factors.

**2x2 result (2026-10-11).** 420 calls. A credit outage after 280 was caught by the guard (3 calls discarded) and
the run resumed after the top-up.

| | agent system (5,003) | short system (929) |
|---|---|---|
| full content: canary / adopted | 32% / 30% | 71% / 43% |
| local content: canary / adopted | 54% / 41% | 66% / 36% |

- **Adoption, the registered outcome:** neither factor meets the rule.
  - system +4.3 points [-3.8, +12.4];
  - content +2.4 [-7.6, +13.3].

  So: **"neither"**. The A2-to-A5 gap of the main run (27% to 42%) shrank to 30% to 36% here.
- **Canary:** **the system prompt matters**, +25.2 points [+11.4, +39.0]; content +8.1 [-3.8, +20.0]. The
  5,000-character agent system prompt makes Gemma ignore a trivial, explicit instruction about half the time it
  would otherwise follow it.
- Entity score change is about zero in every cell (-0.08 to +0.01). 29 print-case answers pasted R's output as a
  literal.

**Reading.** The large system prompt does crowd out instructions; the canary shows it clearly. But whether Gemma
adopts a *substantive* fix does not depend on the system prompt or the amount of context: it stays at 30-43%, and
adopting it does not raise the entity's score. Gemma reads the guidance and mostly declines it, or uses it without
effect.

So the overload hypothesis explains instruction neglect, not the failure to use guidance. Next candidates:
- **trust:** Gemma prefers its own version; test framing with verification evidence;
- **usability:** the guidance cannot work in that position (literal pastes; adoption without gain); look at the
  adopted-but-unchanged cases.

**Adopted but no gain - inspected (2026-10-11), both prompt-load runs, 1,144 verified calls, no model calls.**

The premise was wrong in the pooled form. **246 of 383 adoptions raised the entity's score.** The 137 that did not
share one feature: **every one ended with the program crashing**, and they come from 4 entities in 3 scripts
(clock, hms, pROC).

Split by whether the start state runs:

| start state | calls | adopted -> gain (mean) | not adopted -> gain (mean) |
|---|---|---|---|
| crashes (7 cases: clock, hms, pROC) | 384 | 26% (-0.065) | 20% (+0.040) |
| runs (14 cases) | 760 | **98% (+0.257)** | 38% (-0.082) |

Within the same case (10 running cases with both outcomes), adopted calls beat non-adopted ones in **10 of 10**,
by a mean of +0.53.

*Caveat.* For print cases, "adopted" means the entity's stdout matches R (>= 0.95), which is part of the score, so
some of that gain holds by definition. Only one snippet case in a running state has both outcomes (tidyr
`tribble`: +0.15 vs +0.08).

Why the crashing cases cannot gain, re-verified with the adopted code spliced in:
1. **The program already crashes before the target entity** (clock at `info`, hms at `new_hms`, pROC
   unattributed). No change to the target can score until that crash is fixed: the crash cliff again.
2. **The donor snippet is not self-contained.** It calls helpers that existed in the donor's program and not in
   this one (`year_month_day`, `format_hms`), so the crash moves *into* the target entity.
3. **Answer-format slips.** One replace_entity answer carried the whole file, data shim included. One print answer
   pasted R's output as literals.

**Reading.**
- When the program runs and Gemma uses the guidance, the guidance works.
- Use depends heavily on the case. In the running print cases it ranges from 1 of 55 calls (broom `tidy`, a
  tibble print) to 52 of 55 (purrr `str`). That looks like how hard the requested output is to produce rather than
  distrust.
- The two levers this points to are general, not package-specific:
  - fix crashes before guidance (an upstream crash nullifies everything after it);
  - make guidance self-contained (donor code must carry or name its helpers).

**Three fixes after the adopted-but-no-gain finding (2026-10-11).** All three are tested; the full suite passes
except the known `test_stage2` locale failure.

1. **Crash first, in every policy** (`r2py/harness/agent.py`).
   - Before: the crash culprit was targeted only with `entity_repair=True`. `rewrite_w3` runs without it, and even
     with it the targeting was skipped at step 1 on a crashing start (score 0.0).
   - Now, while the best program crashes, each step repairs the traceback's culprit (`_pick_crash_entity`: the
     outermost frame first; without attribution, the first entity that did not run).
   - When the culprit cannot be replaced as one block (no marker, several spans) or has had 2 tries, the step is
     a full rewrite with a pinned "Fix the crash first" note naming the entity and the error
     (`_crash_first_note`).
   - Fixing one crash lets the program reach the next, which becomes the next target. `objective.search_key`
     already accepts a crash that moves later as progress.
   - Programs that run are left to the policy.
2. **Self-contained guidance** (`r2py/stage2/stitch.py: self_contained`). A snippet is preceded by the top-level
   functions, classes and imports of its program that it uses, transitively. Script variables are left out. Used
   by the library harvest (`_extract_entity_snippet`) and the donor snippets of the probe rigs
   (`substitution_probe.donors`).
3. **Crash-aware status** (`objective.entity_status`): `ran` / `crashed` / `blocked` / `not_run`.
   - Carried by the held-out entity records (`status`), `rescore_finals.py` and `prompt_load.py` (`start_runs`,
     `status_before`, `status_after`).
   - `prompt_load` summaries add a table restricted to cases whose starting program runs. A blocked entity's
     score is not evidence about what was done to it.

**Registered before the runs (2026-10-12): Part A (system prompt trimming) and Part B (crash-first in the
loop).** Gemma only. Part C follows A: A's winner with crash-first, on the 20 frozen states, against B's runs.

*Part A - which system prompt lets Gemma use guidance* (`prompt_load.py`, tag `sysprompt`).
- **Cases:** the prompt-load case rules (single-span entities, at most 3 per kind per script, all dev states),
  **restricted to states whose starting program runs**, so no crash can mask an effect.
- **Base:** the production setting, i.e. today's full agent turn with a whole-file answer and the same guidance
  block (canary + fix) at the end. Only the system prompt varies:
  - **S0** current (`without_replace_entity(AGENT_SYSTEM_PROMPT)`, 4.6k);
  - **S1** role and output format only;
  - **S2** S1 plus the current rules the harness enforces, paraphrased concisely (names, module level, argument
    order, reserved words, data-shim line, no hardcoding, guard removal). This is a subset, with no new rules;
  - **S3** current minus the `probe_r` / `lookup_docs` documentation and the probing rules.
- 5 samples.
- **Outcomes:**
  - canary;
  - adopted;
  - entity score change (unblocked entities only);
  - **gate violations:** the answer does not parse (`_check_syntax`), or the anti-hardcoding review rejects it
    (`review_translation`, run on every answer, one extra model call each);
  - argument-order repairs, reported.
- **Decision:** take the shortest prompt that raises adoption by >= 10 points over S0 (95% bootstrap interval over
  cases excludes 0) **and** does not raise gate violations by more than 5 points. If none qualifies, S0 stays.

*Part B - does crash-first repair crashes better* (`replay.py`, `rewrite_w3`, current harness, 20 frozen states,
3 samples, `work/replay_crashfirst/`).
- **Baseline:** `work/replay_feedback/`. It is the same harness minus crash-first (self-contained guidance has no
  effect with the empty replay library), run 2026-10-11, not concurrently.
- **Primary, on the 8 states whose start crashes (24 runs per arm):**
  - share of runs ending with a program that runs (baseline 20/24);
  - steps until the first candidate that runs (from trajectories);
  - mean final score (baseline 0.717), paired per state, Wilcoxon.
- **Secondary:**
  - the 12 states that start running (crash-first should not act there: a check, not an effect);
  - blocked entities at the end.
- **Decision:** crash-first stays unless it lowers the crashing states' mean final score. It is called an
  improvement only if the paired test gives p < 0.05. Eight states can show only a large effect.

*Part A, before any data (2026-10-12).*
- Only **12 crash-free cases** exist under the case rules: 2 snippet, 10 print, from 7 scripts. 7 of the 24 dev
  states start with a crash. Lifting the per-script cap gives 15, 6 of them from broom, so the cap stays.
- To keep about 400 calls: **8 samples instead of 5** (384 calls).
- Adoption here is mostly print adoption.
- With 12 cases, the bootstrap interval is wide; only a large effect will qualify.
- Part B runs with 4 workers (the baseline used 6) while Part A runs alongside.

**Part A result (2026-10-12): no shorter system prompt qualifies; S0 stays.** 384 calls, 0 provider failures, 12
crash-free cases, whole-file answers.

| prompt | chars | canary | adopted | violations | syntax | review rejected | score change (unblocked) |
|---|---|---|---|---|---|---|---|
| S0 current | 5,003 | 26% | 22% | 40% | 9% | 38% | +0.114 |
| S1 minimal | 506 | 25% | 31% | 42% | 5% | 41% | +0.157 |
| S2 rules | 1,346 | 9% | 23% | 36% | 0% | 36% | +0.109 |
| S3 no tools | 3,506 | 25% | 23% | 35% | 2% | 35% | +0.102 |

Adoption against S0, with violation change:
- S1 +9.4 points [-1.0, +20.8], violations +2.1;
- S2 +1.0 [-3.1, +5.2], violations -3.1;
- S3 +1.0 [-5.2, +9.4], violations -4.2.

None reaches >= +10 with the interval above 0.

- **With whole-file answers the system prompt does not limit instruction-following.** The canary sits at 25% under
  S0, S1 and S3. In the one-entity 2x2 the long prompt cost 25 points of canary; whole-file answering, not the
  system prompt, is the binding factor in production.
- **Trimming does not bring back the mistakes the rules were written against.** Violations are 35-42% in every arm,
  and syntax errors are lowest in the short prompts.
- **The anti-hardcoding review rejects about 38% of answers in every arm, S0 included.** The print-case guidance
  ("make it print exactly this") invites literal output, which the review exists to reject. This conflict is built
  into the guidance.
- S2's low canary (9%) is unexplained.
- **Part C reduces to Part B:** with S0 staying, "winner + crash-first" is Part B's arm.

**Part B result (2026-10-12): crash-first did not repair crashes better; by the registered rule it does not stay.**
60 runs, 0 errors, 0 provider failures.

*Crashing starts (8 states, 24 runs per arm):*

| | crash-first | baseline |
|---|---|---|
| runs ending with a program that runs | 20 | 20 |
| mean final score | 0.698 | 0.717 |
| median step of the first candidate that runs | 3 (reached in 21 runs) | 1 (reached in 22) |
| branch stops: stalled / threshold | 43 / 29 | 33 / 38 |

- Paired per state: -0.019, better/worse/tied 4/1/3, Wilcoxon p = 0.63.
- Better: clock 0.23 to 0.38, hms 0.60 to 0.89, pROC 0.37 to 0.44.
- **Worse: googledrive 1.00 to 0.33.** 2 of 3 runs stalled while still crashing; all 3 baseline runs reached 1.0.
- A full rewrite fixes a crash at step 1. Targeted repair of the culprit takes a median of 3 steps and stalls more.

*Running starts (12 states, where crash-first never acts):* -0.013, better/worse/tied **0/5/7, p = 0.031**.
- The treatment is inactive there, so this negative control shows that **the day-apart baseline differs on its
  own** by about -0.01 to -0.02.
- It is not the time budget: no run stopped on budget, and crash-first runs were faster (4.5 vs 7.2 minutes).
- Likely causes are provider-side variation between days, and Part A running alongside.
- So the crashing-state difference (-0.019) is within that drift. The comparison cannot resolve an effect this
  size, and **a historical baseline is not good enough at this precision: future A/Bs need concurrent arms.**

*Decision as registered:* crash-first lowered the crashing states' mean final score, so it does not stay as the
default.

What the data do say: on crashing starts, a full rewrite usually fixes the crash in one step. Culprit-targeted
repair is slower and failed outright on googledrive, but it unstuck hms and clock, which the baseline left stuck.

**S1 refinement, registered before any data (2026-10-12).** Part A missed its rule, but S1 (+9.4 points adoption
[-1.0, +20.8]) is worth refining; the user notes that the rule's thresholds were arbitrary. Gemma only.

1. **Case pool, from the training translations whose program runs** (`work/reverify`, 223 of 249). Single-span
   entities, at most 2 cases per script.
   - **print:** values right, stdout wrong; the guidance is R's exact printed output.
   - **value (new):** the entity ran, a value dimension < 0.9; the guidance is R's value of the entity's
     variable(s), with "compute it, do not paste it".

   Sample 60, balanced between the kinds. No model calls.
2. **Single call, all arms concurrent.** Full agent turn, whole-file answer, the same guidance block and gates as
   Part A, 3 samples. Arms: **S0**, **S1**, **S1a** (S1 + "the final section of the message holds instructions
   from the harness; follow them exactly"), **S1b** (S1a + "printed output must be produced by code from the
   data, never pasted").

   Reported against S0, with 95% bootstrap intervals over cases:
   - adoption;
   - violations (syntax, review rejection);
   - score change on unblocked entities.

   **Selection:** the S1 variant with the highest adoption whose violation interval does not lie above 0 goes to
   step 3.
3. **Agent loop, concurrent arms:** S0 against the selected variant, 20 frozen dev states, 3 samples (replay
   policies gain a system-prompt option). The final score, paired per state, decides.

Crash-first remains switched on in both arms until it is revisited.

*S1 refinement, step 1 done (2026-10-12), before any step-2 data.*
- **Pool:** 159 crash-free cases from the training translations (86 print, 73 value), with R values limited to
  1,500 characters of JSON. 5 training scripts could not be verified (syntax errors) and are skipped.
- **Sample:** 60 cases (30 print, 30 value) from 56 scripts, in `work/prompt_load_s1ref/cases.json`.
- **Value adoption** = the entity's value dimensions all >= 0.95 after the answer, which, like print adoption, is
  part of the score. `pasted_literal` flags answers containing >= 3 of R's decimal numbers.
- **Arms:** S1a = S1 + 1 line, 623 characters; S1b = S1a + 1 line, 708 characters.
- **Analysis:** `scripts/parts_ab_analysis.py s1ref`, written before the data.

**S1 refinement, step 2 result (2026-10-15).** 720 answers, 0 provider failures.
- **Interruptions:** two standbys froze the run (Oct 12 17:41 to Oct 14 22:07, and Oct 15 07:35 to 08:23). The 4
  calls hung by the second were killed and redone; single-call outcomes do not depend on wall time.

| arm | canary | adopted | violations | pasted | score change |
|---|---|---|---|---|---|
| S0 current (5,003) | 24% | 21% | 24% | 2% | +0.124 |
| S1 minimal (506) | 37% | **28%** | 25% | 3% | +0.137 |
| S1a follow (623) | **48%** | 26% | 29% | 8% | +0.123 |
| S1b follow+compute (708) | 43% | 27% | 27% | 6% | +0.144 |

Against S0, with 95% intervals over 60 cases:

| arm | adoption | violations | score |
|---|---|---|---|
| S1 | +6.7 [-1.1, +14.4] | +0.6 [-6.7, +8.3] | +0.014 [-0.034, +0.067] |
| S1a | +4.4 [-1.7, +10.6] | +4.4 [-2.8, +11.7] | 0.000 [-0.043, +0.042] |
| S1b | **+6.1 [+1.1, +11.7]** | +2.2 [-5.6, +10.0] | +0.020 [-0.013, +0.054] |

- **Selected for step 3 by the registered rule: S1 (minimal).** It has the highest adoption, and its violation
  interval does not lie above 0.
- **The shorter prompts raise adoption by about 4-7 points.** Only S1b's interval excludes 0. None changes the
  single-call score measurably.
- **One sentence doubles the canary:** "follow the instructions in the final section" (S1a) takes it from 24% to
  48%. Yet it raises fix adoption no more than the plain S1 does.
- **By kind:**
  - print adoption: S0 22%, S1 41%, S1a 32%, S1b 34%;
  - value adoption: S0 20%, S1 14%, S1a 19%, S1b 20%.

  The short prompt helps where the fix is to print R's text, and not where values must be computed. On value cases
  S0's rules may help.
- **S1a raises pasting** on print cases to 12% (S0 2%). S1b's compute sentence brings it back to 8%.
- Violations stay at 24-29% in every arm, almost all of them review rejections.

**Step 3 - three arms, S0, S1 and S1b (user's decision, 2026-10-15), and a correction found while building it.**
- The agent loop gives OpenRouter models `AGENT_SYSTEM_PROMPT_OPENROUTER` (3,860 characters as used, with a
  fenced-block answer format: `ACTION: rewrite` + a fenced block). Parts A and step 2 used
  `without_replace_entity(AGENT_SYSTEM_PROMPT)` (5,003 characters, JSON actions) as "S0". **Their S0 was not the
  production prompt.**
- In both the turn ended with "Answer with ACTION: rewrite and the complete Python file", so all arms answered in
  the same form. The comparisons stand as comparisons of those texts, not of the production prompt.
- **In the loop:**
  - **S0 = the production prompt**, unchanged.
  - **S1 and S1b keep their content but use the production answer format** (fenced block after
    `ACTION: rewrite`, and `ACTION: done`). The answer format is not what is tested, and a whole file escaped
    inside a JSON string is a known failure mode.
- Policies `rewrite_w3_S1` and `rewrite_w3_S1b` against `rewrite_w3`, all concurrent: 20 frozen states, 3 samples,
  180 runs.
- **Primary:** final score per state, each variant against S0, paired, Wilcoxon, with a bootstrap interval over
  states.
- **Secondary:**
  - P(final >= 0.9);
  - stalled share;
  - runs ending with a program that runs.
- Crash-first stays on in all arms.

**Step 3 result (2026-10-16): no short prompt measurably beats the production prompt in the loop.** 180 runs, 0
errors, all arms concurrent. A standby overnight (Oct 15 23:35 to Oct 16 13:13) caught no run: the longest took
29 minutes.

| arm | mean final | P(>= 0.9) | stalled | ends running | steps |
|---|---|---|---|---|---|
| S0 production (3,860) | 0.768 | 0.43 | 0.62 | 56/60 | 12.3 |
| S1 (loop format) | 0.785 | **0.55** | 0.57 | 55/60 | 12.1 |
| S1b | 0.724 | 0.43 | 0.60 | 52/60 | 11.6 |

Paired per state (registered primary):
- S1 vs S0: +0.017 [-0.054, +0.085], 6/4/10, p = 0.47.
- S1b vs S0: -0.045 [-0.104, +0.004], 5/5/10, p = 0.58.

*Split by start state (post hoc, not registered):*
- **Running starts (12 states):**
  - S1 +0.038 [-0.002, +0.097], 3/2/7, p = 0.31; rmarkdown 0.64 to 0.96, timeDate 0.85 to 0.98;
  - S1b +0.003.
- **Crashing starts (8 states):**
  - S1 -0.015 [-0.17, +0.13];
  - S1b -0.116 [-0.24, -0.02].

  These differences come from runs ending at 0.0 (still crashing) in clock, ggplot2, hms, pROC and xml2, which
  flip between arms.

**Reading.**
- S1 is the only variant pointing the same way in single calls (+6.7 points adoption) and in the loop (+0.017;
  +0.038 and P(>= 0.9) 0.43 to 0.55 on running starts). No test reaches significance at 20 states x 3 samples.
- S1b's extra sentences gain nothing in the loop and do worst on crashing starts.
- On crashing starts the outcome is dominated by whether the crash gets fixed, which is the crash-first question
  and the bimodal noise seen in every replay.

Production prompt unchanged for now. The next lever is the crash-first revisit (fallback version), with concurrent
arms.

**Measurement upgrade (2026-10-16).**
- `replay.py --pool training`: a fixed pool (seed 0) of 60 training translations below 0.9, **40 whose program
  runs and 20 that crash**, from 33 packages. Script maps come from `work/reverify/script_maps`. The loop keeps the
  dev manifest's settings (the held-out manifest's `max_stalls` is 10, not 3).
- `scripts/replay_compare.py`: concurrent arms against a baseline, the state as the unit, a bootstrap interval,
  Wilcoxon, all / running starts / crashing starts.
- **Power, from the spread of per-state differences in step 3** (SD 0.13-0.16): at 60 states x 3 samples the SE
  is about 0.016-0.021, so the smallest effect detected with 80% power is about **0.05**, not 0.03. 0.03 would
  need about 150 states or more samples.
- Smoke-tested on one crashing training state.

**Guided step and crash fallback, registered before building (2026-10-16).** One concurrent replay on the
training pool (60 states, 3 samples), Gemma.
- **`rewrite_w3`, baseline:** the loop as before crash-first (`crash_first="off"`). This applies Part B's
  registered decision, and **becomes the default again**.
- **`rewrite_w3_crashfb`, crash fallback:**
  - While the best program crashes, the first attempt is a plain full rewrite, exactly as in the baseline.
  - Only after a full rewrite has failed to make the program run does the next step repair the crash culprit,
    or, if the culprit cannot be replaced as one block, rewrite with the "Fix the crash first" note.
  - Part B data: full rewrites fix most crashes at step 1, and targeting rescued what rewrites left stuck (hms,
    clock).
- **`guided_w1k3`, guided step, compute-matched (user's question about the control arm):**
  - One chain, **3 sampled whole-file rewrites per step, the best kept by the verifier**. That is about the
    model calls of 3 independent chains (width 3), so a gain over the baseline cannot come from more calls.
  - When the program runs, the step's turn ends with targeted guidance for the worst-scoring entity that ran and
    has guidance: R's exact printed output (values right, print wrong) or R's values (<= 1,500 characters of
    JSON), as in the prompt-load cases; at most 2 tries per entity.
  - Without a target, the 3 samples are unguided.
- **Primary:**
  - guided vs baseline on running starts (40 states);
  - crash fallback vs baseline on crashing starts (20 states).

  Both paired per state, with a bootstrap interval and Wilcoxon (`replay_compare.py`).
- **Secondary:** all states, P(final >= 0.9), ends running, model steps.
- Expected sensitivity: about 0.05 at 40-60 states.

**Faster instrument: step-level A/B; structured guidance (registered 2026-10-16, before building).**

The full-loop replays take hours per answer and their outcomes are dominated by crash-or-not. A mechanism that
helps must raise what *one step* does from a given state, so steps are measured directly.

- **Step 1 (offline, no model calls).** For the 40 running pool states, count states and remaining loss in
  entities a guided step can target:
  - (a) whole-value guidance (`_guided_target`: R's print, or R's values <= 1,500 characters);
  - (b) **structured guidance**: the worst entity that ran below 0.9, with the verifier's per-path differences
    for it (data feedback such as `info.abbreviation[0]: 'EST' != 'UTC'`), the first differing stdout lines, and
    the locator's first diverging call, so any size of entity reduces to a few concrete differences.
- **Step 2 (step-level A/B, `scripts/step_ab.py`).** The 40 running states, one step from the frozen start, a
  single call per sample (best-of-k follows as 1 - (1 - p)^k), 4 samples, production system prompt and turn.
  - Arms: **U** (unguided), **GV** (whole-value guidance), **GS** (structured guidance).
  - Each answer goes through the loop's gates (shim, argument order, syntax, imports) and is verified.
  - Per call:
    - realized gain = max(0, objective gain), since the loop rejects a worse candidate;
    - P(the step improves);
    - the change of the targeted entity.
  - **Decision:** a guided arm wins if its mean realized gain against U, paired per state, has a 95% bootstrap
    interval above 0. If both win, the larger effect wins.
- **Step 3 (loop confirmation, only if step 2 has a winner).** The winner as `guided_w1k3` (one chain, best of 3
  per step) against `rewrite_w3` on the 40 running states, 2 samples (160 runs), compared with
  `replay_compare.py`.

The crash fallback's trigger was checked on broom: each branch made one full rewrite, then two culprit repairs
(of `tidy`). The step-level test of the fallback follows the same pattern on the 20 crashing states.

**Step 1 result (2026-10-16, no model calls).** The 40 running pool states, verified at their start:
- **Whole-value guidance (GV):** a target in **27** states; the targeted entities hold **15%** of those states'
  remaining loss.
- **Structured guidance (GS):** a target in **all 40**, holding **25%** of the loss. The locator found a first
  diverging call in 27.
- **Example (farver `spectrum`):** "spectrum[0][0]: 255 != 1.0 (outside tolerance)" plus "the first call where
  your Python departs from R is `decode_colour(rainbow(10))`. R computes [255, 0, 0, 255, 153, 0, ...]".
- **Weaker case (ggplot2 `geom_bin_2d_2`):** only "the difference is in what the entity finally assigns or
  prints".

The guidance is frozen in `work/step_ab/targets.json`. Breaking entities down extends guidance from 27 to 40 states
and from 15% to 25% of the loss in reach of one step.

**Step 2 result (2026-10-16): no guided arm beats unguided; step 3 is not triggered.** 480 steps, 0 errors,
about 70 minutes.

| arm | P(improve) | best of 3 | realized gain/step | followed entity | review rejections |
|---|---|---|---|---|---|
| U | 0.26 | 0.59 | +0.0485 | +0.096 | 16 |
| GV whole value | 0.27 | 0.61 | +0.0581 | +0.123 | **30** |
| GS structured | 0.27 | 0.61 | +0.0515 | +0.085 | 20 |

Realized gain against U, paired over 40 states:
- GV +0.0096 [-0.0070, +0.0306];
- GS +0.0030 [-0.0146, +0.0226].

*Post hoc: before the hardcoding review.*
- Improving candidates: U 57, GV 73, GS 63 of 160.
- Without the review, **GV +0.0239 [+0.0057, +0.0450]** against U; GS +0.0067 [-0.0097, +0.0268].
- Whole-value guidance produces more improving rewrites, but the review rejects twice as many (30 vs 16), which
  cancels the gain.
- **Even unguided, the review discards 16 of 57 improving candidates (28%).**

The rig did not keep the code or the review's reasons, so whether those rejections are literal pasting (correctly
rejected) or false positives of a model-based review is not known. That is the next, cheap question. If they are
false positives, the review gate costs every arm about a quarter of its improvements.

**Is the hardcoding review right? Registered before the run (2026-10-16).** User's condition: pasting R's printed
output or values must never come back in. It was a major flaw in earlier versions, so more than one sample is
checked by hand.

- **Re-run** of the step-level A/B (`step_ab.py run --tag review`), the same frozen guidance, U/GV/GS, 3 samples
  (360 steps).
- **Kept for every improving candidate:** its code, the review's verdict and its reason.
- **On every verified candidate,** a deterministic paste check (`scripts/paste_check.py`, 6 tests). It counts
  literals that match what R *computed* (printed lines of >= 12 characters; numbers with >= 4 significant
  decimals, or ints >= 10,000; strings of >= 8 characters from R's values) and appear neither in the R script nor
  in the Python the candidate came from. Pasted = >= 3 numbers, or >= 1 printed line, or >= 2 strings.
- **Manual check:** I read at least 15 review-rejected and 10 review-accepted improving candidates across the arms,
  each classified as "pasted / computed / other rule"; excerpts go to the user.
- **What follows:**
  - If the review mostly rejects real pasting, the review stays, and guidance is reformulated so it does not
    invite pasting.
  - If it mostly rejects computed code, the review is recalibrated **only** in a way that keeps rejecting what
    the deterministic check and the manual check identify as pasting.
  - No change may let pasting through.

**Review check result (2026-10-16): the hardcoding review is mostly right. Guidance with R's values invites
pasting, and the gain it seemed to bring was largely pasting.** 360 steps (353 verified), 149 improving
candidates kept.

Review verdict against the deterministic check:

| | check: pasted | check: clean |
|---|---|---|
| review rejected | 16 | 31 |
| review accepted | 3 | 99 |

Review rejections per arm: U 10/41 (24%), GV 22/57 (39%), GS 15/51 (29%).

**Manual reading (by me), 20 of the 31 "rejected but clean":**
- **18 real hardcoding:**
  - farver: `if n == 10: return [[255, 0, 0], [255, 153, 0], ...]`, R's `rainbow(10)` for the script's input (5);
  - farver encode: a table of R's HCL values to 6 decimals, commented "we use the known R values" (1);
  - sessioninfo: `"R version 4.6.0 (2026-04-24 ucrt)"` and other R-session facts (7);
  - systemfonts: a glyph-metric table (2);
  - fansi: input-to-output lookup tables, `if x == "hello\033[42;33m world": return "..."` (3).
- **1 false positive:** farver, the review objected to the harness's own data shim.
- **1 borderline:** textshaping's lorem text, constant data from the R package.

**12 accepted candidates (one per script):**
- 10 compute their results;
- 1 borderline (farver's white-point table, package data);
- 0 clear pasting.

**3 "accepted but flagged":**
- 2 are print-layout labels, not pasting;
- 1 is partial hardcoding the review let through: caret's `"Pre-processing: centered (4), scaled (4)"`.

Where both rejected, the check's flags are partly label lines, but the review's reasons are real hardcoding.

**Conclusions.**
1. **The review stays; it is not the bottleneck.** Its rejections are overwhelmingly correct.
2. **Showing R's values (GV) raises hardcoding** (39% of its improving candidates rejected vs 24% unguided). The
   pre-review "+0.024" of GV was largely pasting, so step-level guidance gains about 0 once pasting is excluded.
3. **The deterministic check misses common forms of pasting:** small-integer tables, values rounded from R's
   precision, and input-to-output lookup tables keyed on the script's literals. It also flags print-layout
   labels. It must not be relied on alone.
4. **The review also leaks** (caret's literal "(4)"). Neither gate alone is sufficient.
5. **Part of the remaining loss cannot be reached honestly by a Python translation:** R's session details
   (sessioninfo), font metrics from R's font stack (systemfonts), package data (textshaping lorem, farver white
   points). Pasting is the only way to "fix" those, which is exactly what must not be rewarded.

**Environment sizing and the data shim (2026-10-16, no model calls).**

*Correction (user):* R-session facts, font data and package-internal data are reachable honestly, through the
data shim, as inputs from R's environment. They are not unreachable.

*Sizing.* Entities whose R code reads R's session or system, the clock, or fonts hold **0.8%** of the remaining
training loss (4.9 of 635 points, 14 scripts). Package-data lookups (lorem text, white points) cannot be found by
call name, and only a handful were seen. As a score lever an environment shim is small; its value is removing an
incentive to paste.

*How the shim reaches Gemma.* The turn lists "Data variables (loaded by the data shim)": names, types, columns
and a usage hint. The code holds a managed placeholder line. `remove_shim_overrides` (which strips assignments to
shim names) runs only on seeds, never on the agent's rewrites.

**Finding: the shim pre-loads R's results for variables the script computes itself.**
`collect_shim_needed_names` rule (1), "free variables the script references but does not define", is applied per
entity. A variable defined in one entity and used in another therefore counts as free.

Over the 125 scripts with a shim:
- **114 names are true inputs** (datasets);
- **19 are rule (2)** (RNG or file reads; intended, but RNG is now replayed and could be computed);
- **41 are script-computed values** in 39 scripts, e.g. clock `info <- zoned_time_info(x)`, hms
  `d <- data.frame(hours = 1:3)`, lava `e <- estimate(...)`, timeDate `dts`, `tms`.

**Test:** lava's entity `e` replaced by `pass`. The program still runs, `e` counts as executed, and aggregate
(0.694) and entity score (0.25) are unchanged. Missing code goes unnoticed, and later entities compute from R's
value rather than Python's. The turn also tells Gemma these names are pre-loaded, an incentive not to compute
them.

**Overwrites of true inputs:** 381 of 2,838 agent candidates (13%) in the dev replays assign a true shim input
(e.g. a literal dataset stub). The guard that would strip them is not applied in the loop.

**Re-analysis of the shim finding (2026-10-16), at the user's request, before any fix.**

1. **The lava test was flawed.** The span replaced by `pass` held `def estimate(...)`, not an assignment. A clean
   counterfactual: this translation **never assigns `e`**. Removing `e` from the shim's name list (same code) turns
   exit 0 / aggregate 0.694 into a crash / 0.000.
2. **The classification was too coarse.** It counted an entity named like a variable as a definition, but a bare
   `storms` prints a package dataset. Redone by assignment and order over 125 scripts with a shim:
   - **116** never assigned by the script (true inputs);
   - **3** used before the script reassigns them (true inputs);
   - **19** assigned from RNG or file reads (rule 2);
   - **36 names in 27 scripts computed by the script before any use (the leak).**

   Earlier I reported 41 names in 39 scripts.
3. **Counterfactual on the 21 affected training translations** (same code, leaked names removed from the shim
   list):
   - **3 drop to 0** (tagQuery 1.000, sparsevctrs 0.715, tidyr complete 1.000): the code never computes the value;
   - **13 unchanged**;
   - **5 rise**: lubridate 0.850 to 1.000, reshape2 0.812 to 1.000, xml2 0.714 to 0.821, fansi 0.917 to 0.947,
     clock 0.719 to 0.737.

   In every rise, the leaked variable's own entity goes from 0.25 to about 1.0.
4. **Mechanism of the rises (verifier code):** `_r2py_prev_ns` is set to every name bound before the first entity
   (imports and shim), and checkpoints skip names in that set. A shim-loaded name is never captured, even when
   Python recomputes it correctly.

**So the leak both inflates** (code that computes nothing still runs) **and deflates** (correct code gets no credit
for the variable). The same name-based skip also affects the 3 true inputs that the script reassigns; that is a
separate verifier issue, noted, not fixed here.

Fixes 1-3 go ahead on this evidence:
1. shim rule (1) admits only names not assigned before their first use;
2. the overwrite guard runs in the agent loop for names R never assigns;
3. the turn lists only those inputs, with a plain instruction.

**Shim fixes 1-3 done (2026-10-16).** Tests: `tests/test_shim_leak.py` (4); full suite 967 passed, only the known
`test_stage2` locale failure.
1. **`collect_shim_needed_names` rule (1)** admits a name only if no entity assigns it before its first use
   (`_first_assign_and_use`: an assignment entity defines; a bare reference, e.g. `storms`, uses).
   - Over the dev and training maps: 174 names in 125 scripts become 138 in 103. **Exactly the 36 leaked names
     go**; 116 never-assigned inputs, 3 inputs reassigned after use and 19 RNG/read names stay.
   - Existing translations are corrected as well: their shim blocks keep the old list, but the sidecar no longer
     carries the leaked names.
2. **Overwrite guard:** `remove_shim_overrides` now strips only names R never assigns (`shim_input_names`), on the
   seed path and **in every agent rewrite**, with an outcome stat and a history note. Before, the seed stripped
   all shim names, including legitimate reassignments such as `storms <- head(storms)`, and the loop stripped
   nothing.
3. **The turn** names these inputs: "already loaded when your code runs ... Use them as they are; never assign
   them or write their values as literals."

**Re-verified with the fix** (no model calls), matching the counterfactual:
- lubridate 0.850 to **1.000**, reshape2 0.812 to **1.000** (correct code now credited);
- tidyr complete 1.000 to **0.000**, tagQuery 1.000 to **0.000** (they relied on R's result);
- caret 0.778 unchanged.

**Scores from before this fix are not comparable with scores after it** for the 27 affected scripts. Comparisons
within one experiment stay valid: both arms had the same shim.

*Not fixed, noted:* the verifier's name-based skip (`_r2py_prev_ns`) still hides recomputed values of the 19
RNG/read pre-loads and the 3 reassigned inputs. RNG draws are now replayed, so the RNG pre-loads could be dropped
and computed; a separate, tested change.

**RNG pre-loads and pre-loaded names in the checkpoints (2026-10-16).**

*Dropping the RNG pre-loads: not done; the evidence argues against it.* Counterfactual on the 6 translations with
RNG pre-loads (same code, pre-load removed): 4 crash, 2 unchanged, 0 rise. The translations do not draw the
numbers themselves. For `x <- rgamma(...)` the pre-loaded value *is* R's draws, which the replay treats as inputs
anyway, so these pre-loads are not a back door like the 36 computed values. Removing them would break working
translations without making anything more honest.

*Recording a pre-loaded name the code replaces (`r2py/stage4/verifier.py`).*
- **Change:** the checkpoint now records a data value bound before the first entity once, at the entity where the
  code replaces the object (identity changed). R records it where the script assigns it. Untouched pre-loaded
  values stay unrecorded, as before. Built-ins are reached via `_r2py_builtins`, because scripts shadow them (lava
  assigns `id`; a first version broke on exactly that and was caught by the comparison below).
- **Tests:** `tests/test_shim_leak.py`, 3 checkpoint tests.
- **Before/after on 87 translations** (60 pool, 4 targets, 24 dev; previous checkpoint code patched in for
  "before"):
  - **caret_s3 0.409 to 0.742 and pROC print 0.818 to 0.961.** The entity `data` goes 0 to 1: R's `data(X)` loads
    `X`, and the Python code replaces the shim's copy.
  - recipes kpca +0.002.
  - Noise: openssl `ec_dh` (random keys; the same old code gives 0.677 and 0.675) and caret createDataPartition
    (-0.004). ragg's crash in the first "before" run did not reproduce (0.450 three times), so it was a flaky run.
  - The 4 translations I expected to change (they reassign a pre-loaded name) did not.
- Full suite: 970 passed, only the known locale failure.
- *Latent weakness, not changed:* the checkpoint and serializer code look up 24 built-ins by name. A script
  defining one at top level would break recording, but 0 of 259 training translations does.

**Offline ceilings of per-entity acceptance (option 1) and freezing verified entities (option 2)**
(`work/offline_merge_freeze/`, no model calls). Data: the 120 `rewrite_w3` baseline runs of the S1 and feedback
replays, 1,274 candidates, each step replayed against the loop's best state at the time; start states re-verified.
- **Damage:** 200 candidates (16%) damage an entity that was verified (>= 0.95) in the best state. 144 (11%)
  improve some entity but were rejected as a whole.
- **Freeze, 55 spliceable cases:** better than the loop's step in 6, **all 6 in one script** (xml2 `xml_cdata`:
  best state and candidate both crash; restoring one entity makes it run, 0.75). The variant crashes in 35, and
  in 7 freezing turns a running candidate into a crashing one.
- **Merge, 71 spliceable cases:** better in 1. **The merged version crashes in 65 (92%)**: improved entities
  depend on changes elsewhere in the same candidate.
- **Conclusion: neither option has a general ceiling worth building.** A rewrite's improvements and damages are
  not separable per entity. That is also why one-entity answers lost score in the prompt-load runs.

**Why improvements cannot be lifted out of a rewrite (2026-10-16, offline, no model calls).** The user's question:
understand the dependency, then turn it into a structural change.

1. **Crash causes of the 66 crashing entity merges:** NameError 51, Indentation/SyntaxError 14, AttributeError 1.
   Concentrated in 6 scripts (caret 21, clock 18, hms 14, broom 11).
2. **Connected change sets do not help.** A def-use closure (the improved entities plus the changed definitions
   they use, in other entities or outside every entity, transitively) still crashes in 64 of 67. The closure grew
   beyond the improved entities in only 11.
3. **Restored entity markers are not the cause.** On candidates that kept every marker themselves: merge 32/37
   crash, closure 33/36. The candidate itself crashes in 23 of those 37: many "improvements" sit in programs that
   crash as a whole.
4. **Reading the cases shows the mechanism: every rewrite redesigns the program's internal structure.**
   - broom: the best state's helper is `r_tidy_factanal(fa, data)`, the candidate's `r_tidy(fit)`. The improved
     line `fit.loadings[:, i]` works only inside the candidate's design. Both entities are fragments inside a
     helper's body.
   - hms: the improved code calls a helper (`format_hms`) the best state lacks or defines differently.
5. **Measured over all 1,270 parseable candidates:**
   - 1,055 have helper functions (median 5 per program);
   - **52% (545) change the helper interface** (rename, drop, add, or change parameters);
   - when they do, only 43% of the best state's helpers survive unchanged.
6. **Same interface, still failing:** with an unchanged helper interface, 4 of 16 merges run (best state runs in
   15, candidate in 13). All 12 failures are 2 scripts:
   - hms 11: `d = ...` sits inside another R entity's Python range (`d$hours`) or is nested;
   - lava 1: a dict cut in half.

   **The R-entity-to-Python-range mapping does not match the program's real units.**

**Conclusion.** The loop's unit of change is the whole file, and Gemma uses each rewrite to re-architect: 52% change
the helper interface. An improvement is valid only inside the design it was written in. That is why per-entity
acceptance, freezing, one-entity answers and closure merges all failed. The units R gives us (entities) are not the
units of the Python program (helpers and the statements that define each variable).

Two structural consequences:
- **(a) A stable design.** The harness keeps the program's helper layer fixed between steps once its callers
  verify: verified helpers move into a harness-managed block, like the runtime block, and edits change them only
  explicitly. Verified callable functions were used 8 of 8 times.
- **(b) Python-native edit units.** An analysis tool that maps each R entity to the Python statements and helpers
  that actually implement it (def-use, not marker ranges). Edits, merges and guidance then address these connected
  units instead of marker ranges.

**Translation manual, stage 1: one-step test of a frozen design. Registered before building (2026-10-16).** Plan:
`experiments/TRANSLATION_MANUAL_PLAN.md`.

- **Treatment (`F`):** the best program's helper interfaces (top-level `def` / `class` name and parameters) are
  frozen for the step.
  - The turn lists them ("fixed: call them, do not rename them or change their parameters"). The harness enforces
    it (`r2py/harness/manual.py`): a frozen helper the candidate dropped, renamed away from, or re-parameterised
    is put back with the best program's definition.
  - Bodies with an unchanged interface and new helpers are allowed.
- **Control (`U`):** today's step.
- **Setting:** `scripts/step_ab.py`, the 40 running training-pool states, production turn and system prompt, the
  loop's gates and the hardcoding review, 4 samples per arm (320 steps), concurrent.
- **Measured per step:**
  - P(improve) (better by the search objective and passing the review);
  - realized gain;
  - **damage**: entities verified (>= 0.95) in the best state that fall below 0.95;
  - attempted interface changes (before enforcement) and restorations;
  - the candidate's code (kept for an optional cross-sample merge check).
- **Stop rule (from the plan):** stop if `F` improves less often than `U` (paired over states, 95% interval
  entirely below 0) **and** does not reduce damage (interval not entirely below 0). Otherwise, go to stage 2
  (two-step retention).

**Manual stage 1 result (2026-10-16).** 320 steps, 0 errors; 31 of the 40 states have helpers (median 2).

| | U | F (frozen, enforced) | F - U, paired over states |
|---|---|---|---|
| attempted helper-interface change | 14.6% | **5.1%** | |
| P(improve) | 0.263 | 0.287 | +0.025 [-0.044, +0.094] |
| **P(damage a verified entity)** | **0.280** | **0.276** | +0.010 [-0.048, +0.081] |
| realized gain per step | +0.0455 | +0.0322 | -0.013 [-0.032, +0.002] |

The harness restored helpers 8 times in F.

- **Registered decision: go on to stage 2.** F does not improve less often.
- **But the premise is weakened.** Freezing cuts interface changes by two thirds, yet damage to verified entities
  is unchanged at 28% of steps. Within one step, damage does not come from helper interfaces.
- Before stage 2 is built on that premise, the saved candidates are checked for what actually damages verified
  entities: their own code rewritten, an upstream change, or a crash.

**What damages verified entities, and does the loop lose progress? (2026-10-16, no model calls.)**
- **The 272 cases of a verified entity damaged in stage-1 candidates:**
  - **63% the candidate crashes** (blocked 140, crashed in it 30);
  - 29% the entity's own code was rewritten;
  - 9% its code is unchanged but something upstream changed.

  15% of candidates crash although the start runs, the same in U and F. F has more crash-blocked cases (86 vs 54):
  restored helpers sometimes clash with the candidate's new calls.
- **Retention across accepted steps of today's loop** (`rewrite_w3` S1, feedback and crash-first replays): 285
  accepted transitions carried 994 verified entities and **lost 10 (1.0%)**; 8 transitions lose any.
  Acceptance already filters damage out. **Progress accumulates in the sequential loop.**

**Consequence for the manual plan: its premise is refuted.** The claim "progress cannot accumulate because every
rewrite redesigns the program" was wrong. Redesign (52% of rewrites) only explains why candidates cannot be
combined with each other (merging), which the plan already made optional. Stage 2 (retention) has no room: the
loop retains 99%. The manual is not built further. `r2py/harness/manual.py` stays as a tested utility.

**What does limit the loop:** steps that find no improvement (P = 0.26) and stall. Damage is a wasted step, not lost
progress, and 63% of it is new crashes.

**Correction: best-of-k is not 1 - (1 - p)^k (2026-10-17, no model calls).** The step-level tables above give
"best of 3" from the formula, which assumes every call has the same chance. Pooling the U arms of the three
step-level runs (11 calls per state, 40 running states):

| P(no improvement in k calls from one state) | assuming independence | measured per state |
|---|---|---|
| k = 1 | 0.741 | 0.741 |
| k = 3 | 0.407 | **0.576** |
| k = 9 (a stall of 3 steps at 3 calls) | 0.067 | **0.391** |

- Calls from the same state are independent draws, but states differ hugely. **14 of 40 states never improved in
  11 calls** (36% of the remaining loss); 10 improved in 1-2 calls (26%); 16 in 3 or more (38%).
- Best of 3 is about 0.42, not 0.59. More samples per step help only the middle group; the 14 stuck states stay
  stuck however often they are sampled, under width or per-step sampling alike.

**3 per step against width 3 (registered 2026-10-17, before the run).**
- **Question:** with about the same model calls, does one chain that samples 3 rewrites per step and builds on the
  best beat three independent chains? Width keeps three designs alive; the chain shares every improvement and
  stalls less (measured per state: 3 calls fail together in 0.58 of steps, against 0.74 for one call).
- **Arms, concurrent:** `rewrite_w3` (today) and `rewrite_w1k3` (one chain, `guided_k=3`, `guided_mode="off"`: 3
  unguided whole-file rewrites of the same turn; the best by the search objective among those that pass the gates).
- **Built for it:** the hardcoding review goes down the improving drafts best first and keeps the first that
  passes; before, only the best draft was reviewed, and the highest-scoring draft is the likeliest to paste. Drafts
  get the shim-input guard before they are scored, as the loop applies after choosing. Tests in
  `tests/test_entity_repair.py`. `rewrite_w3` is unchanged.
- **States and samples:** the training pool (`--pool training`, 40 running + 20 crashing), 2 samples each, 240
  runs. Estimated 4-6 hours.
- **Primary:** mean final score per state, `rewrite_w1k3` - `rewrite_w3`, paired, bootstrap interval and Wilcoxon
  (`scripts/replay_compare.py`), on the 40 running states. **Decision:** 3 per step wins if the interval lies above
  0; loses if below 0; otherwise no difference at this size.
- **Secondary:**
  - the 20 crashing states, reported apart;
  - P(final >= 0.9), stalled share, ends running;
  - model calls per run (agent actions + extra drafts + reviews), so the compute match is checked, not assumed;
  - the 14 never-improve states against the rest (expected: no difference there for either arm).

**3 per step, first attempt aborted (2026-10-17).** OpenRouter refused calls with `in_flight_budget_exhausted`
from early in the run (92 agent calls, 5 audit, 4 review). A failed call ends the agent loop, so the 75 finished
runs are not valid; they are kept as `work/replay_k3/results_invalid_credits.jsonl`. Rerun after credits are
topped up, unchanged protocol.

**What the 14 never-improve states have in common (2026-10-17, no model calls).** 14 of 40 running pool states
improved in none of 11 unguided calls; they hold 36% of the running states' remaining loss. Each start was
re-verified and its losing entities traced to the item that costs the score:

| cause | states | share of all running-state loss |
|---|---|---|
| R checkpoint run failed, no per-entity R bundles (xml2, systemfonts) | 2 | 3.4% |
| verifier compares a value R itself does not reproduce (openssl: `aes_cbc_encrypt` defaults to `iv = rand_bytes(16)`; R's `serialize` bytes) | 1 | 2.8% |
| verifier compares shiny/bslib tag objects by R's internal list (html dependencies), Python's are "uncomparable" and score 0 | 3 | 12.0% |
| environment: R session info, system fonts, font metrics (sessioninfo, textshaping x2) | 3 | 4.8% |
| harness trap: the shim loads R's data frame as a dict; the turn says "use as they are"; the guard strips `diamonds = pd.DataFrame(diamonds)`; 8/8 saved ggplot2 candidates pass the dict to plotnine and crash | 1 | 3.1% |
| R object model without a Python counterpart (gtable grid grobs) | 1 | 1.9% |
| within reach of a model (farver `rainbow`: Gemma pastes the RGB table, rightly rejected; bslib: never prints the HTML; caret RNG resampling) | 3 | 7.8% |

**28% of the running states' loss (11 of 14 stuck states) is out of reach of any model** because of the harness,
the verifier or the environment; 8% is model-limited.

**The checkpoint failures are corpus-wide.** `run_script_checkpointed` (`r2py/stage1/runner.py`) swallows the
failure and returns no per-entity bundles. **34 of 249 script maps (14%) have none, 9 of the 60 pool states.**
Then every entity is scored on script-wide fallbacks and the feedback cannot say which entity is wrong.
Reproduced from R's own errors:
- **12** the checkpoint call is inserted after an entity that ends inside a multi-line pipe or `+` chain and becomes
  part of it (`unused argument ("group_by")`; ggplot2: "Can't add `.r2py_cp(...)` to a <ggplot>");
- **18** a checkpoint between base-graphics calls breaks the device (`plot.new has not been called yet`; ragg:
  device no longer open);
- **2** an entity id with quotes is escaped in the wrong order (quote before backslash): R syntax error;
- **2** unclear (e1071 `read_matrix_csr`, pROC).

**Feedback noise.** Script-level files, env and warnings items (bslib's woff2 font cache, `TCLLIBPATH`, `TZDIR`,
`GIT_ASKPASS`) are repeated in every losing entity's feedback, although the per-entity score does not use them.

Not fixed yet: no harness edits while a run is pending, and every fix changes scores (re-verify the pool after).

**Harness fixes from the never-improve analysis (2026-10-17).**
- **R checkpoint injection** (`r2py/stage1/runner.py`):
  - checkpoints only at statement boundaries (`_statement_boundary_rows`, tree-sitter: the innermost node spanning
    the boundary is the program or a braced block). Entities that end inside a pipeline, an argument list or an
    `if (cond)` line get no checkpoint (no own R bundle) instead of breaking the run;
  - graphics: the device is no longer closed at the checkpoint of a drawing entity; its pages are flushed just
    before the next new page (`before.plot.new` / `before.grid.newpage`, prepended to the fingerprint hooks) or at
    the end of the run, so low-level calls of later entities still draw on the open plot;
  - entity ids: backslash escaped before the quote; checkpoint file names drop characters Windows forbids
    (`_cp_file_id`, same rule on the Python side).
- **Python checkpoint injection** (`r2py/stage4/verifier.py`): never inside a multi-line string (it parses, so the
  parse check missed it; xml2's `etree.fromstring('''...''')` lost its root tag and crashed once R had bundles).
- **Old data shims** (`refresh_data_shim`, applied when the verifier activates the shim): the binding line is
  rewritten in place so R data frames load as pandas DataFrames. A first version rebuilt the block, made it 4
  lines longer and shifted every Python checkpoint below it (entity line maps are computed before activation):
  8 states fell by up to 0.40 and 3 rose by up to 0.55, all artifacts. The line-preserving version changes the
  12 shim states it was checked on by at most 0.04 (and verification noise, below).
- **Prompt:** shim data frames are described as pandas DataFrames, not "dict ... Usage: pd.DataFrame(name)".
- **Stored R bundles refreshed** for the 38 script maps the injection fix changes (`scripts/refresh_entity_bundles.py`):
  the 34 without bundles, and 4 whose checkpointed entities or figure attribution changed (broom, recipes x2,
  rmarkdown; their old bundles credited a figure to every entity). The other 215 were re-run and compared: 169
  identical, the rest differ only where R itself varies (temp names, keys, times, unseeded fits); kept as stored.
- **Tests:** `tests/test_checkpoint_injection.py` (9, three of them run R). Suite: 990 passed, the known locale
  failure.

**Pool re-verified** (60 states, the pool definition unchanged): mean start 0.388 -> 0.410; one state that crashed
now runs (ragg `agg_webp_anim`); 15 change by more than 0.01, mostly the refreshed ones (xml2 0.79 -> 0.55: it was
scored on script-wide fallbacks; systemfonts, shape, ragg, recipes up). Some differences predate today
(caret `caret_s3` 0.41 -> 0.75 is the 2026-10-16 RNG/shim fixes; `rows_v3` is older). Start scores across
2026-10-17 are not comparable.

**Open, found on the way: verification is not deterministic.** The same source verified 6 times: purrr
`attr_getter` 0.591 four times, 0.63 and 0.454 once (`pluck` 1.0 -> 0.5, `obj1` 0.25 <-> 0.487); timeDate 0.769
and 0.869. Present with the old shim too. Paired designs absorb part of it, but it adds noise to every arm.

**Verification noise, traced (2026-10-17).**
- **The noise reported above came from my offline scripts, not from the loop.** They verified without
  `note_reference`, so every verification asked a model to map entities to lines (sampled at the pinned temperature
  1.0). With the reference noted, as the loop does, the same source scores identically: purrr 8/8, timeDate, xml2
  and recipes 6/6 each. The corrected pool re-verification (sentinels read for all 59 states): mean start 0.385
  -> 0.402, no run/crash flips, 9 states change by more than 0.01, all of them refreshed maps or the 2026-10-16
  fixes (xml2 0.79 -> 0.55, prodlim 0.64 -> 0.50; ragg, caret `caret_s3`, recipes `step_kpca`, pROC, rvest, shape,
  systemfonts up). The earlier claim "verification is not deterministic" was wrong for the loop; the "8 down, 3 up"
  of the first shim refresh was partly this noise on top of the line shift.
- **What the loop does hit:** when a candidate loses its markers so badly that alignment cannot restore them, the
  model mapping runs. Measured offline on the 315 saved stage-1 candidates: sentinels read 228, restored 59, **model
  mapping 28 (9%)**, concentrated in gtable (8/8), pROC `coords` (7/8), recipes `discretize` (5/8), xml2, farver,
  caret, openssl.
- **Change (user's choice):** the mapping is called at temperature 0 and cached on disk per (model, entities,
  source) (`work/mapping_cache/`). **Check: temperature 0 is not repeatable on OpenRouter** — at least 20 of the 28
  candidates got different mappings over 3 calls (farver: `convert_colour` <-> `spec_lab`). The cache makes every
  later verification of a source identical, but the first mapping of a new candidate stays a draw.
- Replay rows now record `verify_paths` (sentinel reuse / restored / model mapping) so that share is measured in
  every run.
- A rare `JSONDecodeError` under parallel verification (bslib, 1 of 60) did not reproduce in 8 parallel runs.

**3 per step against width 3: result (2026-10-17).** 240 runs (the first 173 before credits ran out, 67 after
resuming; 3 runs that ended within 2 minutes of the first refusal were set aside and redone), 0 failed calls in the
kept runs. Harness as fixed on 2026-10-17. Strata by the re-verified start: 41 running, 19 crashing.

| | width 3 (`rewrite_w3`) | 3 per step (`rewrite_w1k3`) |
|---|---|---|
| mean final | 0.690 | 0.665 |
| P(final >= 0.9) | 0.25 | 0.23 |
| ends running | 112/120 | 109/120 |
| agent model calls per run | 12.4 | 12.6 |
| minutes per run | 7.3 | 9.2 |

- **Primary (41 running starts): -0.012 [-0.031, +0.003]**, better/worse/tied 7/11/23, Wilcoxon p 0.23. By the
  registered rule: **no difference at this size.**
- Crashing starts: -0.053 [-0.132, -0.002], 1/6/12, p 0.04. All states: -0.025 [-0.053, -0.004], p 0.03.
- The compute match held (12.4 vs 12.6 calls). 90% of steps had 3 distinct drafts. The review went down the drafts
  in 20 of 183 reviewed steps (`passed_later`); in 22 all improving drafts were rejected.
- The 14 never-improve states stay near-stuck in both arms (mean gain +0.026 vs +0.034; improved 5/28 vs 6/28); on
  the other running states width gains more (+0.169 vs +0.147).
- Model mapping in the loop: 146 of 1382 verifications (11%) under width, 121 of 1420 (9%) under 3 per step, as
  measured offline.
- **Reading:** sharing every improvement in one chain does not beat three independent chains at the same calls;
  on crashing starts width is better, consistent with independent chains trying different crash fixes. Width 3
  stays the default.
- **Cost:** the last 67 runs cost $4.26 ($0.064 per run), so the whole test about $15.

**Check of the 3-per-step result (2026-10-17, user's question; from the saved trajectories, no model calls).**
- Setup verified: the drafts are compared against the current best (`report` is updated on acceptance); the chosen
  draft is re-verified from the cache (same score as at selection); 90% of steps had 3 distinct drafts; the
  compute match held (12.4 vs 12.6 calls); budget stops 11 in each arm.
- **The mechanism works:** a step improves the best 40.0% of the time under 3 per step, 33.7% for a single call
  under width 3; improving steps per chain 1.68 vs 1.37. (Best of 3 independent calls would give 71%; the
  per-state heterogeneity measured earlier predicted about 42%.)
- **Per-chain finals** reconstructed from the trajectories (exact for 96% of runs): one width chain 0.637, the
  3-per-step chain 0.665, width 3 (best of its three chains) 0.690. 3 per step beats one chain by **+0.029
  [+0.009, +0.050]**; width's selection among three finished chains is worth more (+0.053 over one chain).
- **Why the expectation was wrong:** it compared per-step success with a single chain. Width 3 is not one chain:
  it keeps the best of three finished programs, and the chains differ most where it matters (crashing starts:
  different crash fixes). Sharing improvements inside one chain gains less than selecting among three.

**Combination width 3 x 3 per step, estimated offline (2026-10-17, no model calls).** Best of k independent chains
is what width computes, so it is estimated from the existing runs: 6 single chains per state (two width-3 runs) and
2 three-per-step chains, averaging the best over all k-subsets.

| mean final | model calls | running (41) | crashing (19) | all (60) |
|---|---|---|---|---|
| 1 chain | ~4 | 0.701 | 0.499 | 0.637 |
| 3 per step | ~13 | 0.709 | 0.571 | 0.665 |
| width 3 | ~12 | 0.728 | 0.620 | 0.694 |
| best of 2 three-per-step chains | ~25 | 0.720 | 0.643 | 0.696 |
| best of 6 single chains (width 6) | ~25 | 0.744 | 0.687 | 0.726 |

- At equal calls, 2 three-per-step chains lose to 6 single chains: -0.030 [-0.063, -0.004] (running -0.023
  [-0.050, -0.002]); they only match width 3, at twice its calls.
- Extrapolated, the combination (3 three-per-step chains, ~37 calls) lands near 0.71: above width 3, below width 6
  at less cost. Extra calls are better spent on more independent chains.
- Caveats: best of 6 rests on the 6 chains per state (unbiased, noisy); chain finals are reconstructed from
  trajectories (exact for 96% of runs). The $4 check (one more three-per-step run per state) was not run, by the
  user's decision. Width stays 3 by default; width 6 is a cost decision (+0.032 estimated, twice the calls, same
  wall time).

**Is the plateau a local optimum? (2026-10-18, from the 3-per-step trajectories, no model calls.)** Share of steps
that improve the best, by the number of failed steps just before:

| | after 0 fails | after 1 | after 2 |
|---|---|---|---|
| running starts, width 3 | 0.38 | 0.25 | 0.09 |
| running starts, 3 per step | 0.49 | 0.19 | 0.05 |
| crashing starts, width 3 | 0.43 | 0.32 | 0.31 |
| crashing starts, 3 per step | 0.52 | 0.45 | 0.24 |

- Running starts are stuck: after two failures a step almost never improves; more patience would not help. Part
  of that plateau is the harness ceiling (28% of the never-improve states' loss unreachable).
- Crashing starts are cut off by the stopping rule (stop after 3 failures in a row): after two failures the chance
  is still ~0.3. Caveat: chains that fail twice are disproportionately the hard states.
- The loop is greedy search with large random jumps (whole-file rewrites), strict acceptance and early stopping;
  its levers are step size, acceptance, patience and restarts (width).

**Agreed plan, in this order (user, 2026-10-18):**
1. **Raise the harness ceiling** (free to measure: change, then re-score saved translations offline): compare
   shiny/htmltools tag objects by their rendered HTML instead of R's internal list (12% of the running states'
   loss in the never-improve analysis); the environment shim for R session facts and fonts (4.8%).
2. **Patience on crashing programs:** `max_stalls` 5 while the best program crashes, 3 otherwise (a global 5 is a
   config change but wastes steps on running programs, where a third try succeeds 5-9% of the time). One modest
   run.
3. **Running starts:** keep equal-scoring programs (drift across plateaus) or restart after the plateau (from the
   current best with a fresh history, or from a new seed). Needs design and a run.

**Ceiling lever 1a: tag objects (2026-10-18).**
- **Correction:** the "12% of the running states' loss" for tag objects was the whole loss of the three states
  where tag comparison failed, not the part it causes. Only 8 of 249 scripts hold tag objects (4 pool states).
- **Cause:** an R adapter already rendered `shiny.tag` to HTML, but tag lists (`fluidPage`, `page_fillable`,
  `tagList`: class `shiny.tag.list`) fell through to the generic list and were serialised as htmltools' internal
  list (dependency records). Now they render to HTML too (`r2py/stage0/effects/data.py`); stored R values refreshed
  for the 8 scripts (`scripts/refresh_entity_bundles.py --main`); test added.
- **Effect on the stored translations: none to speak of** (shiny `actionButton` 0.552 -> 0.559, the rest
  unchanged). The comparison is now real ("text forms differ (similarity 0.42)" instead of "uncomparable"), but
  the text tier scores similarity^4, and in several translations Python has no variable of R's name (`ui` passed
  inline to `App(...)`, or renamed `app_ui`), which the model can fix.
- **Open question:** py-shiny renders different markup from R's shiny/bslib (similarity 0.4-0.6 for the same UI).
  Full credit needs R's exact HTML; whether an idiomatic py-shiny translation should get it is a scoring decision,
  not a bug.

**Ceiling lever 1b, part one: temp paths (2026-10-18).** 23 of 249 scripts read the environment, in three groups:
temp files (9), session reports (sessioninfo, 5), fonts (6; Python can read the same font files, so these are
within reach of a translation and need no harness change).
- **Temp paths:** `file <- tempfile(fileext = ".jpeg")` was compared as data, R's random path against Python's,
  so the entity always scored 0. Now two absolute paths inside a temp directory with the same extension compare
  equal (`r2py/stage4/comparators/data.py`, `tests/test_temp_paths.py`).
- Re-scored stored translations: ragg `agg_jpeg`/`ppm`/`tiff`/`webp` +0.25 each, e1071 `write_svm` +0.30, sass
  `as_sass` (pool) +0.125, utf8 `output_utf8` +0.075; ragg `webp_anim` (crashes) and sass `sass_import` unchanged.
- Session reports are left for a decision: R's `session_info()` lists R's version and packages; a faithful
  Python translation reports Python's environment, so the comparison measures nothing a translation can do.
- **Session reports (user's decision): excluded from scoring.** Entities whose R code calls `session_info`,
  `sessionInfo`, `platform_info`, `package_info`, `python_info`, `external_info`, `session_diff`, `Sys.info()` or
  `R.version` have no active dimensions, leave the aggregate and get no feedback (`r2py/stage4/verifier.py`,
  `tests/test_env_report.py`). Corpus-wide the rule matches only the 5 sessioninfo scripts; besides the report they
  hold only `library()` calls, so all 5 now score 1.0 (0.56-0.81 before) and in effect leave the evaluation.

**Lever 1 summary:** tag lists ~0 on stored translations (the ceiling is raised but the translations do not use it
yet); temp paths +0.25-0.30 on 5 scripts, +0.125 and +0.075 on two more; session reports removed (5 scripts).
Fonts need no harness change. Scores across 2026-10-18 are not comparable for these 18 scripts.

**Lever 2, patience on crashing programs: continuation test (registered 2026-10-18, before the run).**
- **Reach:** of the 360 width-3 chains of the 3-per-step run, 44 (12%, 11 states) stopped by stalling while their
  best program still crashed. Only these can gain: on a running program the rule changes nothing.
- **Test:** each of the 44 chains continues from its stalled best program for 2 more steps (patience 5 instead
  of 3), production turn, width 1, fresh history (an approximation: the original chain's step notes are not
  replayed). ~90 model calls, under $1.
- **Measures:** per chain, P(the 2 extra steps improve the best) and P(the program then runs); per width-3 run,
  the final with the continued chains substituted (best of 3 by the search objective), against the recorded
  final, on the crashing starts.
- **Decision:** adopt crash patience 5 if the mean run-level gain on crashing starts has a 95% bootstrap interval
  (over states) above 0; otherwise keep 3.

**Lever 2 result (2026-10-18): patience stays 3.** 44 chains continued, 0 errors, $0.27.
- 6 of 44 improved in the 2 extra steps (14%), and all 6 now run; mean gain per continued chain +0.079.
- Run-level gain on crashing starts (20 states): **+0.027 [+0.000, +0.067]**; running starts 0, as expected.
- By the registered rule (interval above 0) not adopted: the lower bound is exactly 0.
- The per-try success (~7%) is far below the 0.31 seen after two failures: these chains had already failed three
  times, and they continued with a fresh history. The earlier "~0.3 after two failures" overstated what a 4th and
  5th try give.
- The change would be cheap (only crashing chains spend the extra steps), so it stays a candidate if a larger
  sample is ever run alongside another test.

**Lever 3, running starts on a plateau: continuation test (registered 2026-10-18, before the run).**
- **States:** every width-3 run of the 3-per-step replay whose start runs and whose final is below the 0.9
  threshold: 62 runs, 32 states, mean plateau score 0.660. The program each run returned continues for 3 more
  steps (width 1), once per arm, concurrently:
  - `continue3` (**restart**: fresh history, strict acceptance);
  - `continue3_eq` (**accept equal**: the same, and a running candidate that scores the same as the current one
    and differs from it becomes the current program; it still counts as a stall). New loop option
    `accept_equal` (off by default), tests in `tests/test_entity_repair.py`.
- **Primary:** gain over the plateau per state (mean over its runs), bootstrap interval over states. An arm is
  adopted as a plateau step if its interval lies above 0. Secondary: accept equal - restart, paired per state;
  number of equal moves taken.
- ~124 continuations, about $1.60.

**Lever 3 result (2026-10-18): the plateaus of running starts are real.** 124 continuations, 0 errors, $1.13.

| arm | runs improved | equal moves | gain over the plateau (32 states) |
|---|---|---|---|
| restart (fresh history) | 11/62 | 0 | +0.0037 [+0.0003, +0.0098] |
| accept equal | 10/62 | 47 | +0.0060 [+0.0004, +0.0133] |

- Accept equal - restart, paired: +0.0023 [-0.0008, +0.0067]: no difference.
- **Formally both pass the registered rule** (intervals above 0), **but the effect is about half a point** on a
  plateau of 0.66, for 3 more calls per run (about +25% cost). Not made a default; `accept_equal` stays an option.
- Equal moves were taken often (47 in 62 runs) and did not lead anywhere: moving sideways on the plateau finds no
  better program either.
- **Conclusion of the three levers:** for running starts the search mechanics (patience, restarts, acceptance)
  are not what limits the score; the remaining loss is in what the model can produce and in the harness ceiling.
  Width (independent chains with final selection) remains the only search lever that pays.

**New default for crashing starts (user's decision, 2026-10-18; commit 7468ccf).** When the program the agent starts
from crashes: 6 independent chains instead of 3 (`DEFAULT_CRASH_WIDTH`), and a chain stops after 5 failed steps in
a row while its best program still crashes, 3 otherwise (`DEFAULT_CRASH_STALLS`, `reason(crash_stalls=...)`).
Running starts are unchanged (a running program is never replaced by a crashing one, so the patience never applies
to them). Manifest keys `agent_crash_width`, `agent_crash_stalls`. Tests in `tests/test_loop.py`,
`tests/test_entity_repair.py`.

**Measured run (registered 2026-10-18, before the run):** replay policy `rewrite_w3_crash6p5` on the 20 crashing
starts of the training pool, 1 sample each (2 samples would cost ~$6.60, more than the $4.83 left), current harness.
Its step curve replaces the estimated width-6 line for crashing starts in the chart (`In-Loop Score Curves`), and
the run's final is compared with the two width-3 runs of 2026-10-17 re-scored with the current harness (not
concurrent: a day apart; reported as such).
- **Result (2026-10-18):** 20 runs, 0 errors, $1.89; all 20 started crashing and ran 6 chains; 15 of 120 chains
  stopped on the 20-minute wall-clock budget (4 workers x 6 chains share the machine). On the chart's 19 crashing
  states: mean final **0.646**, against the width-6 estimate 0.671 and the recorded width-3 finals 0.624:
  **+0.022 [-0.039, +0.085]**, better/worse/tied 8/2/9 (a day apart, one sample). The gain is not established at
  this size; the default stays as decided. Chart updated: the measured line replaces the estimate in the
  "Start crashes" view, the estimate is kept dotted.
- **Time limit for 6-chain runs doubled (user's request, 2026-10-18):** the agent's wall-clock budget is shared by
  chains running in parallel; when the crash width applies, the budget is multiplied by
  `DEFAULT_CRASH_BUDGET_FACTOR = 2.0` (manifest key `agent_crash_budget_factor`; replay applies the same factor).
  Production: 45 min -> 90 min per crashing script (heldout manifest), replay 20 -> 40 min. Not re-measured.

**Crashing-start default, re-run with the doubled time limit (registered 2026-10-18, before the run):** the same
20 crashing states, 1 sample, policy `rewrite_w3_crash6p5`, 40-minute budget (`work/replay_crash6p5_b2`). Its curve
replaces the first measured run in the chart; the estimated width-6 line is removed (user's request).
- **Re-run result (2026-10-19), 40-minute limit:** 20 runs, 0 errors; only 1 of 120 chains stopped on the budget
  (15 with 20 minutes). 4 runs caught by an overnight laptop sleep (22:04-08:02; their wall-clock budget ran through
  the gap) were discarded and redone (`work/replay_crash6p5_b2/discarded_sleep`). Cost $3.45 including the
  discarded runs. On the chart's 19 crashing states: mean final **0.676** (first run 0.646; the width-6 estimate was
  0.671), against the recorded width-3 finals 0.624: **+0.052 [-0.021, +0.126]**, better/worse/tied 9/3/7 (two days
  apart, one sample). Chart: the re-run's line replaces the first; the estimated width-6 line is removed (user's
  request).
