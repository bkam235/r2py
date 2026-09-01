---
id: stringi.stri-startswith-charclass
package: stringi
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# stringi.stri-startswith-charclass

## Guidance
Translate R `stri_startswith_charclass` (FunctionCall from stringi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4fbf495e", "r_snippet": "stri_startswith_charclass(' trim me! ', '\\\\p{WSpace}')", "py_snippet": "# stri_startswith_charclass(' trim me! ', '\\\\p{WSpace}')\n# \\s matches any whitespace character\nprint(bool(re.match(r'\\s', ' trim me! ')))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
