---
id: xml2.xml-set-attrs
package: xml2
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# xml2.xml-set-attrs

## Guidance
Translate R `xml_set_attrs` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0adb2166", "r_snippet": "xml_set_attrs(doc, c(\"b:id\" = \"one\", \"f:id\" = \"two\", \"id\" = \"three\"))", "py_snippet": "def xml_set_attrs(x, value, ns=None):\n    for attr, val in value.items():\n        xml_set_attr(x, attr, val, ns)\n\n# Main script\n\nxml_set_attrs(doc, attrs_val, ns_map)", "score": 0.9333, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
