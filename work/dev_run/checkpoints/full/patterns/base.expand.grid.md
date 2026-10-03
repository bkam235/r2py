---
id: base.expand.grid
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.expand.grid

## Guidance
Translate R `expand.grid` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a8e70ac8", "r_snippet": "corrDF <- expand.grid(row = 1:5, col = 1:5)", "py_snippet": "row_vals = np.tile(np.arange(1, 6), 5)\ncol_vals = np.repeat(np.arange(1, 6), 5)\ncorrDF = pd.DataFrame({'row': row_vals, 'col': col_vals})", "score": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "crash", "old_code": "corrDF = []\nfor r in range(5):\n    for c in range(5):", "new_code": "row_vals = np.tile(np.arange(1, 6), 5)\ncol_vals = np.repeat(np.arange(1, 6), 5)\ncorrDF = pd.DataFrame({'row': row_vals, 'col': col_vals})", "score_delta": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "r_snippet": "corrDF <- expand.grid(row = 1:5, col = 1:5)", "functions": ["base::expand.grid"]}
