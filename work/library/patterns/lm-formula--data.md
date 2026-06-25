---
id: lm-formula--data
package: broom
confidence: tentative
seed: false
created: 2026-06-23
last_review: 2026-06-24
tie_count: 0
---

# lm-formula--data

## Guidance
Translate to statsmodels.api.OLS by extracting the target variable (y) and creating a design matrix (X) using sm.add_constant() for the predictors.

Translate R's `lm()` regression to Python using `statsmodels.api.OLS`, ensuring that `sm.add_constant()` is called on the feature matrix to include an intercept.

Use statsmodels.api.OLS. For formulas like 'mpg ~ wt', use sm.add_constant() on the independent variables to include the intercept.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
