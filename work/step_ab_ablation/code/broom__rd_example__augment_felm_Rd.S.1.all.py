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
    # Mock broom::tidy for statsmodels/linearmodels
    if hasattr(model, 'params'):
        res = pd.DataFrame({
            'term': model.params.index,
            'estimate': model.params.values,
            'std.error': model.bse.values if hasattr(model, 'bse') else np.nan,
            'statistic': model.tvalues.values if hasattr(model, 'tvalues') else np.nan,
            'p.value': model.pvalues.values if hasattr(model, 'pvalues') else np.nan
        })
        if conf_int:
            res['conf.low'] = res['estimate'] - 1.96 * res['std.error']
            res['conf.high'] = res['estimate'] + 1.96 * res['std.error']
        return res
    return None

def augment(model):
    # Mock broom::augment
    if hasattr(model, 'predict'):
        # Handle both statsmodels and linearmodels
        try:
            y_hat = model.predict()
            resid = model.resid
        except:
            # Fallback if predict requires X
            return pd.DataFrame()
        return pd.DataFrame({'fitted': y_hat, 'resid': resid})
    return pd.DataFrame()

def glance(model):
    # Mock broom::glance
    if hasattr(model, 'rsquared'):
        return pd.DataFrame({'r.squared': [model.rsquared], 'nobs': [model.nobs]})
    return pd.DataFrame()

# r2py:entity:head
print(airquality.head())

# est0: No FEs; same as lm()
# r2py:entity:est0
X0 = sm.add_constant(airquality[['Temp', 'Wind', 'Solar.R']])
y0 = airquality['Ozone']
est0 = sm.OLS(y0, X0).fit()

# summarize model fit with tidiers
# r2py:entity:tidy
print(tidy(est0))
# r2py:entity:augment
print(augment(est0))

# est1: add month fixed effects
# r2py:entity:est1
# PanelOLS requires a MultiIndex (entity, time)
df_panel = airquality.copy()
df_panel['obs_id'] = range(len(df_panel))
df_panel = df_panel.set_index(['Month', 'obs_id'])
X1 = sm.add_constant(df_panel[['Temp', 'Wind', 'Solar.R']])
y1 = df_panel['Ozone']
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# summarize model fit with tidiers
# r2py:entity:tidy_1
print(tidy(est1))
# r2py:entity:tidy_2
print(tidy(est1, fe=True))
# r2py:entity:augment_1
print(augment(est1))
# r2py:entity:glance
print(glance(est1))

# SE types for est1
# r2py:entity:tidy_3
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est1_iid))
# r2py:entity:tidy_4
est1_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est1_robust))

# est2: add clustered SEs (also by month)
# r2py:entity:est2
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# summarize model fit with tidiers
# r2py:entity:tidy_5
print(tidy(est2, conf_int=True))
# r2py:entity:tidy_6
est2_cluster = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)
print(tidy(est2_cluster, conf_int=True))
# r2py:entity:tidy_7
est2_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est2_robust, conf_int=True))
# r2py:entity:tidy_8
est2_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est2_iid, conf_int=True))