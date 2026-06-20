---
id: xfun-cache-rds-python
package: 
confidence: tentative
seed: false
created: 2026-06-15
last_review: 2026-06-15
tie_count: 0
---

# xfun-cache-rds-python

## Guidance
Translate R's xfun::cache_rds() to a Python function that caches expression results to disk using pickle. Accept **kwargs to handle variable arguments like rerun flag, execute the expression (time.sleep + list generation), and use MD5 hashing of the expression string to generate cache filenames.

## Evidence
- 34ab01c45818 → score 0.119 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
