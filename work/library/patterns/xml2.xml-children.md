---
id: xml2.xml-children
package: xml2
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
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
- {"r_hash": "4eeb5aaf", "r_snippet": "xml_children(x)", "py_snippet": "children = list(x)\nprint_nodeset(children)\n\n# xml_children(xml_children(x))\n# In R, xml_children(nodeset) returns a flattened nodeset of all children", "score": 0.9699, "script_id": "auto"}

## Edit Examples
(none)
