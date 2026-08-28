# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.mlm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 6

import statsmodels.api as sm
import statsmodels.datasets
import pandas as pd

mtcars = sm.datasets.get_rdataset("mtcars").data

# fit model
X = sm.add_constant(mtcars["wt"])
mod_mpg = sm.OLS(mtcars["mpg"], X).fit()
mod_disp = sm.OLS(mtcars["disp"], X).fit()

# summarize model fit with tidiers (confidence intervals included)
results = []
for name, mod in [("mpg", mod_mpg), ("disp", mod_disp)]:
    ci = mod.conf_int()
    tidy = pd.DataFrame({
        "response": name,
        "term": mod.params.index,
        "estimate": mod.params.values,
        "std.error": mod.bse.values,
        "statistic": mod.tvalues.values,
        "p.value": mod.pvalues.values,
        "conf.low": ci[0].values,
        "conf.high": ci[1].values,
    })
    results.append(tidy)
print(pd.concat(results, ignore_index=True))
