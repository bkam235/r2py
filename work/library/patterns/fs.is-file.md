---
id: fs.is-file
package: fs
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# fs.is-file

## Guidance
Translate R `is_file` (FunctionCall from fs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2a69ae5e", "r_snippet": "is_file(\"foo\")", "py_snippet": "print(os.path.isfile(\"foo\"))\n\n# try(dir_create(\"foo\"))", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
