---
id: xml2.xml-attrs
package: xml2
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# xml2.xml-attrs

## Guidance
Translate R `xml_attrs` (FunctionCall from xml2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "97c78195", "r_snippet": "xml_attrs(x)", "py_snippet": "def xml_attrs(x, ns=None):\n    if isinstance(x, list):\n        return [xml_attrs(node, ns) for node in x]\n    \n    attrs = dict(x.attrib)\n    if isinstance(ns, dict):\n        # Map {url}local -> prefix:local\n        inv_ns = {v: k for k, v in ns.items()}\n        new_attrs = {}\n        for k, v in attrs.items():\n            if '}' in k:\n                url, local = k.split('}', 1)\n                url = url[1:]\n                prefix = inv_ns.get(url, 'unknown')\n                new_attrs[f\"{prefix}:{local}\"] = v\n            else:\n                new_attrs[k] = v\n        return new_attrs\n    return attrs\n\nxml_attrs_res1 = xml_attrs(x)", "score": 0.9333, "script_id": "xml2__rd_example__xml_attr_Rd", "n_calls": 0}

## Edit Examples
(none)
