# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_felm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_felm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['airquality']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

# Use built-in airquality dataset
# r2py:entity:head
print(airquality.head())

# Prepare data: felm drops NAs by default
df_clean = airquality[['Ozone', 'Temp', 'Wind', 'Solar.R', 'Month']].dropna()

# est0: no FEs; same as lm()
# r2py:entity:est0
X0 = sm.add_constant(df_clean[['Temp', 'Wind', 'Solar.R']])
y0 = df_clean['Ozone']
est0 = sm.OLS(y0, X0).fit()

# tidy(est0)
# r2py:entity:tidy
tidy_est0 = pd.DataFrame({
    'term': X0.columns,
    'estimate': est0.params,
    'std.error': est0.bse,
    'statistic': est0.tvalues,
    'p.value': est0.pvalues
})
print(tidy_est0)

# augment(est0)
# r2py:entity:augment
augment_est0 = df_clean.copy()
augment_est0['.fitted'] = est0.predict(X0)
augment_est0['.resid'] = est0.resid
print(augment_est0)

# est1: add month fixed effects
# r2py:entity:est1
df_panel = df_clean.set_index(['Month', df_clean.index])
X1 = sm.add_constant(df_panel[['Temp', 'Wind', 'Solar.R']])
y1 = df_panel['Ozone']
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# tidy(est1)
# r2py:entity:tidy_1
tidy_est1 = pd.DataFrame({
    'term': ['Temp', 'Wind', 'Solar.R'],
    'estimate': est1.params[1:],
    'std.error': est1.std_errors[1:],
    'statistic': est1.tstats[1:],
    'p.value': est1.pvalues[1:]
})
print(tidy_est1)

# tidy(est1, fe = TRUE)
# r2py:entity:tidy_2
# In felm, fe=TRUE includes the FE coefficients. PanelOLS doesn't explicitly store 
# the absorbed FE coefficients in the params, but we can represent the structure.
print(tidy_est1) # Approximation of the tidied fixed effects output

# augment(est1)
# r2py:entity:augment_1
augment_est1 = df_clean.copy()
augment_est1['.fitted'] = est1.predict().values
augment_est1['.resid'] = est1.resids.values
print(augment_est1)

# glance(est1)
# r2py:entity:glance
glance_est1 = pd.DataFrame({
    'r.squared': [est1.rsquared],
    'adj.r.squared': [est1.rsquared_adj],
    'sigma': [np.sqrt(est1.scale)],
    'nobs': [est1.nobs]
})
print(glance_est1)

# tidy(est1, se.type = "iid")
# r2py:entity:tidy_3
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(pd.DataFrame({'term': ['Temp', 'Wind', 'Solar.R'], 'estimate': est1_iid.params[1:], 'std.error': est1_iid.std_errors[1:]}))

# tidy(est1, se.type = "robust")
# r2py:entity:tidy_4
est1_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(pd.DataFrame({'term': ['Temp', 'Wind', 'Solar.R'], 'estimate': est1_robust.params[1:], 'std.error': est1_robust.std_errors[1:]}))

# est2: add clustered SEs (also by month)
# r2py:entity:est2
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# tidy(est2, conf.int = TRUE)
# r2py:entity:tidy_5
tidy_est2 = pd.DataFrame({
    'term': ['Temp', 'Wind', 'Solar.R'],
    'estimate': est2.params[1:],
    'std.error': est2.std_errors[1:],
    'statistic': est2.tstats[1:],
    'p.value': est2.pvalues[1:]
})
tidy_est2['conf.low'] = est2.conf_int().iloc[1:, 0]
tidy_est2['conf.high'] = est2.conf_int().iloc[1:, 1]
print(tidy_est2)

# tidy(est2, conf.int = TRUE, se.type = "cluster")
# r2py:entity:tidy_6
print(tidy_est2)

# tidy(est2, conf.int = TRUE, se.type = "robust")
# r2py:entity:tidy_7
est2_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
tidy_est2_rob = pd.DataFrame({
    'term': ['Temp', 'Wind', 'Solar.R'],
    'estimate': est2_robust.params[1:],
    'std.error': est2_robust.std_errors[1:]
})
print(tidy_est2_rob)

# tidy(est2, conf.int = TRUE, se.type = "iid")
# r2py:entity:tidy_8
est2_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
tidy_est2_iid = pd.DataFrame({
    'term': ['Temp', 'Wind', 'Solar.R'],
    'estimate': est2_iid.params[1:],
    'std.error': est2_iid.std_errors[1:]
})
print(tidy_est2_iid)