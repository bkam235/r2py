---
id: xml2.xml-has-attr
package: xml2
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# xml2.xml-has-attr

## Guidance
Translate R `xml_has_attr` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a4e64c37", "r_snippet": "xml_has_attr(kids, \"id\")", "py_snippet": "def xml_has_attr(x, attr, ns=None):\n    if isinstance(x, list):\n        return [xml_has_attr(node, attr, ns) for node in x]\n    return xml_attr(x, attr, ns) is not None\n\nxml_has_attr_kids = xml_has_attr(kids, \"id\")", "score": 0.9333, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
