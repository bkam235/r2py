# Pre-registration: Does the Pattern Library improve translation scores?

**Status:** Pre-registered prior to data collection
**Date:** 2026-09-19
**Commit hash at registration:** harness 21bcd7fa3707, manifest 5e8eb2f

## Background

An exploratory chronological analysis of 120 runs (Spearman ρ = 0.071, p = 0.44;
Mann-Kendall p = 0.49) found no statistically significant trend between run order
and translation score. Observed score noise: mean = 0.72, SD = 0.29 (n = 120,
left-skewed). This pre-registered experiment tests the Pattern Library's effect
directly, using a design built to have adequate statistical power at this noise
level, rather than reading a trend off the natural chronological run order.

## Hypothesis

**H1 (primary):** For a fixed, held-out set of scripts never used to update the
Pattern Library, verification scores are higher when the library is fully
trained than when it is empty.

**Direction:** One-sided. We predict library training *increases* scores.

**H0 (null):** No difference in scores between empty-library and
fully-trained-library conditions.

## Design

### Held-out test set
- **N = 60 scripts**, fixed before data collection, drawn from the existing
  harvested corpus.
- **Stratified** across effect types and package domains (data wrangling,
  date-time, graphics/plotting, HTML/reactive, statistical model objects,
  string/text processing, file I/O) so no single domain dominates the set.
- These 60 scripts are **permanently excluded** from Pattern Library training
  for the duration of this experiment. Any pattern derived from a held-out
  script must not enter the library.
- The exact list of 60 script identifiers is fixed in
  `experiments/holdout_set.json`, committed alongside this document.

### Training corpus
- All remaining harvested scripts (existing corpus minus the 60 held out).
- Used to populate the Pattern Library across the checkpoints below.

### Checkpoints
1. **Checkpoint 0 (empty):** Pattern Library reset to empty. Score all 60
   held-out scripts.
2. **Checkpoint 1 (half-trained):** Train the library on a random half of the
   training corpus. Score all 60 held-out scripts again.
3. **Checkpoint 2 (fully-trained):** Train the library on the full training
   corpus. Score all 60 held-out scripts a third time.

Checkpoints are cumulative: Checkpoint 1's library state is a superset of
Checkpoint 0's; Checkpoint 2's is a superset of Checkpoint 1's.

### Repetitions
- Each held-out script is translated and scored **3 times per checkpoint**
  (independent runs, same script, same library state).
- The per-script, per-checkpoint score is the **mean of the 3 repetitions**.
- This is a noise-reduction step, applied identically at every checkpoint.

### Controls held fixed throughout
- Verification layer (Stage 4 scorer) — frozen at its current, already-fixed
  state. No changes during the experiment.
- Model and model version used for translation.
- Temperature/sampling settings.
- Scoring rubric and effect-comparator weights.
- Scripts are scored in **randomized order** within each checkpoint (seed
  logged) to avoid any ordering artifacts.

## Primary analysis

For each of the 60 held-out scripts, compute:

```
Δ = mean_score(Checkpoint 2) − mean_score(Checkpoint 0)
```

**Test:** Paired Wilcoxon signed-rank test on the 60 Δ values.
**Alternative hypothesis:** one-sided, Δ > 0.
**α = 0.05.**

Report both the one-sided and two-sided p-value. Report effect size (mean Δ,
median Δ, and matched-pairs rank-biserial correlation).

## Secondary analysis (dose-response)

Using all three checkpoints per script, test whether score increases
monotonically with checkpoint stage (0 → 1 → 2), treating script as a random
effect (e.g., a mixed-effects model with checkpoint as a fixed effect, script
as a random intercept) or, more simply, a per-script Page's trend test across
the three ordered checkpoints. This is exploratory/confirmatory support for
H1, not the primary endpoint.

## What counts as a positive result

The primary hypothesis is considered supported if the paired Wilcoxon test on
Checkpoint 2 vs. Checkpoint 0 rejects H0 at α = 0.05 (one-sided) in the
predicted direction. The secondary dose-response analysis is reported
regardless of the primary result, for transparency.

## What counts as a negative or null result

If the primary test does not reject H0, this will be reported as such — not
re-analyzed with alternative tests chosen post hoc, not restricted to a
"better-performing" subset of scripts, and not accompanied by a different
headline claim. A null result here does not invalidate the Pattern Library
mechanism in general; it means this design, at this sample size, did not
detect an effect of the hypothesized size, and will be reported with the
power analysis that motivated the design (60 scripts, paired design, minimum
detectable effect ≈ 0.09–0.10 mean score improvement at assumed within-script
correlation r = 0.5).

## Known limitations, stated in advance

- The 60-script held-out set, while stratified, cannot cover every R
  construct; results generalize only to the domains represented in the set.
- Within-script correlation between checkpoints (which determines the
  effective power of the paired design) is assumed, not measured in advance;
  actual power may be higher or lower than estimated.
- The training corpus and held-out set are drawn from the same harvesting
  process and may share stylistic regularities not representative of
  arbitrary real-world R code.
- Three repetitions per script per checkpoint reduces but does not eliminate
  measurement noise from translation stochasticity.

## Deviations from this plan

Any deviation from the design above (change in held-out set, change in
checkpoints, change in primary test, additional post hoc tests) will be
logged in a `DEVIATIONS.md` file with a timestamp and rationale, committed
separately from this document, so the original plan remains visible and
unedited.
