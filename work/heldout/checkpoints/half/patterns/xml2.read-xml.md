---
id: xml2.read-xml
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# xml2.read-xml

## Guidance
Translate R `read_xml` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9f6b8511", "r_snippet": "x <- read_xml(\"<foo> a <b/> c <d>e</d> f</foo>\")", "py_snippet": "x = etree.fromstring(\"<foo> a <b/> c <d>e</d> f</foo>\")\n\n# xml_children(x)", "score": 1.0, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}

## Edit Examples
(none)
