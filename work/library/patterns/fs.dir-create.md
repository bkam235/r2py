---
id: fs.dir-create
package: fs
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# fs.dir-create

## Guidance
Translate R `dir_create` (FunctionCall from fs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "12d795fb", "r_snippet": "file_create(\"foo\")", "py_snippet": "with open(\"foo\", \"w\") as f:\n    pass\n\n# file_copy(\"foo\", \"bar\")", "score": 0.9667, "script_id": "auto"}
- {"r_hash": "a8986645", "r_snippet": "file_copy(\"foo\", \"bar\")", "py_snippet": "shutil.copy(\"foo\", \"bar\")\n\n# try(file_copy(\"foo\", \"bar\"))", "score": 0.9667, "script_id": "auto"}
- {"r_hash": "4f6d2444", "r_snippet": "file_delete(c(\"foo\", \"bar\"))", "py_snippet": "for f in [\"foo\", \"bar\"]:\n    if os.path.exists(f):\n        os.remove(f)\n\n# dir_create(\"foo\")", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)
