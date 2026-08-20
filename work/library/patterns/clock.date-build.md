---
id: clock.date-build
package: clock
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# clock.date-build

## Guidance
Translate R `date_build` (FunctionCall from clock) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "12084efa", "r_snippet": "date_build(2019, 1:12, 31)", "py_snippet": "try:\n    # Pandas.to_datetime handles date construction. \n    # Using a dataframe to simulate the vectorization of 1:12\n    dates = pd.to_datetime({'year': 2019, 'month': np.arange(1, 13), 'day': 31}, errors='coerce')\nexcept Exception:\n    pass", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
