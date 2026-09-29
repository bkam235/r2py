# Patches for diagnoses 1–4

Built from the 112 h training-run log (`experiments/train_stdout.txt`) and
`work/heldout/train_progress.jsonl`. **Nothing here has been applied to the repo.**

Scoring was running while these were written, so the live `r2py/` tree was deliberately left
untouched: editing harness source risks a different `harness_hash()` on any resume, which
would invalidate the experiment.

## Apply, after scoring has finished

```bash
git apply .../01-learn-from-subthreshold-scripts.patch
git apply .../02-agent-loop-efficiency.patch
git apply .../03-unlock-nonrewrite-actions.patch
git apply .../04-wall-clock-budget.patch
python -m pytest tests -q
```

Order matters: 04 touches lines 02 introduces. Applying 01 alone is fine.

## Verification already done

- `build_patches.py` asserts every anchor matches **exactly once** and that all five edited
  files still parse.
- All four apply cumulatively via real `git apply`, and the result is byte-identical to the
  expected tree (`diff -r verify new`).
- `test_patched_fns.py` execs the patched functions in isolation: `_check_syntax` gains the
  offending line, `_parse_action` is byte-identical to the original. All checks pass.
- **Not** verified: the full test suite, and any behaviour needing a live translation run.
  Run `pytest tests -q` after applying. Note 4 tests already fail on the unpatched tree
  (2 in `test_stage0_effects.py`, 1 in `test_stage0_sandbox.py`, 1 in `test_stage2.py`).

## What each patch does

### 01 — learn from sub-threshold scripts (`r2py/__init__.py`, `r2py/heldout.py`)

Removes the **script-level** learning gate. `seed_from_translation` already filters per
entity against `entity_score_threshold`, so gating again on the whole-script score discarded
every verified statement in a script that failed overall — 90% of the run's compute
(101 h of 112 h) produced no patterns.

Includes the necessary guard: `_score_in` returned `float(es.executed_ok)` — i.e. **1.0** —
for an entity with no active dimensions. Executing while producing nothing comparable is not
evidence of a correct translation. Without this guard, removing the script gate would fill
the library with patterns learned from unverifiable statements. Now returns `0.0`.

Expect: substantially more patterns per hour, and a real risk of *more, thinner* patterns.
Worth measuring pattern count **and** mean examples-per-pattern after the first run.

### 02 — agent-loop efficiency (`r2py/harness/agent.py`, `r2py/heldout.py`)

- `max_stalls` 10 → **3** in `DEFAULT_PROTOCOL` (the module default was already 3; only the
  manifest raised it). The best rewrite is first reached at median step 2, mean 4.7 — while
  40% of all rewrite steps happened *after* the best answer was already in hand, and another
  24% in loops that never beat the seed. Reclaims roughly 30–40 h.
- **Catastrophic-rewrite feedback.** 17% of rewrites took a positive score to 0.000. The loop
  always re-prompts with `best_source`, so the bad rewrite was *already* discarded — but the
  agent was never told, and kept iterating against a version it believed was current. It now
  gets an explicit "DISCARDED / REVERTED — the source above is the previous, better version"
  message, and is told to change only the failing statements.
- **Usable syntax feedback.** `_check_syntax` returned only `line 9: invalid syntax`, throwing
  away `exc.text` and `exc.offset`. It now appends the offending source line and a caret.
  (It also silently mis-numbered lines, because `ast.parse` runs on a copy with `# r2py:`
  lines stripped; showing the text sidesteps that.)
- **Correct hint for the 3.10 f-string error** instead of the blanket
  "reserved keywords" guess.

### 03 — unlock non-rewrite actions (`r2py/harness/prompt.py` only)

Action counts were rewrite **1,424** vs probe_r 18, lookup_docs 1, done 10.

**The parser is not at fault** — I checked: `_parse_action` step 0 (`_ACTION_TAG_RE`) already
handles `ACTION: probe_r` / `done` / `lookup_docs` correctly and runs before every fallback,
and *zero* responses failed to parse in the whole run. The cause is the prompt alone:

- "REWRITE FIRST. When the score is low, rewrite immediately." → now scoped to the first step.
- "Keep your analysis to 1-2 sentences. **ALL your output tokens should go to code.**" → this
  actively suppresses planning before a 110-line regeneration. Replaced with a request to
  state, in 2–4 sentences, which entities are failing and what will change.
- Adds an explicit rule that a second *blind* rewrite is the most common way to lose score.
- States the target runtime is **CPython 3.10**, where an f-string expression may not contain
  a backslash (legal from 3.12). 14 rejections were this alone — the model writing valid
  modern Python for an older target.

### 04 — wall-clock budget (`r2py/harness/agent.py`, `r2py/loop.py`, `r2py/heldout.py`)

`reason(..., budget_s=None)`, checked at the top of each step; threaded through
`run_loop(agent_budget_s=...)` and `DEFAULT_PROTOCOL["agent_budget_s"] = 2700` (45 min).

A step-count cap would never have caught the worst cases: `fansi__strwrap_ctl` burned
**10.7 h in 6 rewrites** (~107 min/step), `ragg__agg_capture` 10.2 h in 12. Three scripts ate
26 h between them and none reached threshold.

**Limitation:** the check is at step boundaries, so a single pathological verify can still
overrun the budget. Interrupting mid-verification would be far more invasive. Separately,
~107 min for one step is itself unexplained and worth instrumenting — the budget caps the
symptom, not the cause.

## On your hypothesis about over-constraining

You asked whether the constraints are preventing valid Python, since Gemma 4 normally writes
it fine. The evidence says **yes, partly** — though not by forbidding anything directly:

- The prompt already *contains* correct rules for both R-mimicry traps (positional-before-
  keyword, reserved-keyword kwargs, lines 159–167). They were violated anyway: the auto-fixers
  fired **328 times** (255 arg-order, 73 keyword) and 227 rewrites were still rejected for
  syntax. Adding more rules is not working.
- Truncation is **not** the cause (2 events in the whole run).
- The structural driver is this pairing: *"The rewrite MUST be the COMPLETE file… if the
  current translation is 300 lines, your rewrite should be roughly 300 lines too"* together
  with *"ALL your output tokens should go to code"*. Every single step forces a full
  regeneration of ~110 lines (median) with planning suppressed. That is simultaneously the
  syntax-error generator and the reason 45% of rewrites lose score: the model must reproduce
  working code perfectly in order to change three lines of it.

Patch 03 relaxes the token-suppression half. **The full-file-rewrite half is the deeper
problem and I have not patched it** — a targeted-edit action (replace one entity / apply a
diff) is a real design change, in the same class as approach 5, and is the single highest-value
follow-up. Sketch: a `replace_entity` action taking an entity id and its new Python body,
spliced using the existing `r2py:entity` sentinels and `rebuild_entity_line_map`; the machinery
for locating entity spans already exists in `stage2/stitch.py`.

## Pre-registration impact

01, 02 and 03 all change what the library learns or how well it translates, so a run using
them is **not** comparable to the current one and needs a new pre-registration. 04 changes
only where compute is truncated, but it too alters outcomes on slow scripts.
