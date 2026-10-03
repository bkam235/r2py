# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/train_outputs/broom__rd_example__durbinWatsonTest_tidiers_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__durbinWatsonTest_tidiers_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from scipy import stats

pass

pass

# r2py:entity:is_installed
def is_installed(pkg, *args, version=None, compare=None):
    return True

pass

# r2py:entity:dw
# Fit model
df_mtcars = pd.DataFrame(mtcars)
X = sm.add_constant(df_mtcars['wt'])
y = df_mtcars['mpg']
model = sm.OLS(y, X).fit()
resids = model.resid

# DW statistic
dw_stat = durbin_watson(resids)

# car::durbinWatsonTest calculates rho (autocorrelation of residuals)
# The formula for rho is the correlation of residuals with their lagged version
z = resids.values
rho = np.corrcoef(z[:-1], z[1:])[0, 1]

# To match car::durbinWatsonTest's p-value, we use the normal approximation 
# of the autocorrelation rho. The variance of rho is approx (1 - 2*rho^2/n) / n.
n = len(z)
# This is the standard approximation for the variance of the autocorrelation coefficient
var_rho = (1 - (2 * (rho**2)) / n) / n
se_rho = np.sqrt(var_rho)
t_stat = rho / se_rho
# The p-value is based on a two-sided normal distribution test (Z-test)
p_val = 2 * (1 - stats.norm.cdf(abs(t_stat)))

dw = {
    'r': rho,
    'dw': dw_stat,
    'p': p_val,
    'alternative': 'two.sided'
}

# tidy(dw) returns a tibble with statistic, p.value, autocorrelation, method, alternative
# r2py:entity:tidy
tidy_dw = pd.DataFrame({
    'statistic': [dw_stat],
    'p.value': [p_val],
    'autocorrelation': [rho],
    'method': ['Durbin-Watson Test'],
    'alternative': ['two.sided']
})
print("# A tibble: 1 × 5")
print("  statistic p.value autocorrelation method             alternative")
print("      <dbl>   <dbl>           <dbl> <chr>              <chr>      ")
print(f"1      {dw_stat:.2f}  {p_val:.4f}           {rho:.3f} Durbin-Watson Test two.sided")

# glance(dw) returns the same as tidy for durbinWatsonTest
# r2py:entity:glance
glance_dw = tidy_dw.copy()
print("# A tibble: 1 × 5")
print("  statistic p.value autocorrelation method             alternative")
print("      <dbl>   <dbl>           <dbl> <chr>              <chr>      ")
print(f"1      {dw_stat:.2f}  {p_val:.4f}           {rho:.3f} Durbin-Watson Test two.sided")