---
id: unlink-to-pathlib
package: 
confidence: tentative
seed: false
created: 2026-06-15
last_review: 2026-06-15
tie_count: 0
---

# unlink-to-pathlib

## Guidance
R's unlink() removes files matching a glob pattern. In Python, use pathlib.Path.glob() to find matching files and pathlib.Path.unlink() to remove them, which is more robust than glob.glob() + os.remove() and matches R's behavior more closely.

## Evidence
- 34ab01c45818 → score 0.090 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "env", "old_code": "pattern = f + \"_*.rds\"\nfor file in glob.glob(pattern):\n    try:\n        os.remove(file)\n    except OSError:\n        pass", "new_code": "import pathlib\nfor file in pathlib.Path(os.path.dirname(f)).glob(os.path.basename(f) + \"_*.rds\"):\n    try:\n        file.unlink()\n    except OSError:\n        pass", "score_delta": 0.09, "script_id": "34ab01c45818"}
