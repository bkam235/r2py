---
id: googlesheets4.gs4-has-token
package: googlesheets4
confidence: tentative
seed: true
created: 2026-07-17
last_review: 2026-07-17
tie_count: 0
---

# googlesheets4.gs4-has-token

## Guidance
Translate R `gs4_has_token` (FunctionCall from googlesheets4) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "627d499f", "r_snippet": "if (gs4_has_token()) withAutoprint({ # examplesIf", "py_snippet": "def gs4_has_token() -> bool:\n    \"\"\"Check if a valid Google Sheets token is available.\"\"\"\n    return False\n\nif gs4_has_token():", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
