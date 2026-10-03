---
id: xml2.url-unescape
package: xml2
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# xml2.url-unescape

## Guidance
Translate R `url_unescape` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1df9858f", "r_snippet": "url_unescape(\"a%20b%2fc\")", "py_snippet": "print(urllib.parse.unquote(\"a%20b%2fc\"))\n\n# url_unescape(\"%C2%B5\")", "score": 1.0, "script_id": "xml2__rd_example__url_escape_Rd", "n_calls": 0}

## Edit Examples
(none)
