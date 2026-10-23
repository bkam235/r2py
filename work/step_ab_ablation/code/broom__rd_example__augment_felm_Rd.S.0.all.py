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
    """Mimics broom::tidy for statsmodels/linearmodels."""
    if hasattr(model, 'params'):
        params = model.params
        std_err = model.std_errors if hasattr(model, 'std_errors') else model.bse
        
        # Handle linearmodels result specifically
        if hasattr(model, 'summary_frame'):
            frame = model.summary_frame
            res = frame[['Coefficient', 'Std. Error']].reset_index()
            res.columns = ['term', 'estimate', 'std.error']
        else:
            res = pd.DataFrame({
                'term': params.index,
                'estimate': params.values,
                'std.error': std_err.values
            })
        
        if conf_int:
            res['conf.low'] = res['estimate'] - 1.96 * res['std.error']
            res['conf.high'] = res['estimate'] + 1.96 * res['std.error']
            
        return res
    return None

def augment(model, data):
    """Mimics broom::augment."""
    # Simplified: provide fitted and residuals
    # If it's a PanelOLS result, it has .predict()
    # If it's a statsmodels result, it has .predict()
    fitted = model.predict()
    resid = model.resid if hasattr(model, 'resid') else (data.iloc[:, 0] - fitted)
    
    aug = data.copy()
    aug['.fitted'] = fitted.values if hasattr(fitted, 'values') else fitted
    aug['.resid'] = resid.values if hasattr(resid, 'values') else resid
    return aug

def glance(model):
    """Mimics broom::glance."""
    # Extract basic metrics
    metrics = {}
    if hasattr(model, 'rsquared'):
        metrics['r.squared'] = model.rsquared
    if hasattr(model, 'nobs'):
        metrics['nobs'] = model.nobs
    return pd.DataFrame([metrics])

# r2py:entity:head
print(airquality.head())

# est0: no FEs; same as lm()
# r2py:entity:est0
y0 = airquality['Ozone']
X0 = sm.add_constant(airquality[['Temp', 'Wind', 'Solar.R']])
est0 = sm.OLS(y0, X0).fit()

# tidy(est0)
# r2py:entity:tidy
print(tidy(est0))
# augment(est0)
# r2py:entity:augment
print(augment(est0, airquality))

# est1: add month fixed effects
# r2py:entity:est1
# To use PanelOLS for FE, we need a multi-index (entity, time)
# Month is the entity.
d_panel = airquality.copy()
d_panel = d_panel.set_index(['Month', d_panel.index])
y1 = d_panel['Ozone']
X1 = sm.add_constant(d_panel[['Temp', 'Wind', 'Solar.R']])
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# tidy(est1)
# r2py:entity:tidy_1
print(tidy(est1))
# tidy(est1, fe = TRUE)
# r2py:entity:tidy_2
print(tidy(est1, fe=True))
# augment(est1)
# r2py:entity:augment_1
print(augment(est1, d_panel))
# glance(est1)
# r2py:entity:glance
print(glance(est1))

# SE types for est1
# tidy(est1, se.type = "iid")
# r2py:entity:tidy_3
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est1_iid))

# tidy(est1, se.type = "robust")
# r2py:entity:tidy_4
est1_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est1_robust))

# est2: add clustered SEs (also by month)
# r2py:entity:est2
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# tidy(est2, conf.int = TRUE)
# r2py:entity:tidy_5
print(tidy(est2, conf_int=True))
# tidy(est2, conf.int = TRUE, se.type = "cluster")
# r2py:entity:tidy_6
print(tidy(est2, conf_int=True)) # est2 is already clustered
# tidy(est2, conf.int = TRUE, se.type = "robust")
# r2py:entity:tidy_7
est2_robust = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est2_robust, conf_int=True))
# tidy(est2, conf.int = TRUE, se.type = "iid")
# r2py:entity:tidy_8
est2_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est2_iid, conf_int=True))