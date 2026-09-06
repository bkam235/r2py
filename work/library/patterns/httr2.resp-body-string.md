---
id: httr2.resp-body-string
package: httr2
confidence: tentative
seed: true
created: 2026-09-06
last_review: 2026-09-06
tie_count: 0
---

# httr2.resp-body-string

## Guidance
Translate R `resp_body_string` (FunctionCall from httr2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2f71f136", "r_snippet": "resp |> resp_body_string()", "py_snippet": "content_str = resp.text\n# To match R's print(string), we use repr() but ensure double quotes and literal \\n\nformatted_str = content_str.replace('\"', '\\\\\"')\nprint(f'[1] \"{formatted_str}\"')\n\n# R: resp |> resp_body_html()\n# R's resp_body_html returns an html_document object. \n# The print output shows the <html> tag, then the <head> section, then <body> section.", "score": 0.9866, "script_id": "auto"}

## Edit Examples
(none)
