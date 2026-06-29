---
id: broom--tidy---broom--glance
package: broom
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-29
tie_count: 0
---

# broom--tidy---broom--glance

## Guidance
Translate these functions by creating Python functions that extract relevant statistics from the model object and return them as a pandas DataFrame.

Convert the output of a statistical test into a pandas DataFrame containing the statistic, p-value, and method metadata.

Translate these as data frames (e.g., using pandas) that summarize model statistics into a tidy, tabular format.

Translate as functions that return a pandas DataFrame containing a summarized version of the model object's key statistics.

Convert the model result's properties into a pandas DataFrame with specific columns representing the model's statistics.

Translate to a pandas DataFrame that summarizes model statistics, typically formatting the result into a single-row table with named columns.

Translate broom's tidiers by converting the model summary or test result into a pandas DataFrame with standardized columns (e.g., 'statistic', 'p.value').

Translate these 'tidiers' by creating a pandas DataFrame that maps the specific components of the model result (e.g., statistic, p-value) into named columns.

Translate these to pandas DataFrames. If the source R function returns vectors (even for single values) as is common in R, ensure the Python implementation extracts the scalar value (e.g., `dw['dw'][0]`) to avoid nesting arrays inside the DataFrame cells.

Translate these R functions to Python by creating a pandas DataFrame that summarizes the model or test results into a single-row table.

Translate these to helper functions that convert model result objects or dictionaries into pandas DataFrames with specific columns mirroring the R tibble output.

Translate these functions to Python functions that return a pandas DataFrame containing the model's summary statistics.

Translate these functions by creating a pandas DataFrame (typically a single row) containing the key statistics of the model object, formatted to mimic a tidy tibble.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
