---
id: haven.na-tag
package: haven
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# haven.na-tag

## Guidance
Translate R `na_tag` (FunctionCall from haven) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0a8074ac", "r_snippet": "na_tag(x)", "py_snippet": "def na_tag(x):\n    if isinstance(x, (list, np.ndarray)):\n        return np.array([i.tag if isinstance(i, TaggedNA) else None for i in x])\n    if isinstance(x, TaggedNA):\n        return x.tag\n    return None\n\nres_tag = na_tag(x)\nout_tag = []\nfor i in res_tag:\n    if i is None:\n        out_tag.append(\"NA\")\n    else:\n        out_tag.append(f'\"{i}\"')\nprint(f\"[1] {' '.join(out_tag)}\")", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
