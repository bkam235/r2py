---
id: xml2.xml-add-child
package: xml2
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# xml2.xml-add-child

## Guidance
Translate R `xml-add-child` from xml2 to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b494fba5", "r_snippet": "xml_add_child(t1, t3)", "py_snippet": "def xml_add_child(x, value, copy_node=True):\n    if copy_node:\n        # If the value is already an element, deepcopy it to simulate R's .copy = TRUE\n        if isinstance(value, etree._Element):\n            node = copy.deepcopy(value)\n        else:\n            node = value\n    else:\n        node = value\n    \n    x.append(node)\n    return node", "score": 1.0, "script_id": "xml2__vignette__modification_s7.R", "n_calls": 0}
- {"r_hash": "f5d2be94", "r_snippet": "xml_add_child(t1, read_xml(\"<test/>\"))", "py_snippet": "# To replicate that, we set copy_node=False for existing nodes.\nxml_add_child(t1, t3, copy_node=False)", "score": 1.0, "script_id": "xml2__vignette__modification_s7.R", "n_calls": 0}

## Edit Examples
(none)
