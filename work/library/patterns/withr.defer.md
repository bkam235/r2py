---
id: withr.defer
package: withr
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# withr.defer

## Guidance
Translate R `defer` (ExternalSymbol from withr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "302624a3", "r_snippet": "withr::defer(print(\"hi\"))", "py_snippet": "class WithrMock:\n    def __init__(self):\n        self.global_exits = []\n\n    def defer(self, expr_func, priority=\"first\"):\n        if priority == \"first\":\n            self.global_exits.insert(0, expr_func)\n        else:\n            self.global_exits.append(expr_func)\n\nwithr.defer(lambda: print(\"hi\"))\n\n# In R: withr::deferred_run()", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
