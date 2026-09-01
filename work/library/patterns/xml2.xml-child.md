---
id: xml2.xml-child
package: xml2
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# xml2.xml-child

## Guidance
Translate R `xml_child` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "efb6925e", "r_snippet": "xml_child(x)", "py_snippet": "child_1 = x[0] if len(x) > 0 else None\nprint(f\"{{xml_node}}\\n{format_node(child_1)}\")\n\n# xml_child(x, 2)", "score": 0.9444, "script_id": "auto"}

## Edit Examples
(none)
