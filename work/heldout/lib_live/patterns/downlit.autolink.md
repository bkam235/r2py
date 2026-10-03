---
id: downlit.autolink
package: downlit
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# downlit.autolink

## Guidance
Translate R `autolink` (FunctionCall from downlit) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a607d69d", "r_snippet": "autolink(\"stats::median()\")", "py_snippet": "def escape_html(text):\n    # R's escape_html in downlit is likely a wrapper around basic html escaping\n    # But it preserves the exact quotes in the example output.\n    return html.escape(text, quote=False)\n\nr_print(autolink(\"stats::median()\"))", "score": 1.0, "script_id": "downlit__rd_example__autolink_Rd", "n_calls": 0}

## Edit Examples
(none)
