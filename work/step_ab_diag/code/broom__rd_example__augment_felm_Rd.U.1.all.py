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

def tidy(model, fe=False, se_type=None, conf_int=False):
    # This is a mock of the broom::tidy function for felm/OLS models
    if hasattr(model, 'params'):
        params = model.params
        std_err = model.std_errs if hasattr(model, 'std_errs') else model.bse
        t_stats = params / std_err
        p_vals = model.pvalues
        
        res = pd.DataFrame({
            'term': params.index,
            'estimate': params.values,
            'std.error': std_err.values,
            'statistic': t_stats.values,
            'p.value': p_vals.values
        })
        
        if conf_int:
            conf_low = params - 1.96 * std_err
            conf_high = params + 1.96 * std_err
            res['conf.low'] = conf_low.values
            res['conf.high'] = conf_high.values
            
        return res
    return pd.DataFrame()

def augment(model, data):
    # Mock of broom::augment
    fitted = model.predict()
    resid = model.resid
    aug = data.copy()
    aug['.fitted'] = fitted.values if hasattr(fitted, 'values') else fitted
    aug['.resid'] = resid.values if hasattr(resid, 'values') else resid
    return aug

def glance(model):
    # Mock of broom::glance
    return pd.DataFrame({
        'r.squared': [model.rsquared],
        'adj.r.squared': [model.rsquared_adj],
        'sigma': [model.resid.std()],
        'nobs': [model.nobs]
    })

# Use built-in `airquality` dataset
# r2py:entity:head
print(airquality.head())

# No FEs; same as lm()
# r2py:entity:est0
# felm(Ozone ~ Temp + Wind + Solar.R, airquality)
df0 = airquality[['Ozone', 'Temp', 'Wind', 'Solar.R']].dropna()
X0 = sm.add_constant(df0[['Temp', 'Wind', 'Solar.R']])
y0 = df0['Ozone']
est0 = sm.OLS(y0, X0).fit()

# summarize model fit with tidiers
# r2py:entity:tidy
print(tidy(est0))
# r2py:entity:augment
print(augment(est0, df0))

# add month fixed effects
# r2py:entity:est1
# felm(Ozone ~ Temp + Wind + Solar.R | Month, airquality)
df1 = airquality[['Ozone', 'Temp', 'Wind', 'Solar.R', 'Month']].dropna()
df1 = df1.set_index(['Month', df1.index])
X1 = sm.add_constant(df1[['Temp', 'Wind', 'Solar.R']])
y1 = df1['Ozone']
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# summarize model fit with tidiers
# r2py:entity:tidy_1
print(tidy(est1))
# r2py:entity:tidy_2
print(tidy(est1, fe=True))
# r2py:entity:augment_1
print(augment(est1, df1))
# r2py:entity:glance
print(glance(est1))

# The "se.type" argument
# r2py:entity:tidy_3
est1_iid = est1.fit(cov_type='unadjusted')
print(tidy(est1_iid))
# r2py:entity:tidy_4
est1_robust = est1.fit(cov_type='robust')
print(tidy(est1_robust))

# add clustered SEs (also by month)
# r2py:entity:est2
# felm(Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month, airquality)
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# summarize model fit with tidiers
# r2py:entity:tidy_5
print(tidy(est2, conf_int=True))
# r2py:entity:tidy_6
print(tidy(est2.fit(cov_type='clustered', cluster_entity=True), conf_int=True))
# r2py:entity:tidy_7
print(tidy(est2.fit(cov_type='robust'), conf_int=True))
# r2py:entity:tidy_8
print(tidy(est2.fit(cov_type='unadjusted'), conf_int=True))