---
id: xml2.xml-set-attr
package: xml2
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# xml2.xml-set-attr

## Guidance
Translate R `xml_set_attr` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "6ca2d059", "r_snippet": "xml_set_attr(doc, \"id\", \"two\")", "py_snippet": "def xml_set_attr(x, attr, value, ns=None):\n    target_attr = attr\n    if isinstance(ns, dict) and ':' in attr:\n        prefix, local = attr.split(':', 1)\n        if prefix in ns:\n            target_attr = f\"{{{ns[prefix]}}}{local}\"\n    x.set(target_attr, value)\n\nxml_set_attr(doc, \"id\", \"one\") # xml_attr(doc, \"id\") <- \"one\"\nxml_set_attr(doc, \"id\", \"two\")\n\n# Set multiple attributes", "score": 0.9333, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
