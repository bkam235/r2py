---
id: xfun.cache-rds-to-pickle
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# xfun.cache-rds-to-pickle

## Guidance
Translate R's xfun::cache_rds() to Python by implementing a simple file-based cache using pickle. The function should accept **kwargs to handle extra parameters like rerun=True, check for existing cache files (unless rerun is True), and return the computed result. This preserves the caching behavior and allows recomputation when requested.

## Evidence
- 34ab01c45818 → score 0.561 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "env", "old_code": "def compute():\n    \"\"\"Placeholder function that takes one second.\"\"\"\n    time.sleep(1)", "new_code": "def compute(**kwargs):\n    \"\"\"Caches computation result with 1 second sleep.\"\"\"\n    import pickle\n    import hashlib\n    \n    # Create a simple cache key\n    cache_key = hashlib.md5(str(kwargs).encode()).hexdigest()\n    cache_file = f + '_' + cache_key + '.rds'\n    \n    # Check if cached result exis", "score_delta": 0.5612, "script_id": "34ab01c45818"}
