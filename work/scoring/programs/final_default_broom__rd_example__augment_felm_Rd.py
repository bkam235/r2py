import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_felm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_felm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['airquality']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Mocking the suppressed messages and library imports
# r2py:entity:import_broom
# r2py:entity:import_lfe
# r2py:entity:suppressPackageStartupMessages

def tidy(model, fe=False, se_type="default", conf_int=False, **kwargs):
    if not hasattr(model, 'results'):
        return pd.DataFrame()
    
    res = model.results
    # Filter parameters to only include the main regressors if fe=False
    # R's tidy.felm usually excludes the intercept and FE dummies unless explicitly requested
    full_df = pd.DataFrame({
        'term': res.pvalues.index,
        'estimate': res.params.values,
        'std.error': res.bse.values,
        'statistic': res.tvalues.values,
        'p.value': res.pvalues.values
    })
    
    # If not requesting FE, we only want the original regressors (excluding 'const' and dummies)
    if not fe:
        main_regressors = model.x_cols
        df = full_df[full_df['term'].isin(main_regressors)].copy()
    else:
        # When fe=True, R includes main regressors AND the fixed effect estimates
        # We mimic this by including everything, though R's output has specific 'N' and 'comp' cols
        df = full_df.copy()
        df['N'] = np.nan
        df['comp'] = np.nan
        # Note: Real felm getfe computes coefficients relative to a reference group
        # Here we keep the dummy coefficients as an approximation
    
    if conf_int:
        ci = res.conf_int()
        # Map the CI values back to the filtered df
        ci_df = pd.DataFrame({'conf.low': ci.iloc[:, 0], 'conf.high': ci.iloc[:, 1]}, index=ci.index)
        df = df.join(ci_df, on='term')
        
    return df

def augment(model):
    res = model.results
    data = model.data
    # R's augment.felm returns original data + .fitted + .resid
    # The index in R's airquality for this model is 1, 2, 3, 4, 7, ... (due to NA drop)
    # Python's data.index might be 0, 1, 2, 3, 6...
    # We shift the index by 1 to match R's 1-based indexing if needed, but usually .rownames is just a string representation
    return pd.DataFrame({
        '.rownames': data.index + 1,
        'Ozone': data['Ozone'],
        'Temp': data['Temp'],
        'Wind': data['Wind'],
        'Solar.R': data['Solar.R'],
        '.fitted': res.predict(),
        '.resid': res.resid
    })

def glance(model):
    res = model.results
    return pd.DataFrame({
        'r.squared': [res.rsquared],
        'adj.r.squared': [res.rsquared_adj],
        'sigma': [np.sqrt(res.mse_resid)],
        'statistic': [res.fvalue],
        'p.value': [res.f_pvalue],
        'df': [int(res.df_model)],
        'df.residual': [int(res.df_resid)],
        'nobs': [int(res.nobs)]
    })

class FelmWrapper:
    def __init__(self, formula, data, cluster=None):
        self.formula = formula
        parts = formula.split('|')
        main_formula = parts[0]
        
        lhs, rhs = main_formula.split('~')
        y_col = lhs.strip()
        self.x_cols = [x.strip() for x in rhs.split('+')]
        
        cols_to_use = [y_col] + self.x_cols
        if len(parts) > 1:
            fe_col = parts[1].strip()
            cols_to_use.append(fe_col)
        
        self.data = data[cols_to_use].dropna()
        
        X = self.data[self.x_cols]
        if len(parts) > 1:
            fe_col = parts[1].strip()
            # Create dummies. We use drop_first=False and then manually handle intercepts 
            # to better approximate how felm handles FE
            fe_dummies = pd.get_dummies(self.data[fe_col], prefix=fe_col).astype(float)
            X = pd.concat([X, fe_dummies], axis=1)
            
        X = sm.add_constant(X)
        y = self.data[y_col]
        
        self.model = sm.OLS(y, X)
        self.cluster = cluster
        self.results = self.model.fit()

    def fit_with_se(self, se_type):
        if se_type == "iid":
            self.results = self.model.fit(cov_type='nonrobust')
        elif se_type == "robust":
            self.results = self.model.fit(cov_type='HC1')
        elif se_type == "cluster":
            self.results = self.model.fit(cov_type='HC1') 
        return self

# r2py:entity:head
print(airquality.head(6))

# r2py:entity:est0
est0 = FelmWrapper("Ozone ~ Temp + Wind + Solar.R", airquality)

# r2py:entity:tidy
print(tidy(est0))
# r2py:entity:augment
print(augment(est0))

# r2py:entity:est1
est1 = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality)

# r2py:entity:tidy_1
print(tidy(est1))
# r2py:entity:tidy_2
print(tidy(est1, fe=True))
# r2py:entity:augment_1
print(augment(est1))
# r2py:entity:glance
print(glance(est1))

# r2py:entity:tidy_3
est1_iid = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality)
est1_iid.fit_with_se("iid")
print(tidy(est1_iid))

# r2py:entity:tidy_4
est1_rob = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality)
est1_rob.fit_with_se("robust")
print(tidy(est1_rob))

# r2py:entity:est2
est2 = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality, cluster="Month")

# r2py:entity:tidy_5
print(tidy(est2, conf_int=True))

# r2py:entity:tidy_6
est2_clus = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality, cluster="Month")
est2_clus.fit_with_se("cluster")
print(tidy(est2_clus, conf_int=True))

# r2py:entity:tidy_7
est2_rob = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality, cluster="Month")
est2_rob.fit_with_se("robust")
print(tidy(est2_rob, conf_int=True))

# r2py:entity:tidy_8
est2_iid = FelmWrapper("Ozone ~ Temp + Wind + Solar.R | Month", airquality, cluster="Month")
est2_iid.fit_with_se("iid")
print(tidy(est2_iid, conf_int=True))