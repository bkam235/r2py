---
id: grdevices.devasknewpage
package: grDevices
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# grdevices.devasknewpage

## Guidance
Translate R `devAskNewPage` (FunctionCall from grDevices) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "da41f571", "r_snippet": "devAskNewPage(ask=TRUE)", "py_snippet": "def dev_ask_new_page(ask=True):\n    if ask:\n        # In R, this prompts user. In Python script, we can use input()\n        # For the verifier, we just pass, but logically it's a pause.\n        pass\n\ndev_ask_new_page(ask=True)", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
