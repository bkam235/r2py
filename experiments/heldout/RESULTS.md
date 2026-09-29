# Results — does a trained Pattern Library improve translation scores?

Analysis of the experiment pre-registered in `PREREGISTRATION_2.md`, with deviations logged in
`DEVIATIONS.md`. Raw output: `work/heldout/analysis.json`.

**Everything under "Pre-registered result" was specified before data collection. Everything under
"Post-hoc checks" was computed after seeing the primary p-value and is diagnostic only — none of
it is a test of record, and none of it changes the conclusion.**

## Provenance

| | |
|---|---|
| Harness hash | `5a2b026daa0a` — single value on every scored row |
| LLM settings | `temperature 1.0`, provider pinned `novita/bf16`, no fallbacks, 300 s timeout — single value on every row |
| Checkpoints analysed | `empty` (0 patterns), `half` (107), `full` (155) |
| Training | 256 scripts, 112.0 h, library grown from empty |
| Held-out scripts | 60, never used for training, sha256-verified |
| Scoring runs | 540 attempted, **496 scored**, 44 failed (see *Data completeness*) |
| Infra-crash runs | 0 |
| Share of scored entities the library could inform | **20%** |

---

## Pre-registered result

### Primary hypothesis: not supported

**H1:** the mean score over *targetable* entities is higher with a fully trained library than an
empty one. One-sided paired Wilcoxon signed-rank, α = 0.05.

```
n = 39 paired scripts
mean  empty 0.697  ->  full 0.735      diff +0.038  (SE 0.027)    median +0.000
improved / tied / worse:  15 / 16 / 8
Wilcoxon (greater, zero_method="wilcox"):  statistic = 190,  p = 0.0569
two-sided p = 0.1137      matched-pairs rank-biserial r = +0.377      n_nonzero = 23
```

**p = 0.0569 > 0.05, so H0 is not rejected.** By the criterion set out in advance — *"supported
if the paired Wilcoxon test on Checkpoint 2 vs Checkpoint 0 rejects H0 at α = 0.05 (one-sided)"*
— **this is a negative result.** It is reported as such: no other endpoint, checkpoint pair,
subset or test is promoted in its place.

21 of the 60 held-out scripts had no targetable entity and so could not enter this test. One
further script (`tinytex`) produced no usable run at all. Per stratum (descriptive):

| stratum | n | mean diff |
|---|---|---|
| data_wrangling | 7 | +0.004 |
| date_time | 5 | −0.089 |
| graphics | 5 | +0.064 |
| html | 8 | +0.021 |
| stats_objects | 9 | **+0.157** |
| other | 5 | +0.000 |

### Control: non-targetable entities — the informative comparison

The same contrast on entities the library had nothing for:

```
n = 58 paired scripts
mean  empty 0.715  ->  full 0.716      diff +0.001  (SE 0.011)    median +0.000
improved / tied / worse:  20 / 20 / 18
Wilcoxon (greater):  p = 0.4567      two-sided p = 0.9134      r = +0.020      n_nonzero = 38
```

This is the single most useful number in the experiment. The control is essentially **exactly
null**, while targetable entities moved +0.038 with a moderate rank-biserial of +0.377. Whatever
movement occurred was **localised to the entities the library could act on**, which is what a
real mechanism would look like and which rules out non-specific causes — model drift, prompt
difficulty, time of day, provider variation. The control arm did its job.

It remains descriptive. It does not make the primary test significant.

### Secondary: whole-script aggregate score

```
n = 59 paired scripts
mean  empty 0.683  ->  full 0.683      diff +0.001  (SE 0.013)    median +0.000
improved / tied / worse:  27 / 15 / 17
Wilcoxon (greater):  p = 0.2070      two-sided p = 0.4140      r = +0.141      n_nonzero = 44
by checkpoint:  empty 0.683   half 0.699   full 0.683
trend, n = 59:  non-decreasing 21, strictly increasing 7,  Page L p = 0.1070
```

Flat, as expected: the whole-script score averages over many statements the library cannot
inform, which is exactly why the targetable-entity endpoint was registered as primary.

### Secondary: dose-response

Targetable endpoint across the three ordered checkpoints:

```
empty 0.697   ->   half 0.746   ->   full 0.735
n = 39:  non-decreasing 17, strictly increasing 2
Page's trend test:  L = 476,  p = 0.1825
```

**Not monotonic — `half` scores higher than `full`.** Only 2 of 39 scripts increase strictly at
every step. The trend test does not reject. See *The half-beats-full question* below.

---

## Post-hoc checks (diagnostic only)

### Robustness of the primary effect

| check | result |
|---|---|
| Restricted to the 31 scripts with a complete 3+3 reps | mean **+0.0115**, p = **0.1753** |
| Share of the total mean diff from the top 5 scripts | **81%** (+1.209 of +1.487) |
| Share from the single largest script | 45% (`pROC__geom_polygon_auc_roc`, +0.667) |
| Leave-one-out p range over 39 refits | **0.0212 – 0.0943** |
| Leave-one-out fits with p ≥ 0.05 | **32 of 39** |

The effect leans on a small number of scripts, and **both of the two largest positive
contributors lost repetitions to connection errors** (`pROC` 2/2/3 reps, `ModelMetrics__ppv`
2/2/2). Restricting to scripts with complete data more than halves the mean and moves p to 0.18.
These checks point the *same way* as the registered result — they reinforce a negative
conclusion rather than competing with it.

Note that the mean diff is outlier-sensitive while the Wilcoxon statistic is rank-based; both
point in the same direction (positive, not significant).

### A caution about `stats_objects`

That stratum contributes +0.157 (n = 9) and carries the two largest positive scripts. It is also
the stratum where **30% of scripts have data entities excluded from comparison** as
unserializable model objects (`glmModel`, `rocobj`, `rec`, …; 1,278 such warnings in training).
A large swing in a stratum whose measurement is partly hollow is the least trustworthy kind of
signal here. Until model objects are actually comparable, it cannot be said whether that +0.157
reflects better translation or a measurement artifact.

### The half-beats-full question

Stepwise paired contrasts on the targetable endpoint (all post-hoc):

| contrast | n | mean diff | better / tied / worse | p (greater) | p (two-sided) |
|---|---|---|---|---|---|
| empty → half | 39 | **+0.0487** | 17 / 13 / 9 | 0.0292 | 0.0585 |
| half → full | 39 | **−0.0106** | 9 / 15 / 15 | 0.7964 | 0.4073 |
| empty → full | 39 | +0.0381 | 15 / 16 / 8 | 0.0569 | 0.1137 |

The first half of training accounts for more than the whole. **This must not be read as a
result** — `empty → half` is not the registered contrast, and selecting it after seeing the data
is precisely what the registration forbids. It is recorded because it raises a mechanistic
question worth testing properly.

Three candidate mechanisms were checked, and **none is supported**:

1. **The added patterns are weaker.** No. Translation-example scores are effectively identical
   (in `half`: mean 0.985, median 1.000, n = 119; added `half`→`full`: mean 0.978, median 1.000,
   n = 49). Examples per pattern 1.11 vs 1.02; base-R share 35% vs 33%.
2. **Prompt crowding / cap truncation.** No. The prompt caps at 8 base-R patterns and 5
   corrections, and **no held-out script reaches either cap** at either checkpoint. Matched
   patterns per script: `half` mean 0.83 (max 4), `full` mean 1.17 (max 5).
3. **The newly added patterns actively mislead.** No relationship. Of the 39 scripts, 16 gained
   at least one matched pattern between `half` and `full` and 23 did not:

   | group | n | mean half→full diff | better / tied / worse | two-sided p |
   |---|---|---|---|---|
   | gained a pattern | 16 | −0.0222 | 4 / 7 / 5 | 0.8125 |
   | pattern set unchanged | 23 | −0.0025 | 5 / 8 / 10 | 0.3942 |

   Between groups: Mann-Whitney **p = 0.6381** — no dose relationship.

**Conclusion: the non-monotonicity is most consistent with sampling noise.** At n = 39 with 15
ties, 3 repetitions and temperature 1.0, a −0.011 step is well inside the noise floor, and
`half → full` has two-sided p = 0.41. The experiment cannot resolve the dose-response at this
sample size — which is a statement about its power, not evidence of saturation.

---

## Data completeness

44 of 540 runs failed and are dropped from the means, as registered:

| cause | runs | scripts | handling |
|---|---|---|---|
| Connection errors (transient) | 35 | 13 | Not re-run — see below |
| `tinytex` `win_app_dir()` failure in R | 9 | 1 | Deterministic; retained as failed (DEVIATIONS, Notes) |

A separate 176 runs lost to OpenRouter credit exhaustion **were** re-run before analysis
(DEVIATIONS D3), a decision taken while blind to any test statistic.

The 35 connection failures were **not** re-run. That decision became unavailable once the
primary p-value was known: completing runs because a p-value sits just above threshold is
data-dependent augmentation, regardless of intent. The failures are balanced across checkpoints
(scored runs: empty 164, half 166, full 166), so they add noise rather than bias.

## What this does and does not show

**Does not show:** that a trained Pattern Library improves held-out translation scores. The
registered test does not reject H0, and the robustness checks weaken rather than strengthen it.

**Does not show:** that the mechanism fails. The design was under-covered and underpowered:
only **20% of scored entities were targetable**, 21 of 60 scripts could not contribute at all,
and 16 of the remaining 39 were exact ties — leaving 23 informative pairs. The pre-registration
deliberately claimed no power for this endpoint, and that caution was warranted.

**Does suggest**, without establishing: movement concentrated exactly where the library applies
(+0.038, r = +0.377) against a null control (+0.001, r = +0.020). That is the pattern a working
mechanism would produce, at a sample size too small to confirm it.

**Establishes about the harness itself**, from the training run: only 34% of training scripts
cleared the 0.9 gate and taught the library anything, 90% of the 112 h produced no pattern, 45%
of agent rewrites lowered the score, and 131 of the 155 patterns hold just one example. Coverage,
not the retrieval mechanism, is the binding constraint.

## Implications for the next iteration

1. **Coverage first.** Removing the redundant script-level learning gate (patch 01 in
   `experiments/patches/`) grows the library at the *same* evidence standard.
2. **Repair the agent loop** before adding anything (patches 02–03, then targeted edits). Raising
   the 34% pass rate raises *verified* coverage, which is what the endpoint needs.
3. **Make model objects comparable** (Stage 4) before trusting any `stats_objects` result.
4. **Power the next run for the targetable endpoint.** 39 pairs with 16 ties cannot resolve
   effects of this size. Either raise targetability well above 20% or increase the held-out set.
5. **Do not lower the pattern-inclusion threshold** as a coverage fix — see Stage 5 of
   `experiments/IMPROVEMENT_PLAN.md` for why, and for the version that is testable.
