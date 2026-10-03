---
id: xml2.xml-siblings
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# xml2.xml-siblings

## Guidance
Translate R `xml_siblings` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d5725421", "r_snippet": "xml_siblings(xml_children(x)[[1]])", "py_snippet": "first_child = xml_children_x[0]\nsiblings = [el for el in first_child.getparent() if el is not first_child]\nprint(format_xml_node(siblings))\n\n# xml_parent(xml_children(x))", "score": 1.0, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}

## Edit Examples
(none)
