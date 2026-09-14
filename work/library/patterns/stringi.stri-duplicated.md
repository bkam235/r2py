---
id: stringi.stri-duplicated
package: stringi
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# stringi.stri-duplicated

## Guidance
Translate R `stri_duplicated` (FunctionCall from stringi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bafe56cc", "r_snippet": "stri_duplicated(c('a', 'b', 'a', NA, 'a', NA))", "py_snippet": "def stri_duplicated(str_vec, from_last=False, strength=None):\n    # Handle strings with potential Unicode normalization or case insensitivity\n    # strength=1 in stringi usually means primary level (case/accent insensitive)\n    processed = []\n    for x in str_vec:\n        if x is None or (isinstance(x, float) and np.isnan(x)):\n            processed.append(None)\n        else:\n            val = str(x)\n            if strength == 1:\n                val = unicodedata.normalize('NFKD', val).casefold()\n            processed.append(val)\n\n    n = len(processed)\n    duplicated = [False] * n\n    seen = s", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
