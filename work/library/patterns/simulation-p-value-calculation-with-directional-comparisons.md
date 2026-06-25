---
id: simulation-p-value-calculation-with-directional-comparisons
package: broom
confidence: tentative
seed: false
created: 2026-06-25
last_review: 2026-06-25
tie_count: 0
---

# simulation-p-value-calculation-with-directional-comparisons

## Guidance
When computing two-sided p-values from simulations, use <= and >= operators (not < and >) to include boundary cases, and apply the two-tailed formula: p = 2 * min(p_lower, p_upper) with a cap at 1.0.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
