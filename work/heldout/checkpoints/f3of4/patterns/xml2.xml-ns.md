---
id: xml2.xml-ns
package: xml2
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# xml2.xml-ns

## Guidance
Translate R `xml_ns` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ed87e515", "r_snippet": "ns <- xml_ns(x)", "py_snippet": "ns_map = x.nsmap.copy()\nif None in ns_map:\n    del ns_map[None]\nns = list(ns_map.values())", "score": 0.92, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
