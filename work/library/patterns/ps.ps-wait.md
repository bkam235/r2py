---
id: ps.ps-wait
package: ps
confidence: tentative
seed: true
created: 2026-08-25
last_review: 2026-08-25
tie_count: 0
---

# ps.ps-wait

## Guidance
Translate R `ps_wait` (FunctionCall from ps) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "feafa5c1", "r_snippet": "ps_wait(list(p1$as_ps_handle(), p2$as_ps_handle()), 0)", "py_snippet": "    def ps_wait(processes, timeout_ms):\n        start_time = time.time()\n        timeout_sec = timeout_ms / 1000.0\n        \n        # Convert timeout 0 to immediate check\n        # Convert -1 to indefinite wait (though the example uses 0 and 1000)\n        \n        while True:\n            results = [not p.is_running() for p in processes]\n            if all(results):\n                return results\n            \n            if timeout_ms == 0:\n                return results\n            \n            if timeout_ms != -1 and (time.time() - start_time) >= timeout_sec:\n                return results\n  ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
