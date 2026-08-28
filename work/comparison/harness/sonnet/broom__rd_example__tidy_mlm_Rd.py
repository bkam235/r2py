# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 4

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
import scipy.stats as stats

# Load mtcars dataset
import statsmodels.datasets
mtcars = sm.datasets.get_rdataset("mtcars", "datasets").data

# fit multivariate linear model: cbind(mpg, disp) ~ wt
# In Python, we fit two separate OLS models (one per response)
# r2py:entity:mod
X = sm.add_constant(mtcars[["wt"]])
responses = ["mpg", "disp"]

# r2py:entity:tidy
def tidy_mlm(X, mtcars, responses, conf_int=True, conf_level=0.95):
    rows = []
    for resp in responses:
        y = mtcars[resp]
        model = OLS(y, X).fit()
        
        for term in model.params.index:
            estimate = model.params[term]
            std_error = model.bse[term]
            statistic = model.tvalues[term]
            p_value = model.pvalues[term]
            
            row = {
                "response": resp,
                "term": term,
                "estimate": estimate,
                "std.error": std_error,
                "statistic": statistic,
                "p.value": p_value,
            }
            
            if conf_int:
                ci = model.conf_int(alpha=1 - conf_level)
                row["conf.low"] = ci.loc[term, 0]
                row["conf.high"] = ci.loc[term, 1]
            
            rows.append(row)
    
    return pd.DataFrame(rows)

# r2py:entity:tidy
result = tidy_mlm(X, mtcars, responses, conf_int=True, conf_level=0.95)

# Rename 'const' term to match R's '(Intercept)'
result["term"] = result["term"].replace("const", "(Intercept)")

# Print result
pd.set_option("display.float_format", lambda x: f"{x:.6g}")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print("# A tibble: 4 × 8")
print(result.to_string(index=False))