# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tools import add_constant

# r2py:entity:tidy
def tidy(model, conf_int=False, conf_level=0.95, exponentiate=False):
    """
    Mimics broom::tidy for statsmodels RegressionResults.
    """
    # Extract coefficients, std errors, t-stats, and p-values
    params = model.params
    bse = model.bse
    tvalues = model.tvalues
    pvalues = model.pvalues
    
    df_tidy = pd.DataFrame({
        'term': params.index,
        'estimate': params.values,
        'std.error': bse.values,
        'statistic': tvalues.values,
        'p.value': pvalues.values
    })
    
    if conf_int:
        # Calculate confidence intervals
        ci = model.conf_int(alpha=1 - conf_level)
        ci.columns = ['conf.low', 'conf.high']
        ci.index.name = 'term'
        df_tidy = df_tidy.merge(ci, left_on='term', right_index=True)
        
    if exponentiate:
        df_tidy['estimate'] = np.exp(df_tidy['estimate'])
        if 'conf.low' in df_tidy.columns:
            df_tidy['conf.low'] = np.exp(df_tidy['conf.low'])
            df_tidy['conf.high'] = np.exp(df_tidy['conf.high'])
            
    return df_tidy

# Setup data (mtcars)
from statsmodels.datasets import get_rdataset
mtcars = get_rdataset("mtcars", "datasets").data

# fit model: lm(cbind(mpg, disp) ~ wt, mtcars)
# In R, cbind(mpg, disp) creates a multivariate response.
# In Python statsmodels, we fit two separate models or a Multivariate Linear Model.
# To match the 'tidy' output for multivariate lm, we usually treat them as combined results.

# r2py:entity:mod
X = add_constant(mtcars['wt'])
y = mtcars[['mpg', 'disp']]

# Fitting Multivariate OLS
model = sm.OLS(y, X).fit()

# summarize model fit with tidiers
# For multivariate models, broom::tidy typically stacks results for each response variable
# We iterate through the responses to mimic this behavior.
# r2py:entity:tidy
results = []
for col in y.columns:
    res = tidy(sm.OLS(y[col], X).fit(), conf_int=True)
    res.insert(0, 'response', col)
    results.append(res)

tidy_output = pd.concat(results, ignore_index=True)
print(tidy_output)