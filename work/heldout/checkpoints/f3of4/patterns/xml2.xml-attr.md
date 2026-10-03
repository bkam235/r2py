---
id: xml2.xml-attr
package: xml2
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# xml2.xml-attr

## Guidance
Translate R `xml_attr` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ae70763f", "r_snippet": "xml_attr(x, \"id\")", "py_snippet": "def xml_attr(x, attr, ns=None, default=None):\n    if isinstance(x, list):\n        return [xml_attr(node, attr, ns, default) for node in x]\n    \n    # If ns is passed as a list (to match R's xml_ns output), \n    # we can't use it for prefix lookup unless we have the mapping.\n    # However, the internal logic for namespaced attributes in lxml requires {url}local.\n    \n    # Try direct match first\n    val = x.get(attr)\n    if val is not None:\n        return val\n    \n    # Handle namespaced attributes if a mapping is provided\n    if isinstance(ns, dict) and ':' in attr:\n        prefix, local = attr.split(':', 1)\n        if prefix in ns:\n            val = x.get(f\"{{{ns[prefix]}}}{local}\")\n            if val is not None:\n                return val\n                \n    return default\n\nxml_attr_res1 = xml_attr(x, \"id\")", "score": 0.9333, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
