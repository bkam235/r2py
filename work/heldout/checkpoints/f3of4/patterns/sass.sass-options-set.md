---
id: sass.sass-options-set
package: sass
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# sass.sass-options-set

## Guidance
Translate R `sass_options_set` (FunctionCall from sass) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "de0b080b", "r_snippet": "old_options <- sass_options_set(precision = 1)", "py_snippet": "def sass_options_set(**kwargs):\n    global GLOBAL_OPTIONS\n    # R's sass_options_set returns the previous options list\n    old = {\"sass.options\": GLOBAL_OPTIONS[\"sass.options\"].copy()}\n    \n    # If kwargs is empty, we handle based on R logic (though not called here)\n    # Otherwise, update the global sass.options\n    GLOBAL_OPTIONS[\"sass.options\"].update(kwargs)\n    return old\n\nold_options = sass_options_set(precision=1)", "score": 1.0, "script_id": "sass__rd_example__sass_options_Rd", "n_calls": 0}

## Edit Examples
(none)
