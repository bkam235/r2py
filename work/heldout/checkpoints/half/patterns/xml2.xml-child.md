---
id: xml2.xml-child
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
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
- {"r_hash": "efb6925e", "r_snippet": "xml_child(x)", "py_snippet": "node_child = x[0] if len(x) > 0 else None\nprint(format_xml_node(node_child))\n\n# xml_child(x, 2)", "score": 0.9444, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}

## Edit Examples
(none)
