---
id: xml2.xml-parent
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# xml2.xml-parent

## Guidance
Translate R `xml_parent` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b1787097", "r_snippet": "xml_parent(xml_children(x))", "py_snippet": "parents_of_children = [node.getparent() for node in xml_children_x]\nseen = set()\nunique_parents = []\nfor p in parents_of_children:\n    if p not in seen:\n        unique_parents.append(p)\n        seen.add(p)\nprint(format_xml_node(unique_parents))\n\n# Mixed content", "score": 0.9425, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}

## Edit Examples
(none)
