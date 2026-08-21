---
id: data.table.tables
package: data.table
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# data.table.tables

## Guidance
Translate R `tables` (FunctionCall from data.table) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8f28d12b", "r_snippet": "tables()", "py_snippet": "def tables():\n    \"\"\"\n    Mimics the data.table::tables() function.\n    Iterates through global variables to find data-table-like objects.\n    \"\"\"\n    # Get all globals that are pandas DataFrames (mimicking is.data.table)\n    found_tables = []\n    for name, obj in globals().items():\n        if isinstance(obj, pd.DataFrame):\n            # Calculate memory usage in MB\n            mb = obj.memory_usage(deep=True).sum() / (1024 * 1024)\n            # Get columns\n            cols = \",\".join(obj.columns.tolist())\n            # Get key from attributes (set by our setkey equivalent)\n            key = o", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
