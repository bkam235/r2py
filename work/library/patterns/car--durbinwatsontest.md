---
id: car--durbinwatsontest
package: broom
confidence: tentative
seed: false
created: 2026-06-22
last_review: 2026-06-24
tie_count: 0
---

# car--durbinwatsontest

## Guidance
Use `statsmodels.stats.stattools.durbin_watson` on the model residuals to calculate the Durbin-Watson statistic.

Implement using the formula sum((diff(residuals)**2)) / sum(residuals**2) or via statsmodels.stats.stattools.durbin_watson.

Implement using residuals from a statsmodels fit; if calculating p-values via simulation, resample residuals and project them using the model's design matrix (I-P) to get simulated residuals.

Use statsmodels.stats.stattools.durbin_watson for the core statistic and implement a simulation loop with numpy for the p-value and autocorrelation (rho).

Implement using residuals from a statsmodels fit result, calculating the DW statistic as the sum of squared differences of residuals divided by the sum of squared residuals.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
