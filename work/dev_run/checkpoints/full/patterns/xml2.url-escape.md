---
id: xml2.url-escape
package: xml2
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# xml2.url-escape

## Guidance
Translate R `url_escape` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5be7d406", "r_snippet": "url_escape(\"a b c\")", "py_snippet": "print(urllib.parse.quote(\"a b c\"))\n\n# url_escape(\"a b c\", \"\")\n# In R, the second argument to url_escape is often used to specify characters NOT to escape.\n# In Python, 'safe' parameter defines characters that should be kept as-is.", "score": 1.0, "script_id": "xml2__rd_example__url_escape_Rd", "n_calls": 0}

## Edit Examples
(none)
