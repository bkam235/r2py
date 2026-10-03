---
id: xml2.xml-children
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# xml2.xml-children

## Guidance
Translate R `xml_children` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4eeb5aaf", "r_snippet": "xml_children(x)", "py_snippet": "xml_children_x = list(x)\nprint(format_xml_node(xml_children_x))\n\n# xml_children(xml_children(x))", "score": 0.9699, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}
- {"r_hash": "71c50453", "r_snippet": "kids <- xml_children(x)", "py_snippet": "def xml_children(x):\n    return list(x)", "score": 0.92, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
