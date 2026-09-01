---
id: xml2.xml-parent
package: xml2
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
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
- {"r_hash": "b1787097", "r_snippet": "xml_parent(xml_children(x))", "py_snippet": "parents = []\nseen = set()\nfor child in children:\n    p = child.getparent()\n    if p is not None and p not in seen:\n        parents.append(p)\n        seen.add(p)\nprint_nodeset(parents)\n\n# Mixed content\n# x <- read_xml(\"<foo> a <b/> c <d>e</d> f</foo>\")", "score": 0.9425, "script_id": "auto"}

## Edit Examples
(none)
