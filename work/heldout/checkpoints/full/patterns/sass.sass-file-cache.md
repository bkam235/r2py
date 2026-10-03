---
id: sass.sass-file-cache
package: sass
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# sass.sass-file-cache

## Guidance
Translate R `sass_file_cache` (FunctionCall from sass) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7d2b5d28", "r_snippet": "cache <- sass_file_cache(sass_cache_context_dir())", "py_snippet": "# Define the cache directory (approximating sass_cache_context_dir)\ncache_dir = os.path.join(os.environ.get('TEMP', '/tmp'), 'sass_cache')", "score": 1.0, "script_id": "sass__rd_example__sass_file_cache_Rd", "n_calls": 0}

## Edit Examples
(none)
