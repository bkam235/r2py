---
id: r-sample---for-shuffling-indices
package: dplyr
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# r-sample---for-shuffling-indices

## Guidance
R's `sample(nrow(x))` and `sample(ncol(x))` for shuffling should be translated to `np.random.permutation(len(x))` and `np.random.permutation(len(x.columns))`, then applied via `.iloc`.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
