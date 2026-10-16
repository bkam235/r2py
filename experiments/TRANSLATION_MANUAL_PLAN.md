# Translation manual: plan for real in-loop gains

> **Status 2026-10-16: stopped after stage 1.** Freezing helper interfaces cut interface changes from 15% to 5% of
> steps, but damage to verified entities stayed at 28%; 63% of that damage is new crashes. Today's loop already
> keeps 99% of verified entities across accepted steps (994 carried, 10 lost), so progress accumulates and the
> premise below ("progress cannot accumulate") is refuted. Redesign only blocks *combining* candidates, which is
> optional. Details: `IMPROVEMENT_PLAN.md`, entries of 2026-10-16.

*Written 2026-10-16, after the agreement in conversation. Evidence for every claim below is logged in
`experiments/IMPROVEMENT_PLAN.md` (entries of 2026-10-11 to 2026-10-16); the offline material is in
`work/offline_merge_freeze/`.*

## 1. What we learned (why this plan)

**Telling Gemma more does not change what it writes.** About ten experiments moved nothing measurable:
- prompt-delivered library, lessons and oracle;
- corrected feedback (+0.020, n.s.);
- system-prompt trimming (S1 +0.017 in the loop, n.s.);
- guided steps with R's values or structured differences (+0.010 / +0.003 per step, n.s.; the apparent extra gain
  of value guidance was largely pasting);
- crash-first (-0.019, within day drift).

What has worked: width (several candidates, the verifier picks: +0.144), and code the harness owns and verifies
(verified functions used 8/8).

**One step improves the program about 26% of the time, whatever we tell Gemma.** 30% of steps make it worse (13%
catastrophically), and loops stop by stalling (62% of branches) with two thirds of their time unused.

**Improvements do not accumulate, because every rewrite redesigns the program.**
- 52% of rewrites change the helper interface (rename, drop, add, re-parameterise); then only 43% of the helpers
  survive unchanged.
- An improvement is valid only inside the design it was written in.
- So per-entity acceptance (65/71 merges crash), freezing verified entities (wins in one script only), one-entity
  answers (adopt more, score worse) and def-use closure merges (64/67 crash) all failed.
- **The units R gives us (entities) are not the units of the Python program** (helpers, and the statements that
  define each variable). Code for one R entity can sit inside another's range (hms `d` in `d$hours`).

## 2. The approach: three layers

1. **The R program** (fixed): the logical structure, i.e. the order of the entities, the variables each defines
   and uses, the functions R defines.
2. **The translation manual** (harness-maintained, structured and machine-checkable, with natural-language notes
   for Gemma). Per R entity:
   - the Python unit that implements it: statements and helpers, found by def-use, not by marker ranges;
   - **helper interfaces**: name, parameters, return type;
   - **data representations**: e.g. "`d`: pandas DataFrame, column `hours`".

   The harness derives the manual from the program deterministically. Gemma may *propose* amendments, never
   rewrite it implicitly.
3. **The Python code**, edited within the manual's units.

**Enforcement (the "insurance"):** every edit is checked against the manual's invariants (frozen interfaces,
representations, assignment of code to entities). A violation is undone or the edit rejected, as the harness
already restores the data shim. A deliberate interface change goes through an explicit action that updates all
call sites at once (the tool for connected changes); only then does the manual change.

**Why enforcement and not just text:** the evidence says text in the prompt is not followed; harness-owned
structure is.

**Merging is not required.** With a fixed design, gains compound through the ordinary sequential loop: accepted
steps build on each other. Merging stays an optional amplifier later (recovering partial improvements from
rejected candidates, combining parallel branches).

## 3. Open design decisions

- **When the manual freezes.** Not before the program first runs and its entities verify; before that, rewrites
  stay free. Freezing too early would lock in a bad design.
- **When redesign is allowed.** Some designs are wrong (hms: code of different entities tangled). A deliberate,
  verified redesign step when the loop is stuck, never a side effect of every rewrite.
- **What counts as a representation change.** A type change of a variable that later entities use. The
  `entity_types` from R and Python's captured types give the reference.

## 4. Build and test, in order (each stage has a stop rule)

All tests on Gemma, with concurrent arms, using the crash-aware status (`objective.entity_status`) and the
training pool (`replay.py --pool training`) where a loop is involved.

**Stage 1: one-step test of a frozen design (about 1 h).**
- *Build:* minimal enforcement only. Freeze the current best program's helper interfaces (top-level `def`/`class`
  names and parameters) for one step. A candidate that changes them is restored where possible, otherwise
  rejected. Reuse `scripts/step_ab.py` (frozen states, production turn, the loop's gates, the review).
- *Arms:* free (today) vs frozen.
- *Measure:*
  - P(step improves);
  - share of steps that damage an entity verified (>= 0.95) in the best state (16% today);
  - how often the structure still changes (attempted interface changes);
  - optional: whether improvements from different samples of the same step now merge.
- *Stop rule:* if the frozen arm improves less often **and** does not reduce damage, stop and rethink.
- *Necessary, not sufficient:* this shows no downside, not compounding.

**Stage 2: two-step retention test (about 2 h).**
- Step 2 starts from step 1's best result.
- *Measure:* **retention**, the share of entities improved in step 1 that are still improved after step 2, frozen
  vs free.
- *Stop rule:* no better retention under the frozen design, no further build-out.

**Stage 3: the manual proper.**
- *Build:*
  - the analysis tool: entity to Python unit by def-use, helper interfaces, representations;
  - the explicit "change interface" action that updates all call sites;
  - the freeze point (first verified run) and the explicit redesign step.
- *Test:* unit tests on the cases seen offline (broom `r_tidy`, hms `d` / `d$hours`, lava `e`).

**Stage 4: loop confirmation.**
- A concurrent replay, manual + enforcement vs today's loop, on the training pool (60 states, about 0.05
  detectable).
- Primary: final score per state, paired, split by running and crashing starts.

## 5. Kept in mind, not in this plan

- **Environment shim:** R session facts and package-internal data supplied through the shim under a strict
  whitelist; data objects, never function results. Small as a score lever (0.8% of loss), but it removes an
  incentive to paste.
- **Adaptive sampling when stuck** (best of 3 per step instead of stopping): modest expected gain (+0.02-0.03).
- **Pasting safeguards:**
  - the hardcoding review stays (18/20 manual rejections correct);
  - `scripts/paste_check.py` is a measuring instrument, not a gate. Its known gaps are small-integer tables,
    rounded values and input-keyed lookup tables; it also flags print labels;
  - guidance must never hand Gemma R's values verbatim.
- **Measurement rules learned:**
  - concurrent arms only (a day-apart baseline drifted 0.01-0.02);
  - report running and crashing starts apart;
  - prefer step-level tests to loop replays for screening;
  - re-verify scores after any verifier fix. The shim-leak fix (2026-10-16) changed scores for 27 scripts;
    comparisons across that date are invalid.
