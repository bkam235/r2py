---
id: xml2.xml-length
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# xml2.xml-length

## Guidance
Translate R `xml_length` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2bc3df5d", "r_snippet": "xml_length(x)", "py_snippet": "print(f\"[1] {len(list(x))}\")\n\n# xml_length(x, only_elements = FALSE)", "score": 1.0, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}

## Edit Examples
(none)
