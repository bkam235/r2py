---
id: broom--tidy-glance
package: broom
confidence: tentative
seed: false
created: 2026-06-23
last_review: 2026-07-02
tie_count: 0
---

# broom--tidy-glance

## Guidance
Convert model output into a pandas DataFrame with standardized columns (e.g., 'statistic', 'p.value') to mimic R's tidy data frame output.

When translating broom's tidiers, ensure the output is a pandas DataFrame with columns exactly matching the R tibble specification.

Translate `broom::tidy()` and `broom::glance()` by creating pandas DataFrames that replicate the summary statistics and structure of the R object.

Convert the result object (dictionary or class) into a pandas DataFrame with the specific columns expected by the broom tidier (e.g., 'statistic', 'p.value', 'autocorrelation').

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
