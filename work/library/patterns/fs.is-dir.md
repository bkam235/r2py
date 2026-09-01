---
id: fs.is-dir
package: fs
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# fs.is-dir

## Guidance
Translate R `is_dir` (FunctionCall from fs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a7547f90", "r_snippet": "is_dir(\"bar\")", "py_snippet": "print(os.path.isdir(\"bar\"))\n\n# try(file_create(\"bar\"))", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
