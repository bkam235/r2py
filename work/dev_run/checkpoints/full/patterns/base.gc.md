---
id: base.gc
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.gc

## Guidance
Translate R `gc` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d170a525", "r_snippet": "gc()", "py_snippet": "import gc\ngc.collect()", "score": 0.9667, "script_id": "xml2__vignette__modification_s8", "n_calls": 1}

## Edit Examples
(none)
