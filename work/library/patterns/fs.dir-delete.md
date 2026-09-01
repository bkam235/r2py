---
id: fs.dir-delete
package: fs
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# fs.dir-delete

## Guidance
Translate R `dir_delete` (FunctionCall from fs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1452a2cd", "r_snippet": "dir_delete(\"bar\")", "py_snippet": "if os.path.isdir(\"bar\"):\n    shutil.rmtree(\"bar\")", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
