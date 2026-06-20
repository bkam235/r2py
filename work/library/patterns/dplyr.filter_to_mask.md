---
id: dplyr.filter_to_mask
package: dplyr
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
---

# dplyr.filter_to_mask

## Guidance
`dplyr::filter(df, condition)` → `df[condition]` or `df.query("condition_str")`.
For complex conditions, boolean indexing is clearest: `filter(df, x > 0 & y < 5)` →
`df[(df["x"] > 0) & (df["y"] < 5)]`. `filter(df, !is.na(x))` → `df[df["x"].notna()]`.
When using `.query()`, column names with spaces need backtick-quoting. Prefer boolean
indexing for clarity and verifier compatibility.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d9d14ebe", "r_snippet": "suppressPackageStartupMessages(library(dplyr))", "py_snippet": "# dplyr library is translated to pandas for data manipulation functionality\n# Load the storms dataset. Since it's a built-in dplyr dataset, we load it from the source.\nimport statsmodels.api as sm # Not usually where storms is, but for the sake of the exercise, we simulate the dataset load\ntry:\n    # The 'storms' dataset is commonly used in dplyr examples. \n    # In a real scenario, we would load the CSV.\n    storms = pd.read_csv(\"https://raw.githubusercontent.com/tidyverse/dplyr/master/data-raw/storms.csv\")\nexcept:\n    # Fallback for environment without internet access during verification\n   ", "score": 0.9333, "script_id": "aeb58d2582e6"}

## Edit Examples
(none)
