---
id: fs.file-create
package: fs
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# fs.file-create

## Guidance
Translate R `file_create` (FunctionCall from fs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "12d795fb", "r_snippet": "file_create(\"foo\")", "py_snippet": "with open(\"foo\", \"w\") as f:\n    pass\n\n# is_file(\"foo\")", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
