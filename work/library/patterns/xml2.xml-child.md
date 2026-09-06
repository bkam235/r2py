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
- {"r_hash": "d5725421", "r_snippet": "xml_siblings(xml_children(x)[[1]])", "py_snippet": "first_child = children[0]\nsiblings = [sib for sib in x if sib != first_child]\nprint_nodeset(siblings)\n\n# xml_parent(xml_children(x))\n# R's xml_parent on a nodeset returns a nodeset of unique parents.", "score": 1.0, "script_id": "auto"}
- {"r_hash": "2bc3df5d", "r_snippet": "xml_length(x)", "py_snippet": "print(f\"[1] {len(list(x))}\")\n\n# xml_length(x, only_elements = FALSE)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "a08edbc2", "r_snippet": "xml_contents(x)", "py_snippet": "contents = x.xpath(\"node()\")\nprint_nodeset(contents)\n\n# xml_length(x)\n# By default, xml_length counts elements only.", "score": 0.9714, "script_id": "auto"}

## Edit Examples
(none)
