---
id: xml2.xml-contents
package: xml2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
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
- {"r_hash": "a08edbc2", "r_snippet": "xml_contents(x)", "py_snippet": "contents = []\nif x.text:\n    contents.append(x.text)\nfor child in x:\n    contents.append(child)\n    if child.tail:\n        contents.append(child.tail)\n\ndef format_contents(nodes):\n    res = []\n    for n in nodes:\n        if isinstance(n, str):\n            res.append(n)\n        else:\n            # Elements in xml_contents are printed without their tails\n            res.append(etree.tostring(n, encoding='unicode').strip())\n    header = f\"{{xml_nodeset ({len(nodes)})}}\"\n    return \"\\n\".join([header] + [f\"[{i+1}] {val}\" for i, val in enumerate(res)])\n\nprint(format_contents(contents))\n\n# xml_length(x)", "score": 0.9806, "script_id": "xml2__rd_example__xml_children_Rd", "n_calls": 0}

## Edit Examples
(none)
