---
id: complex_r_model_objects_use_data_shim
package: broom
confidence: tentative
seed: false
created: 2026-06-23
last_review: 2026-06-23
tie_count: 0
---

# complex_r_model_objects_use_data_shim

## Guidance
When R code relies on domain-specific model objects (e.g., from `car::durbinWatsonTest`), do not attempt to reimplement the model fitting and testing logic in Python; instead, include the computed result object in the data shim and load it directly.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
