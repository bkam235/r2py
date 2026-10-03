---
id: base.lapply
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.lapply

## Guidance
Translate R `lapply` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0b66f98f", "r_snippet": "lapply(names(resourcePaths()), removeResourcePath)", "py_snippet": "paths_to_remove = list(resourcePaths().keys())\nresults = [removeResourcePath(p) for p in paths_to_remove]\nif not results:\n    print(\"list()\")\nelse:\n    print(results)", "score": 1.0, "script_id": "shiny__rd_example__resourcePaths_Rd", "n_calls": 2}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "for path in list(resource_paths.keys()):\n    del resource_paths[path]", "new_code": "paths_to_remove = list(resourcePaths().keys())\nresults = [removeResourcePath(p) for p in paths_to_remove]\nif not results:\n    print(\"list()\")\nelse:\n    print(results)", "score_delta": 0.5, "script_id": "shiny__rd_example__resourcePaths_Rd", "r_snippet": "lapply(names(resourcePaths()), removeResourcePath)", "functions": ["base::lapply", "base::names"]}
