# Meta-loop: the cycle protocol

How the harness is improved, one question at a time. Written 2026-10-25 from the cycles of 2026-10-11 to 2026-10-25
(the log is `IMPROVEMENT_PLAN.md`); a session that runs a cycle follows this file. In Claude Code the
project skill `/meta-cycle [question]` (`.claude/skills/meta-cycle/SKILL.md`, local, not in git) starts a cycle by
this protocol, one cycle per session.

## Two loops

- **The ground loop** (r2py; agent DeepSeek V4.1 Flash, seeds, review, audit and mapping Gemma 4 31B, as of
  `default_2026_11_12`): translates one script, minutes per script. Its behaviour is a set of options with defaults
  in `r2py/loop.py` (`DEFAULT_*`) and the manifest.
- **The meta-loop** (a person and a strong model, days per cycle): changes the harness. It touches the ground loop
  through three interfaces only:
  - **settings, meta -> ground:** a change is built behind an option that is off by default; adopting it flips the
    default. Nothing else reaches production translations;
  - **telemetry, ground -> meta:** results rows, trajectories, `run_manifest.json`, the health report;
  - **versions, both ways:** every run row carries the scorer version (`r2py/scoring.py`) and a policy name
    (`default_2026_11_12`); the curves carry the scorer version they were re-scored with.

## The objective

The meta-loop exists to get good translations from a cheap agent model (the person's decision, 2026-11-14). Its
primary metric is **the plateau of the production default**: the mean final score of the current `default_<date>`
policy on the 60 training states under the open scoring epoch, confirmed on the held-out pool. The secondary metric
is **the share of finals >= 0.95**, reported next to it. `default_2026_11_12` under epoch 11: plateau 0.881
training, 0.907 held-out; share >= 0.95 0.550 training (33 of 60), 0.652 held-out (30 of 46).

**The cost class.** The agent's model stays in the cost class of DeepSeek V4.1 Flash: about its cost per translated
script or less (the default's training replay: $2.06 for 60 runs, about $0.035 per script). A result with a model
outside the class is explanatory: it shows how much of the gap is the model's, and it cannot become the default.

"Gain" and "correction" below apply to both metrics. Every cycle says what it does to them:
- a **harness change** can raise them; the replay or test measures by how much. A model choice for one of the
  loop's roles (agent, seeds, review, audit, mapping) inside the cost class is a harness change: the largest single
  gain so far (+0.065 on the plateau, 2026-11-12) was the agent's model;
- a **learning change** (the model trained on translations the loop verified) can raise it the same way, through a
  policy with another model; the replay or test measures by how much;
- a **scorer change that corrects scores** (false losses removed) moves the plateau without any translation changing;
  the curve rebuild shows it, and it is a correction of the measurement, not a gain;
- a **scorer change that only corrects feedback** (false messages, false timeouts, curves unchanged) can raise the
  plateau only through what the model does with the cleaner feedback, and that is unmeasured until the default is
  replayed (step 9).

The harness and learning changes are **gains** (the loop writes better programs); a scorer change that corrects scores
is a **correction** (the same programs measured differently); one that corrects only feedback is a correction that
may lead to a gain, unmeasured until a replay. The meta-loop
exists for gains. Measurement hygiene is not an end in itself: a scorer
question earns a cycle when the fault blocks a gain, by hiding real progress from the model or misleading its
feedback, and it is ranked by what it unblocks, not by the points it moves. That a scorer check is free is no reason
to prefer it; harness questions have instruments of $0.30-1.20.

### Headroom

The objective is worth pursuing only while the pool leaves room a test can see. The **reachable gap** is 1 - mean
final minus the points held by states the gap ledger (step 1) classes as out of reach (measurement faults not yet
fixable, values no faithful program can match). The **noise floor** is what one replay of the default moves by on
its own: about ±0.03 on the 60-state plateau (`width6-running-pool`, 2026-11-06); on the share >= 0.95 about ±0.09
(the same two replays, 46 running starts: 0.261 vs 0.174, 4 states flipped; under Gemma with the stop threshold at
0.9), since the share moves in steps of one state (1/60 = 0.017). When the reachable gap is below about twice the
noise floor, gains on this pool can no longer be confirmed by the instrument that measures the
objective, and the cycle says so before proposing any lever: it states the reachable gap and proposes a new
objective (a harder or larger pool, the share of finals >= 0.95 as primary, cost per verified script, or another the evidence
supports). Changing the objective or the pools is the person's decision. States the ledger still has as `unknown`
are counted both ways, so the reachable gap is a range.

**Stall trigger.** When the latest three cycles together added less than 0.01 of gain to the plateau (corrections
not counted),
the next cycle opens with bets (step 1) and an objective proposal, not with a lever or a scorer question.

## Roles

| who | decides or does |
|---|---|
| **Person** (owner) | which question a cycle asks; accepting a scorer change (opening an epoch); every spend of credits or training compute; the decision rules; the training data's audit; adopting a default (a tuned model included); what is published |
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
that lag. `--deep` shows what the scorer says about the start programs, so on its own it finds measurement faults;
for the states holding the most of the gap, also read the trajectories (`<run_dir>/trajectories/`): what each step
tried, its outcome and crash, its stop reason, and whether the next step used the feedback. Look across states for
behaviour patterns too: candidate crash types, stop reasons, review rejections, step success rates, where the curves
flatten.

**The gap ledger** (`experiments/gap_ledger.md`, committed) holds one row per training state whose default final is
below 0.95: its points of the gap, its class (measurement, out of reach, behaviour, capability, unknown), the evidence
(an offline test, a trajectory, a result) and the cycle that set it. A cycle updates the rows it learns about
instead of re-deriving them from the health report, and the headroom check reads the reachable gap from it. A state
stays `unknown` until a test or a trajectory reading classes it.

The ledger says where the gap is; it is not where questions come from.

**Levers and bets.** A **lever** tunes the loop as it is (an option, a hint, a gate, a scorer fix, patience,
width); past levers gained 0-0.02. A **bet** changes what the loop is or what it is measured on: the model of a role
(agent, seeds, review, audit, mapping), a capability the agent lacks (a tool, a way to inspect or run what it cannot
now), the unit of work or the architecture, the learning track, or the objective and the pool (a role's model only inside the cost class). Every gain above 0.03
so far was a bet (width +0.144, conversation mode +0.05, the agent's model +0.065). Every proposal has at least one
bet. A bet is ranked by its **ceiling** (from a ceiling measurement where one exists, else argued from the evidence),
its cost and its cheapest **kill test** (a few dollars at most, registered first; the full test only if it
survives), not by a chance taken from past levers. Where no ceiling measurement fits the current default (an
oracle hint, a tool the cheap agent lacks), proposing one is a bet; a much stronger agent is explanatory (outside the
cost class). A bet may need more than an option
(a tool, an instrument, a pool); it is built behind an option or policy as usual. Lessons are scoped to the agent
model they were measured under; one measured under another model is a hypothesis to retest, not a bound on a bet.

A lever names the part of the gap it addresses and how many points of it it could reach at most. For a
scorer question that is the states it touches times what they lose. A harness lever usually touches many states a
little: its reach is the share of the gap in the states it touches times a success rate from the nearest past result
measured under the current default's agent (computed from its replay's trajectories, not carried over from an
earlier model: under Gemma a third step after two failures improved 5-9% of the time, under DeepSeek Flash 19% on
running and 45% on crashing starts). Candidates are ranked by **expected gain in the plateau** (reach times the
chance it holds) and the cost of finding out. Every proposal has at least one harness question, or says why there is
none; after two scorer cycles in a row, the best harness question goes first unless a scorer fault is shown to block
it.

A question whose reach on the production default is zero (it explains a policy that is not the default, or a
mechanism no option would change) is an **explanatory** question. It is labelled so, names the decision its answer
would change, and runs at most once in three cycles.

When a large share of the gap is capability, the proposal lists the learning track's next step (3c: data, audit,
train) with its status, even if it is not proposed for this cycle.

### 2. Diagnose

Trace one loss to its cause on a concrete program, and show the cause with an offline test. Then classify it:
- **measurement** (the scorer is wrong: the October checkpoint, temp-path, tag-list and globals faults) -> scorer
  track;
- **behaviour** (the scorer is right and the program is wrong; the loop or the model does something it should not,
  or misses a lever: width, patience, conversation) -> harness track. The trajectories show it: the same mistake
  repeated across steps, crashes in a library's API, chains stopping while gains were still being found, feedback
  that names the difference with no step acting on it, good candidates rejected by a gate. A behaviour cause is shown
  on the trajectories and, where it can be, with the cheapest instrument that calls a model (step 5);
- **capability** (the scorer is right, the feedback names the difference, and the model rarely proposes a correct
  program: varied attempts across steps and chains, none right; more width does not reach it) -> learning track.

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

### 3c. Learning track (person-gated: the data audit and every training spend)

Search with the verifier finds programs better than the model alone writes; training the model on them makes the
next round's search start from a stronger policy (expert iteration). Open question in `IMPROVEMENT_PLAN.md`
(2026-11-05); not yet run.
1. **Data.** Collect verified pairs (R source, final Python, and the trajectory) from finished runs, with their scorer
   version. The training and held-out states of `experiments/pools/` never enter the data, nor other scripts of the
   same Rd example or vignette. Record the count by package and a hash of the data set.
2. **Audit, before any training.** Training exploits the scorer's remaining faults far harder than the frozen model
   does. Read a sample of the highest-scoring pairs for faithfulness (pasting, hard-coded values, behaviour that only
   the comparison accepts) and show the person the audit; a fault found is a scorer question (3a) first.
3. **Train** behind a policy that names the model (`model=...` in a replay policy), off by default; record the base
   model, the data hash and the training settings. Training compute is a spend: gated like a run.
4. Register and test as below, the tuned model against the base model at the same calls. The decision rule for
   tuned models is the person's, set when the first one is registered.

### 4. Register, before any data

Append an entry to `IMPROVEMENT_PLAN.md` (the reasoning) and a record to the experiment registry
(`experiments/registry.jsonl`, the structured fields), and commit both before the run:
- hypothesis and the option it tests;
- instrument, pool (training), arms, samples, workers;
- primary metric, secondary metrics, strata (running and crashing starts apart);
- decision rule and tier (below), and what each outcome will mean;
- **power:** the smallest effect the instrument can resolve at the planned samples (from the interval widths of
  earlier runs of the same instrument), next to the question's maximum reach. If the reach is below it, the test
  does not run as a decision test: add samples, choose a sharper instrument, or register it as descriptive with the
  decision its answer informs;
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
| `replay.py --pool training` (the whole loop, frozen starts) | the end-to-end effect | about $2 for 60 runs of the default (November) |

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

Before asking for the sign-off, audit the finals that gained most: read the 10 final programs of the candidate
policy with the largest gains over the current default for faithfulness (pasted R values, hard-coded results,
behaviour only the comparison accepts) and show the person what was read. A fault found is a scorer question (3a)
first, and the flip waits for it.

On the person's sign-off: flip the default in `r2py/loop.py` (and its manifest key; for a tuned model, the model), add a replay policy named
`default_<date>` for the new production default, add a test that the default is on. Adopted changes stay under
watch: a later run that contradicts them reverts them by the same rule.

### 9. Record

- The registry record is complete (`python scripts/registry.py show <id>`): decision, held-out status, the commit
  of the result.
- The result in `IMPROVEMENT_PLAN.md` under the registered entry: numbers with intervals, actual cost, decision,
  caveats; corrections of earlier readings where the result changes them; the plateau of the production default
  before and after, split into gain and correction, and why it moved or did not.
- The run's health report stays in its run directory.
- The gap ledger rows the cycle learned about are updated.
- **Replay of the default.** A replay of `default_<date>` on the training pool (`replay.py --pool training`, about
  $2, registered as descriptive) is the only measurement of the objective itself. It makes sense when:
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
