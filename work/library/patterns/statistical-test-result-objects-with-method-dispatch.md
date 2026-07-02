---
id: statistical-test-result-objects-with-method-dispatch
package: base
confidence: tentative
seed: false
created: 2026-07-02
last_review: 2026-07-02
tie_count: 0
---

# statistical-test-result-objects-with-method-dispatch

## Guidance
Create a custom class to hold test results as attributes (dw, p, r, alternative), then implement separate tidy() and glance() functions that accept these objects and return formatted DataFrames. Use setattr() to dynamically attach result values to the object.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
