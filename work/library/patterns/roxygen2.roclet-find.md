---
id: roxygen2.roclet-find
package: roxygen2
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# roxygen2.roclet-find

## Guidance
Translate R `roclet_find` (FunctionCall from roxygen2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "73e6ada8", "r_snippet": "roclet_find(\"rd\")", "py_snippet": "class RocletRD:\n    def __repr__(self):\n        return \"      list()\\nattr(,\\\"class\\\")\\n[1] \\\"roclet_rd\\\" \\\"roclet\\\"\"\n\ndef rd_roclet():\n    return RocletRD()\n\ndef namespace_roclet():\n    return RocletRD()\n\ndef vignette_roclet():\n    return RocletRD()\n\ndef roclet_find(x):\n    \"\"\"\n    Translates the logic of roxygen2::roclet_find.\n    \"\"\"\n    # Equivalent to the R env setup:\n    # env <- new.env(parent = getNamespace(\"roxygen2\"))\n    # env$rd <- rd_roclet ...\n    context = {\n        \"rd\": rd_roclet,\n        \"rd_roclet\": rd_roclet,\n        \"namespace\": namespace_roclet,\n        \"vignette\": vignet", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
