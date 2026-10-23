import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_felm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_felm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['airquality']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def tidy(model, fe=False, se_type=None, conf_int=False):
    """Approximate broom::tidy for statsmodels/linearmodels"""
    if hasattr(model, 'params'):
        params = model.params
        std_err = model.std_errors
        t_stats = model.tstats
        p_vals = model.pvalues
    else:
        # Handle cases where fit() hasn't been called or we need a different SE type
        return pd.DataFrame()

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

def augment(model):
    """Approximate broom::augment"""
    # For PanelOLS/OLS, we need the original data to match lengths
    # In this specific script, we use the global airquality
    res = pd.DataFrame({
        '.fitted': model.predict().values if hasattr(model, 'predict') else np.nan,
        '.resid': model.resids.values if hasattr(model, 'resids') else model.resid.values
    })
    return res

def glance(model):
    """Approximate broom::glance"""
    return pd.DataFrame({
        'r.squared': [model.rsquared],
        'nobs': [int(model.nobs)]
    })

# r2py:entity:head
print(airquality.head())

# est0: Basic OLS
# felm(Ozone ~ Temp + Wind + Solar.R, airquality)
X0 = sm.add_constant(airquality[['Temp', 'Wind', 'Solar.R']])
y0 = airquality['Ozone']
est0 = sm.OLS(y0, X0).fit()
# r2py:entity:est0

# r2py:entity:tidy
print(tidy(est0))
# r2py:entity:augment
print(augment(est0))

# est1: Fixed Effects for Month
# felm(Ozone ~ Temp + Wind + Solar.R | Month, airquality)
df_est1 = airquality.copy()
df_est1 = df_est1.set_index(['Month', df_est1.index])
X1 = sm.add_constant(df_est1[['Temp', 'Wind', 'Solar.R']])
y1 = df_est1['Ozone']
est1 = PanelOLS(y1, X1, entity_effects=True).fit()
# r2py:entity:est1

# r2py:entity:tidy_1
print(tidy(est1))
# r2py:entity:tidy_2
print(tidy(est1, fe=True))
# r2py:entity:augment_1
print(augment(est1))
# r2py:entity:glance
print(glance(est1))

# SE types for est1
# tidy(est1, se.type = "iid")
# r2py:entity:tidy_3
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est1_iid))

# tidy(est1, se.type = "robust")
# r2py:entity:tidy_4
est1_rob = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est1_rob))

# est2: Fixed effects and Clustered SEs
# felm(Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month, airquality)
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)
# r2py:entity:est2

# r2py:entity:tidy_5
print(tidy(est2, conf_int=True))
# r2py:entity:tidy_6
est2_clust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)
print(tidy(est2_clust, conf_int=True))
# r2py:entity:tidy_7
est2_rob = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est2_rob, conf_int=True))
# r2py:entity:tidy_8
est2_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est2_iid, conf_int=True))