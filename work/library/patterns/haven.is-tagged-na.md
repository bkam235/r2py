---
id: haven.is-tagged-na
package: haven
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# haven.is-tagged-na

## Guidance
Translate R `is_tagged_na` (FunctionCall from haven) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bf0248b2", "r_snippet": "is_tagged_na(x)", "py_snippet": "def is_tagged_na(x, tag=None):\n    if isinstance(x, (list, np.ndarray)):\n        res = []\n        for i in x:\n            if isinstance(i, TaggedNA):\n                res.append(tag is None or i.tag == tag)\n            else:\n                res.append(False)\n        return np.array(res)\n    if isinstance(x, TaggedNA):\n        return tag is None or x.tag == tag\n    return False\n\nres_istag = is_tagged_na(x)\nprint(f\"[1] {' '.join([str(v).upper() for v in res_istag])}\")", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
