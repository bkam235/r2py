# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 4

import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

# Load mtcars
mtcars = pd.read_csv("https://gist.githubusercontent.com/seankross/a412dfbd88b3db70b74b/raw/5f23f993cd87c283ce766e7ac6b329ee7cc2e1d1/mtcars.csv")

# fit model: lm(cbind(mpg, disp) ~ wt, mtcars) — multivariate linear model
# For each response, fit a separate OLS and collect tidy results

# r2py:entity:tidy
def tidy_mlm(X, y_dict, conf_int=False, conf_level=0.95):
    """Tidy a multivariate linear model (mlm), mimicking broom::tidy.mlm"""
    results = []
    
    for response_name, y in y_dict.items():
        n = len(y)
        p = X.shape[1]
        
        # Fit OLS
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        y_hat = X @ beta
        residuals = y - y_hat
        
        # Standard errors
        dof = n - p
        mse = np.sum(residuals**2) / dof
        XtX_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(XtX_inv) * mse)
        
        # t-statistics and p-values
        t_stats = beta / se
        p_values = 2 * scipy_stats.t.sf(np.abs(t_stats), dof)
        
        term_names = ["(Intercept)", "wt"]
        
        for i in range(len(term_names)):
            row = {
                "response": response_name,
                "term": term_names[i],
                "estimate": beta[i],
                "std.error": se[i],
                "statistic": t_stats[i],
                "p.value": p_values[i],
            }
            
            if conf_int:
                t_crit = scipy_stats.t.ppf(1 - (1 - conf_level) / 2, dof)
                row["conf.low"] = beta[i] - t_crit * se[i]
                row["conf.high"] = beta[i] + t_crit * se[i]
            
            results.append(row)
    
    return pd.DataFrame(results)

# r2py:entity:mod
# Prepare design matrix
X = np.column_stack([np.ones(len(mtcars)), mtcars["wt"].values])
y_dict = {"mpg": mtcars["mpg"].values, "disp": mtcars["disp"].values}

# summarize model fit with tidiers
# r2py:entity:tidy
result = tidy_mlm(X, y_dict, conf_int=True)

# Print in tibble-like format
print("# A tibble: {} × {}".format(result.shape[0], result.shape[1]))

col_types = {}
for col in result.columns:
    if result[col].dtype == object:
        col_types[col] = "<chr>"
    else:
        col_types[col] = "<dbl>"

header = "  ".join(f"{col}" for col in result.columns)
types = "  ".join(f"{col_types[col]}" for col in result.columns)
print(f"  {header}")
print(f"  {types}")

for _, row in result.iterrows():
    parts = []
    for col in result.columns:
        val = row[col]
        if isinstance(val, str):
            parts.append(f"{val}")
        elif col == "p.value":
            parts.append(f"{val:.2e}")
        else:
            parts.append(f"{val:.2f}")
    print("  ".join(parts))