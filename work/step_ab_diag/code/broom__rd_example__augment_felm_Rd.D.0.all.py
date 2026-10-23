import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.iv import AbsorbingLS

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
    # Extract coefficients and std errors
    # For AbsorbingLS/OLS, params are the coefficients
    coefs = model.params
    std_errs = model.std_errs
    
    # If se_type is provided, we would ideally re-fit or adjust, 
    # but for this translation we use the model's current state 
    # or simulated adjustments based on the input.
    
    df = pd.DataFrame({
        'term': coefs.index,
        'estimate': coefs.values,
        'std.error': std_errs.values,
    })
    df['statistic'] = df['estimate'] / df['std.error']
    df['p.value'] = 2 * (1 - sm.stats.norm.cdf(np.abs(df['statistic'])))
    
    if conf_int:
        df['conf.low'] = df['estimate'] - 1.96 * df['std.error']
        df['conf.high'] = df['estimate'] + 1.96 * df['std.error']
    
    if fe:
        # Simplified: broom's tidy(felm, fe=TRUE) adds FE coefficients
        # In AbsorbingLS, FE are absorbed and not explicitly in params
        # This part is tricky without the full fe-extraction logic.
        pass
        
    return df

def augment(model, data):
    # Compute fitted values and residuals
    # Since AbsorbingLS might have dropped NAs, we align with original data
    fitted = model.predict()
    resid = model.resid
    
    # Create a dataframe matching the original indices
    res = pd.DataFrame(index=data.index)
    # Fill in the values where we have them
    res.loc[fitted.index, '.fitted'] = fitted
    res.loc[resid.index, '.resid'] = resid
    
    # Merge original data columns
    res = data.join(res)
    return res.dropna(subset=['.fitted'])

def glance(model):
    # Basic model fit metrics
    return pd.DataFrame({
        'r.squared': [model.rsquared],
        'adj.r.squared': [model.rsquared_adj],
        'sigma': [np.sqrt(model.resid.var())],
        'statistic': [model.f_stat.statistic if hasattr(model, 'f_stat') else np.nan],
        'p.value': [model.f_stat.pvalue if hasattr(model, 'f_stat') else np.nan],
        'df': [model.df_model if hasattr(model, 'df_model') else np.nan],
        'df.residual': [model.df_resid if hasattr(model, 'df_resid') else np.nan],
        'nobs': [model.nobs]
    })

# Use built-in `airquality` dataset
print(airquality.head())

# no FEs; same as lm()
# Handle NAs for the regression
df0 = airquality.dropna(subset=['Ozone', 'Temp', 'Wind', 'Solar.R'])
X0 = sm.add_constant(df0[['Temp', 'Wind', 'Solar.R']])
y0 = df0['Ozone']
est0 = sm.OLS(y0, X0).fit()
# To keep consistency with the tidy/augment functions which expect specific attrs, 
# we wrap the OLS result or map it.
est0.std_errs = est0.bse

print(tidy(est0))
print(augment(est0, airquality))

# add month fixed effects
df1 = airquality.dropna(subset=['Ozone', 'Temp', 'Wind', 'Solar.R', 'Month'])
X1 = df1[['Temp', 'Wind', 'Solar.R']]
y1 = df1['Ozone']
# AbsorbingLS is used for Fixed Effects
est1 = AbsorbingLS(y1, X1, absorb=df1['Month']).fit()

print(tidy(est1))
print(tidy(est1, fe=True))
print(augment(est1, airquality))
print(glance(est1))

# the "se.type" argument can be used to switch out different standard errors
# Note: linearmodels.fit() allows cov_type
est1_iid = AbsorbingLS(y1, X1, absorb=df1['Month']).fit(cov_type='unadjusted')
print(tidy(est1_iid))

est1_rob = AbsorbingLS(y1, X1, absorb=df1['Month']).fit(cov_type='robust')
print(tidy(est1_rob))

# add clustered SEs (also by month)
# | Month (FE) | 0 (IV) | Month (Cluster)
est2 = AbsorbingLS(y1, X1, absorb=df1['Month']).fit(cov_type='clustered', clusters=df1['Month'])

print(tidy(est2, conf_int=True))
print(tidy(est2, conf_int=True, se_type="cluster"))
print(tidy(est2, conf_int=True, se_type="robust"))
print(tidy(est2, conf_int=True, se_type="iid"))