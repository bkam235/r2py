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
    # This function approximates broom::tidy for felm-like models
    # For statsmodels/linearmodels, we extract coefficients, std errors, t-stats, and p-values
    
    # In the case of est1/est2 (PanelOLS), we handle different cov_types
    if hasattr(model, 'params') and not hasattr(model, 'fit'): # It's already a result object
        res = model
    else:
        res = model

    # Extract basic stats
    df = pd.DataFrame({
        'term': res.params.index,
        'estimate': res.params.values,
        'std.error': res.std_errs.values,
        'statistic': res.tstats.values,
        'p.value': res.pvalues.values
    })
    
    if conf_int:
        conf = res.conf_int()
        df['conf.low'] = conf[0].values
        df['conf.high'] = conf[1].values
        
    if fe:
        # This is a simplification; felm FE coefficients are usually handled separately
        # In this specific R example, tidy(est1, fe=TRUE) shows the FE for months
        pass

    return df

def augment(model):
    # This function approximates broom::augment
    # Return a dataframe with the original data, fitted values and residuals
    # Since we don't have the original dataframe easily, we use the model's attributes
    
    # For the purpose of the example, we recreate the structure
    # We need the data used in the model
    # Since R's augment returns the original data + .fitted + .resid
    # we use a proxy based on the dataset airquality
    
    # This is simplified for the demonstration
    fitted = model.predict().values if hasattr(model, 'predict') else model.fitted_values
    resid = model.resid.values if hasattr(model, 'resid') else model.resids
    
    # The R augment returns a tibble including original columns
    # We return a dataframe with fitted and resid
    return pd.DataFrame({'fitted': fitted, 'resid': resid})

def glance(model):
    # This function approximates broom::glance
    return pd.DataFrame({
        'r.squared': [model.rsquared],
        'adj.r.squared': [model.rsquared_adj],
        'sigma': [np.sqrt(model.scale if hasattr(model, 'scale') else 0)],
        'nobs': [int(model.nobs)]
    }, index=[0])

# use built-in `airquality` dataset
print(airquality.head())

# no FEs; same as lm()
# Ozone ~ Temp + Wind + Solar.R
data0 = airquality[['Ozone', 'Temp', 'Wind', 'Solar.R']].dropna()
X0 = sm.add_constant(data0[['Temp', 'Wind', 'Solar.R']])
y0 = data0['Ozone']
est0 = sm.OLS(y0, X0).fit()

# summarize model fit with tidiers
print(tidy(est0))
print(augment(est0))

# add month fixed effects
# Ozone ~ Temp + Wind + Solar.R | Month
data1 = airquality[['Ozone', 'Temp', 'Wind', 'Solar.R', 'Month']].dropna()
# Prepare for PanelOLS: set index to (Month, observation_id)
data1 = data1.reset_index()
data1 = data1.set_index(['Month', 'index'])
X1 = sm.add_constant(data1[['Temp', 'Wind', 'Solar.R']])
y1 = data1['Ozone']
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# summarize model fit with tidiers
print(tidy(est1))
print(tidy(est1, fe=True))
print(augment(est1))
print(glance(est1))

# se.type switches
# iid
est1_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est1_iid))
# robust
est1_rob = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est1_rob))

# add clustered SEs (also by month)
# Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month
# Cluster by the entity effect (Month)
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# summarize model fit with tidiers
print(tidy(est2, conf_int=True))
# se.type = "cluster"
est2_cluster = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)
print(tidy(est2_cluster, conf_int=True))
# se.type = "robust"
est2_rob = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='robust')
print(tidy(est2_rob, conf_int=True))
# se.type = "iid"
est2_iid = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='unadjusted')
print(tidy(est2_iid, conf_int=True))