---
id: base.as.vector
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.as.vector

## Guidance
Translate R `as.vector` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b7cac5e8", "r_snippet": "corrDF$correlation <- as.vector(R2)", "py_snippet": "corrDF['correlation'] = R2.values.flatten('F')", "score": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "crash", "old_code": "        corrDF.append({'row': r+1, 'col': c+1, 'correlation': R2.iloc[r, c]})\ncorrDF = pd.DataFrame(corrDF)", "new_code": "corrDF['correlation'] = R2.values.flatten('F')", "score_delta": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "r_snippet": "corrDF$correlation <- as.vector(R2)", "functions": ["base::as.vector"]}
