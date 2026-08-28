# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 4

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

# Suppress startup messages (no-op in Python)
pass

# broom is not available in Python, we'll implement tidy() for mlm objects

# r2py:data_shim:begin
mtcars = pd.DataFrame({
    'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9, 21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],
    'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6, 6, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 8, 8, 8, 4],
    'disp': [160.0, 160.0, 108.0, 258.0, 360.0, 225.0, 360.0, 146.7, 140.8, 167.6, 167.6, 275.8, 275.8, 275.8, 472.0, 460.0, 440.0, 78.7, 75.7, 71.1, 120.1, 318.0, 304.0, 350.0, 400.0, 79.0, 120.3, 95.1, 351.0, 145.0, 301.0, 121.0],
    'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 123, 123, 180, 180, 180, 180, 205, 215, 52, 65, 66, 91, 200, 150, 245, 175, 66, 91, 113, 264, 175, 335, 109],
    'drat': [3.9, 3.9, 3.85, 3.08, 3.15, 2.76, 3.21, 3.69, 3.92, 3.92, 3.92, 3.07, 3.07, 3.07, 2.93, 3.0, 3.23, 4.93, 4.22, 4.08, 4.7, 3.07, 3.15, 3.73, 3.08, 4.08, 4.43, 3.77, 4.22, 3.62, 3.54, 4.11],
    'wt': [2.62, 2.875, 2.32, 3.215, 3.44, 3.46, 3.57, 3.19, 3.15, 3.44, 3.44, 4.07, 3.73, 3.78, 5.25, 5.424, 5.645, 2.2, 1.615, 1.835, 2.465, 3.52, 3.435, 3.84, 3.845, 1.935, 2.14, 1.513, 3.17, 2.77, 3.57, 2.78],
    'qsec': [16.46, 17.02, 18.61, 19.44, 17.02, 20.22, 15.84, 20.0, 22.9, 18.3, 18.9, 17.4, 17.6, 18.0, 17.98, 17.82, 17.0, 16.7, 18.52, 19.44, 20.01, 15.84, 17.3, 15.41, 17.05, 18.52, 19.47, 16.8, 16.87, 18.6, 14.5, 18.6],
    'vs': [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    'am': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    'gear': [4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 4],
    'carb': [4, 4, 1, 1, 2, 1, 4, 2, 2, 4, 4, 3, 3, 3, 4, 4, 4, 1, 2, 1, 2, 4, 4, 4, 2, 1, 2, 2, 4, 6, 8, 2]
})
# r2py:data_shim:end

# Fit multivariate linear model using separate OLS for each response
# r2py:entity:mod
X = sm.add_constant(mtcars[['wt']])
y_mpg = mtcars['mpg']
y_disp = mtcars['disp']

mod_mpg = sm.OLS(y_mpg, X).fit()
mod_disp = sm.OLS(y_disp, X).fit()

# Extract coefficients with confidence intervals for multivariate response
# r2py:entity:tidy
def tidy_mlm(mod_mpg, mod_disp, conf_int=False, alpha=0.05):
    """Tidy multivariate linear model results"""
    results_list = []
    
    for response, mod in [('mpg', mod_mpg), ('disp', mod_disp)]:
        # Get confidence intervals
        if conf_int:
            ci = mod.conf_int(alpha=alpha)
        
        for i, term in enumerate(mod.params.index):
            # Rename 'const' to '(Intercept)'
            term_name = '(Intercept)' if term == 'const' else term
            
            coef = mod.params[term]
            se = mod.bse[term]
            t_val = mod.tvalues[term]
            p_val = mod.pvalues[term]
            
            row = {
                'response': response,
                'term': term_name,
                'estimate': coef,
                'std.error': se,
                'statistic': t_val,
                'p.value': p_val
            }
            
            if conf_int:
                row['conf.low'] = ci.loc[term, 0]
                row['conf.high'] = ci.loc[term, 1]
            
            results_list.append(row)
    
    return pd.DataFrame(results_list)

# r2py:entity:tidy
print("> tidy(mod, conf.int = TRUE)")
tidy_results = tidy_mlm(mod_mpg, mod_disp, conf_int=True)
print("# A tibble: 4 × 8")
print(tidy_results.to_string(index=False))