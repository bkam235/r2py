---
id: rdatasets-import-fix
package: 
confidence: tentative
seed: false
created: 2026-06-07
last_review: 2026-06-07
tie_count: 0
---

# rdatasets-import-fix

## Guidance
The rdatasets package in Python does not export rdatasets_data as a named import. Use 'import rdatasets' and access datasets via rdatasets.data(dataset_name) instead of trying to import a non-existent rdatasets_data function.

## Evidence
- dd2e0ea0b08b → score 0.067 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "from rdatasets import rdatasets_data", "new_code": "import rdatasets", "score_delta": 0.0667, "script_id": "dd2e0ea0b08b"}
