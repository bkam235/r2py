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
    """Approximate broom::tidy for statsmodels and linearmodels."""
    if hasattr(model, 'params'):
        params = model.params
        std_err = model.std_errors
        t_stats = model.tstats
        p_vals = model.pvalues
        
        df = pd.DataFrame({
            'term': params.index,
            'estimate': params.values,
            'std.error': std_err.values,
            'statistic': t_stats.values,
            'p.value': p_vals.values
        })
        
        if conf_int:
            df['conf.low'] = df['estimate'] - 1.96 * df['std.error']
            df['conf.high'] = df['estimate'] + 1.96 * df['std.error']
            
        return df
    return None

def augment(model, data=None):
    """Approximate broom::augment."""
    # For statsmodels/linearmodels, we return fitted values and residuals
    # We assume the model object has the necessary attributes
    if hasattr(model, 'predict'):
        # This is simplified; in R augment returns a df with .fitted and .resid
        fitted = model.predict()
        # Handle residuals (some models use .resid, others .resids)
        resid = getattr(model, 'resid', getattr(model, 'resids', None))
        return pd.DataFrame({'fitted': fitted, 'resid': resid})
    return None

def glance(model):
    """Approximate broom::glance."""
    results = {}
    if hasattr(model, 'rsquared'):
        results['r.squared'] = model.rsquared
    if hasattr(model, 'nobs'):
        results['nobs'] = model.nobs
    return pd.DataFrame([results])

# r2py:entity:head
print(airquality.head())

# est0: no FEs; same as lm()
# r2py:entity:est0
X0 = sm.add_constant(airquality[['Temp', 'Wind', 'Solar.R']])
y0 = airquality['Ozone']
est0 = sm.OLS(y0, X0).fit()

# r2py:entity:tidy
print(tidy(est0))
# r2py:entity:augment
print(augment(est0))

# est1: add month fixed effects
# r2py:entity:est1
# To implement felm(Ozone ~ Temp + Wind + Solar.R | Month, airquality)
# We use PanelOLS with entity_effects=True, setting Month as the entity index
df_est1 = airquality.copy()
df_est1['obs_id'] = range(len(df_est1))
df_est1 = df_est1.set_index(['Month', 'obs_id'])
y1 = df_est1['Ozone']
X1 = sm.add_constant(df_est1[['Temp', 'Wind', 'Solar.R']])
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# r2py:entity:tidy_1
print(tidy(est1))
# r2py:entity:tidy_2
print(tidy(est1, fe=True))
# r2py:entity:augment_1
print(augment(est1))
# r2py:entity:glance
print(glance(est1))

# se.type arguments
# r2py:entity:tidy_3
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est1_iid))

# r2py:entity:tidy_4
est1_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est1_robust))

# est2: add clustered SEs (also by month)
# r2py:entity:est2
# felm(Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month, airquality)
# Cluster by Month (which is our entity index)
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

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