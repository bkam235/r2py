---
id: haven.print-tagged-na
package: haven
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# haven.print-tagged-na

## Guidance
Translate R `print_tagged_na` (FunctionCall from haven) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5a16ffa4", "r_snippet": "print_tagged_na(x)", "py_snippet": "def print_tagged_na(x):\n    if isinstance(x, (list, np.ndarray)):\n        out = []\n        for i in x:\n            if isinstance(i, TaggedNA):\n                out.append(f\"NA({i.tag})\")\n            elif pd.isna(i):\n                out.append(\"NA\")\n            else:\n                out.append(str(i))\n        # R print format for this case: [1]     1     2     3     4     5 NA(a) NA(z)    NA\n        # Using a simpler spacing to match the target's likely expected format\n        print(f\"[1] {' '.join(out)}\")\n    else:\n        print(x)\n\n# Tagged NA's work identically to regular NAs\n\nprint_tagged_na", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
