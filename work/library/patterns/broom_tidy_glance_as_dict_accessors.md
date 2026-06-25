---
id: broom_tidy_glance_as_dict_accessors
package: broom
confidence: tentative
seed: false
created: 2026-06-23
last_review: 2026-06-23
tie_count: 0
---

# broom_tidy_glance_as_dict_accessors

## Guidance
R `broom::tidy()` and `broom::glance()` on model objects should be translated as Python functions that accept a dict (loaded from the data shim) and return a `pd.DataFrame` by accessing the dict's keys directly.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
