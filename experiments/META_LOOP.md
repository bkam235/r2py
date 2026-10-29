# Meta-loop: the cycle protocol

How the harness is improved, one question at a time. Written 2026-10-25 from the cycles of 2026-10-11 to 2026-10-25
(the log is `IMPROVEMENT_PLAN.md`); a session that runs a cycle follows this file. In Claude Code the
project skill `/meta-cycle [question]` (`.claude/skills/meta-cycle/SKILL.md`, local, not in git) starts a cycle by
this protocol, one cycle per session.

## Two loops

- **The ground loop** (r2py, Gemma 4 31B): translates one script, minutes per script. Its behaviour is a set of
  options with defaults in `r2py/loop.py` (`DEFAULT_*`) and the manifest.
- **The meta-loop** (a person and a strong model, days per cycle): changes the harness. It touches the ground loop
  through three interfaces only:
  - **settings, meta -> ground:** a change is built behind an option that is off by default; adopting it flips the
    default. Nothing else reaches production translations;
  - **telemetry, ground -> meta:** results rows, trajectories, `run_manifest.json`, the health report;
  - **versions, both ways:** every run row carries the scorer version (`r2py/scoring.py`) and a policy name
    (`default_2026_10_20`); the curves carry the scorer version they were re-scored with.

## The objective

The meta-loop exists to raise **the plateau of the production default**: the mean final score of the current
`default_<date>` policy on the 60 training states under the open scoring epoch (0.792 in epoch 6), confirmed on the
held-out pool. Every cycle says what it does to that number:
- a **harness change** can raise it; the replay or test measures by how much;
- a **scorer change that corrects scores** (false losses removed) moves the plateau without any translation changing;
  the curve rebuild shows it, and it is a correction of the measurement, not a gain;
- a **scorer change that only corrects feedback** (false messages, false timeouts, curves unchanged) can raise the
  plateau only through what the model does with the cleaner feedback, and that is unmeasured until the default is
  replayed (step 9).

Measurement hygiene is not an end in itself: a scorer question is worth its share of the gap, like any other.

## Roles

| who | decides or does |
|---|---|
| **Person** (owner) | which question a cycle asks; accepting a scorer change (opening an epoch); every spend of credits; the decision rules; adopting a default; what is published |
| **Strong model** (proposer, analyst) | observes, diagnoses, proposes, builds and tests code, registers the test, runs it once approved, analyses by the registered rule, records |
| **Gemma** | the ground loop only; never proposes harness changes |

**Off limits to the proposer without the person's acceptance:** the scorer (`SCORER_PATHS` in `r2py/scoring.py`:
effect capture, sandboxes, verifier and comparators, R checkpointing, shim, entity attribution, objective), the
stored R ground truth (`work/reverify/script_maps`), the pools (`experiments/pools/`), the decision rules, and a
registered test's design once data exists. A scorer change is never made to move a result; it is made because a
measurement is wrong, shown on a concrete program.

## Standing rules

- **Verify before asserting.** A cause is a hypothesis until an offline test (no model calls) shows it.
- **No edits to `r2py/` while a run is in progress**; the run would mix two harnesses.
- **No pasting back:** R values or R stdout never reach the model's program; `paste_check` in the health report
  watches for it.
- **Cheap first:** the cheapest instrument that can answer the question (ladder below). Record the cost of every
  run.
- **The laptop stays awake during runs** (the person's setting; the run guard marks rows that overlapped a sleep
  `invalid` and reruns them on resume).
- **Commit with the trailer** `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; never commit keys.

## The cycle

### 0. Before starting

```bash
git status
```
```bash
python scripts/scoring_epoch.py status
```
The tree is committed, the scorer is `same` as the open epoch (if `CHANGED`, finish the scorer track first), and no
run is in progress. Compare the scorer version of the latest replay of the production default with the open epoch:
if a replay of the default makes sense (step 9), say so before choosing the question.

### 1. Observe

Start from the latest health report of the latest run (`<run_dir>/health_report.md`; `replay.py` writes it at the
end of every run) and the curves (`experiments/figures/inloop_curves.html`). With `--deep` the report re-verifies
the never-improving starts and lists their losing entities (no model calls):
```bash
python scripts/health_report.py work/replay_default --deep
```
Start from the report's score gap: how much of 1 - mean final sits in states that never improve, in states that
improve and stop below 0.9, and in runs that end crashing, by start stratum, and which states hold the most of it.
Then look for causes: never-improving states, crash types, model-mapping share, paste flags, stop reasons, strata
that lag. A candidate question names the part of the gap it addresses and how many points of it it could reach at
most (the states it touches times what they lose); candidates are ranked by that reach, the chance it holds and the
cost of finding out.

### 2. Diagnose

Trace one loss to its cause on a concrete program, and show the cause with an offline test. Then classify it:
- **measurement** (the scorer is wrong: the October checkpoint, temp-path, tag-list and globals faults) -> scorer
  track;
- **behaviour** (the loop or the model does something it should not, or misses a lever: width, patience,
  conversation) -> harness track.

### 3a. Scorer track (person-gated, no model calls)

1. Change the scorer and add a unit test that fails before and passes after.
2. Check the reference set (147 programs, about 5-10 minutes):
   ```bash
   python scripts/scoring_epoch.py check
   ```
   If the report says the R-capture code changed, re-capture the maps (`scripts/refresh_entity_bundles.py`) and
   check again.
3. Show the person the report (`work/scoring/check_<time>.md`): which programs moved, entity by entity, and why
   that is the intended effect. Unintended moves send the change back to step 1.
4. On the person's acceptance:
   ```bash
   python scripts/scoring_epoch.py accept --note "<what changed and why>"
   ```
   This opens the epoch and rebuilds the curves (all ~1,400 programs re-scored, about 20 minutes, no model calls).
5. Record (step 9): which earlier results the change qualifies, and the curves before and after; and whether the
   change corrected scores (the plateau moved) or only feedback the model sees (the plateau did not move, and its
   effect on translations is unmeasured).

### 3b. Harness track

1. Build the change behind an option that is off by default, with a unit test. `scoring_epoch.py status` must still
   say `same`; if it does not, the change touches the scorer and belongs in 3a.
2. Smoke-test it on one state.

### 4. Register, before any data

Append an entry to `IMPROVEMENT_PLAN.md` (the reasoning) and a record to the experiment registry
(`experiments/registry.jsonl`, the structured fields), and commit both before the run:
- hypothesis and the option it tests;
- instrument, pool (training), arms, samples, workers;
- primary metric, secondary metrics, strata (running and crashing starts apart);
- decision rule and tier (below), and what each outcome will mean;
- cost estimate and the run guard budget;
- the analysis command.

```bash
python scripts/registry.py register spec.json
```
The spec holds `id, question, track, instrument, pool, arms, baseline, primary, rule, est_cost, plan` (the plan
entry's bold heading) and optionally `option, samples, strata, run_dir, analysis, budget, note`; the registry adds
the date, the scorer version and the commit.

An extension (more samples) is registered the same way before it runs, and the rule is applied once to the
combined data. No other look at the data in between.

### 5. Test

Ask the person to approve the spend, naming the instrument, the estimated cost and the budget. Then run with the run
guard (`--budget USD`, `--reserve` default $0.50). Instruments, cheapest first (costs measured in October):

| instrument | answers | cost |
|---|---|---|
| offline re-verification, `scoring_epoch.py check`, `health_report.py --deep` | measurement questions | free |
| `step_ab.py` (one step from frozen states) | does a step do better? | $0.45-0.55 for 240-360 steps |
| `two_step.py` (two steps, step 1 shared) | does step 2 use step 1's outcome? | about $0.80 per 120 trials |
| `continue_stalled.py`, `continue_plateau.py` (continue saved chains) | patience, plateaus | $0.30-1.20 |
| `replay.py --pool training` (the whole loop, frozen starts) | the end-to-end effect | $4.35 for 60 runs of the default |

All write the common format that `expkit.py analyze` reads. Before the run ends nothing in `r2py/` changes.

### 6. Decide

Apply the registered rule once:
```bash
python scripts/expkit.py analyze <results.jsonl> --baseline <arm> --metric <metric> --rule free
```
(`--rule costly --best-of K` for a change that costs calls.) Then complete the record; the actual cost comes from
the run guard's manifest:
```bash
python scripts/registry.py result <id> --estimate "<primary estimate>" --decision "<adopted | not adopted | extended | descriptive>" --heldout pending
``` The decision rules (the person's, 2026-10-20):
- **free and reversible** (no extra model calls, no stratum harmed, switchable): adopt if P(effect > 0) >= 0.9 in
  the bootstrap over states;
- **costs extra calls:** adopt only if it beats the same calls spent on sampling (best of k) with P >= 0.9;
- **claims** about effects keep the 95% interval.

### 7. Confirm on the held-out pool

A change that passed on the training pool is run once more on the 46 held-out states (`--pool heldout`; frozen in
`experiments/pools/heldout.json`) with the same instrument and the same rule, registered like any test. Pass: the
rule holds again. Fail: the default does not change, and the result is recorded. Either way the original record's
`--heldout` becomes `passed` or `failed` (the held-out run is a record of its own). The held-out pool has only 6
crashing starts, so a crash-specific change cannot be confirmed there; that is stated, and the person decides.

### 8. Adopt

On the person's sign-off: flip the default in `r2py/loop.py` (and its manifest key), add a replay policy named
`default_<date>` for the new production default, add a test that the default is on. Adopted changes stay under
watch: a later run that contradicts them reverts them by the same rule.

### 9. Record

- The registry record is complete (`python scripts/registry.py show <id>`): decision, held-out status, the commit
  of the result.
- The result in `IMPROVEMENT_PLAN.md` under the registered entry: numbers with intervals, actual cost, decision,
  caveats; corrections of earlier readings where the result changes them; the plateau of the production default
  before and after, and why it moved or did not.
- The run's health report stays in its run directory.
- **Replay of the default.** A replay of `default_<date>` on the training pool (`replay.py --pool training`, about
  $4.35, registered as descriptive) is the only measurement of the objective itself. It makes sense when:
  - a default changed (the new default's curve is unmeasured), or
  - since the latest replay of the production default, one or more accepted epochs corrected feedback the model sees
    without moving the curves (their effect on translations is unmeasured), or
  - the next question would be ranked by a gap table that no longer describes the current harness.

  The strong model points this out, says which of these applies and what the replay would tell, and asks; the person
  decides. A new line in the curves needs a change to `scripts/learning_curves.py`.
- When the plateau table or the lessons change, update the top section of `IMPROVEMENT_PLAN.md`, the figure and the
  page "In-Loop Score Curves".
- Commit.

## Not yet built

- **Telemetry gaps:** the trajectories do not record each step's cost or exactly which feedback was shown.
