---
id: base.print
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.print

## Guidance
Translate R `print` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c3dfad3e", "r_snippet": "plot.discrete_distr <- function(x, ...) {\n  print(autoplot(x, ...))\n}", "py_snippet": "def plot_discrete_distr(x, **kwargs):\n    # Assuming x is a distribution object or a set of values\n    # Since autoplot for discrete distributions usually implies a probability mass function (PMF)\n    # We create a DataFrame from the data to plot using plotnine\n    \n    if hasattr(x, 'pmf'):\n        # If x is a distribution object (like from scipy.stats)\n        vals = np.arange(int(x.ppf(0.001)), int(x.ppf(0.999)) + 1)\n        probs = [x.pmf(v) for v in vals]\n        d = pd.DataFrame({'x': vals, 'prob': probs})\n    else:\n        # If x is a sequence of observations\n        d = pd.Series(x).value_counts(normalize=True).reset_index()\n        d.columns = ['x', 'prob']\n    \n    p = (ggplot(d) + \n         geom_col(mapping=aes(x='x', y='prob')) + \n         theme_minimal())\n    \n    print(p)", "score": 1.0, "script_id": "ggplot2__vignette__ggplot2-in-packages_s13", "n_calls": 1}

## Edit Examples
(none)
