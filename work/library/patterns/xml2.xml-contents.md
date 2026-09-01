---
id: xml2.xml-contents
package: xml2
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# xml2.xml-contents

## Guidance
Translate R `xml_contents` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a08edbc2", "r_snippet": "xml_contents(x)", "py_snippet": "contents = x.xpath(\"node()\")\nprint_nodeset(contents)\n\n# xml_length(x)\n# By default, xml_length counts elements only.", "score": 0.9714, "script_id": "auto"}

## Edit Examples
(none)
