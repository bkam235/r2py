---
id: fs.file-delete
package: fs
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# fs.file-delete

## Guidance
Translate R `file_delete` (FunctionCall from fs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "882ea27b", "r_snippet": "file_delete(\"foo\")", "py_snippet": "if os.path.isfile(\"foo\"):\n    os.remove(\"foo\")\n\n# dir_delete(\"bar\")", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
