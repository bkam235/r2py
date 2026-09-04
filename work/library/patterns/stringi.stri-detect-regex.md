---
id: stringi.stri-detect-regex
package: stringi
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# stringi.stri-detect-regex

## Guidance
Translate R `stri_detect_regex` (FunctionCall from stringi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "acb8e2e4", "r_snippet": "stri_detect_regex(c('a1', 'a2', 'b3', 'a4', 'c5'), '^a')", "py_snippet": "# stri_detect_regex(c('a1', 'a2', 'b3', 'a4', 'c5'), '^a')\nprint([bool(re.search(r'^a', s)) for s in data])", "score": 1.0, "script_id": "auto"}
- {"r_hash": "fa051e74", "r_snippet": "stri_trans_char('id.123', '.', '_')", "py_snippet": "def stri_trans_char(text, old, new):\n    table = str.maketrans(old, new)\n    return text.translate(table)\n\nprint(stri_trans_char('id.123', '.', '_'))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
