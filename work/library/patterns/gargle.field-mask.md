---
id: gargle.field-mask
package: gargle
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# gargle.field-mask

## Guidance
Translate R `field_mask` (FunctionCall from gargle) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "3fc89112", "r_snippet": "field_mask(x)", "py_snippet": "def field_mask_impl(value, key):\n    \"\"\"\n    Helper function to recursively generate the field mask for a \n    dictionary-like object.\n    \"\"\"\n    if isinstance(value, dict):\n        # Recurse into the dictionary\n        children = [field_mask_impl(v, k) for k, v in value.items()]\n        children_str = \",\".join(children)\n        return f\"{key}({children_str})\"\n    else:\n        # Base case: just return the key\n        return key\n\ndef field_mask(x):\n    \"\"\"\n    Translates a dictionary into a Google API field mask string.\n    \"\"\"\n    if not isinstance(x, dict):\n        raise TypeError(\"x must b", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
