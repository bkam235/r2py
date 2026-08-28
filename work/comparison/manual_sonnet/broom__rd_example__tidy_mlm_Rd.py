# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.mlm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 6

import pandas as pd
import statsmodels.api as sm

# Load the mtcars dataset
mtcars = sm.datasets.get_rdataset("mtcars", "datasets").data

# Fit multivariate linear model: lm(cbind(mpg, disp) ~ wt, mtcars)
# R's mlm fits each response column separately with the same predictors
X = sm.add_constant(mtcars["wt"])
responses = ["mpg", "disp"]

rows = []
for response in responses:
    model = sm.OLS(mtcars[response], X).fit()
    ci = model.conf_int()
    for term in model.params.index:
        rows.append({
            "response": response,
            "term": term,
            "estimate": model.params[term],
            "std.error": model.bse[term],
            "statistic": model.tvalues[term],
            "p.value": model.pvalues[term],
            "conf.low": ci.loc[term, 0],
            "conf.high": ci.loc[term, 1],
        })

tidy_result = pd.DataFrame(rows)
print(tidy_result.to_string(index=False))
