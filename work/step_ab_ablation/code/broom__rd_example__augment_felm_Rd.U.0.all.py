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
    if hasattr(model, 'params'):
        params = model.params
        std_err = model.std_errors
        t_stat = model.tstats
        p_val = model.pvalues
        
        df = pd.DataFrame({
            'term': params.index,
            'estimate': params.values,
            'std.error': std_err.values,
            'statistic': t_stat.values,
            'p.value': p_val.values
        })
        
        if conf_int:
            df['conf.low'] = df['estimate'] - 1.96 * df['std.error']
            df['conf.high'] = df['estimate'] + 1.96 * df['std.error']
            
        return df
    return pd.DataFrame()

def augment(model, data):
    # Simple approximation of broom::augment for felm
    fitted = model.predict()
    resid = model.resid
    res = data.copy()
    res['.fitted'] = fitted
    res['.resid'] = resid
    return res

def glance(model):
    return pd.DataFrame({
        'r.squared': [model.rsquared],
        'adj.r.squared': [model.rsquared_adj],
        'nobs': [int(model.nobs)]
    })

# r2py:entity:head
print(airquality.head())

# est0: No FEs
# felm(Ozone ~ Temp + Wind + Solar.R, airquality)
df0 = airquality.dropna(subset=['Ozone', 'Temp', 'Wind', 'Solar.R'])
X0 = sm.add_constant(df0[['Temp', 'Wind', 'Solar.R']])
y0 = df0['Ozone']
# Using OLS to mimic felm without FEs
est0_sm = sm.OLS(y0, X0).fit()
# To keep consistency with PanelOLS objects used later, we wrap/assign
est0 = est0_sm

# r2py:entity:tidy
print(tidy(est0))

# r2py:entity:augment
print(augment(est0, df0))

# est1: Month Fixed Effects
# felm(Ozone ~ Temp + Wind + Solar.R | Month, airquality)
df1 = airquality.dropna(subset=['Ozone', 'Temp', 'Wind', 'Solar.R', 'Month'])
df1_panel = df1.set_index(['Month', df1.index])
X1 = sm.add_constant(df1_panel[['Temp', 'Wind', 'Solar.R']])
y1 = df1_panel['Ozone']
# entity_effects=True handles the fixed effect for 'Month'
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# r2py:entity:tidy_1
print(tidy(est1))

# r2py:entity:tidy_2
print(tidy(est1, fe=True))

# r2py:entity:augment_1
print(augment(est1, df1))

# r2py:entity:glance
print(glance(est1))

# SE Types for est1
# r2py:entity:tidy_3 (iid)
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est1_iid))

# r2py:entity:tidy_4 (robust)
est1_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est1_robust))

# est2: Month FE and Month Cluster
# felm(Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month, airquality)
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# r2py:entity:tidy_5
print(tidy(est2, conf_int=True))

# r2py:entity:tidy_6 (cluster)
est2_cluster = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)
print(tidy(est2_cluster, conf_int=True))

# r2py:entity:tidy_7 (robust)
est2_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est2_robust, conf_int=True))

# r2py:entity:tidy_8 (iid)
est2_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est2_iid, conf_int=True))