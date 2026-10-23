# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__augment_betamfx_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_betamfx_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x', 'y']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

# r2py:entity:set.seed
np.random.seed(12345)
# r2py:entity:n
n = 1000

# Data is provided by shim
# r2py:entity:d
d = pd.DataFrame({'y': y, 'x': x})

# r2py:entity:mod_betamfx
class BetaMFX:
    """
    Mimics the behavior of mfx::betamfx.
    Beta regression mean: mu = inv_logit(Xb)
    Marginal effect: dy/dx = mu * (1 - mu) * beta
    """
    def __init__(self, formula, data):
        self.data = data
        y = data['y'].values
        # We use a GLM with Binomial family as an approximation for the mean 
        # parameters of Beta regression (since both use the logit link).
        X = sm.add_constant(data[['x']])
        model = sm.GLM(y, X, family=sm.families.Binomial())
        res = model.fit()
        
        self.params = res.params
        self.cov = res.cov_params()
        self.mu = res.predict(X)
        self.nobs = len(y)
        self.df_resid = res.df_resid
        
        # Compute Marginal Effects (Average Marginal Effect - AME)
        # mfx_i = mu_i * (1 - mu_i) * beta_x
        beta_x = self.params[1]
        self.mfx_per_obs = self.mu * (1 - self.mu) * beta_x
        self.mfx_estimate = np.mean(self.mfx_per_obs)
        
        # Delta method for SE of AME: 
        # SE(AME) approx = sqrt(mean( (mu*(1-mu))^2 * var(beta_x) ))
        # This is a simplification of the mfx package's approach.
        var_beta_x = self.cov.iloc[1, 1]
        self.mfx_se = np.sqrt(np.mean((self.mu * (1 - self.mu))**2) * var_beta_x)
        
        # Model diagnostics (approximated to match R's betamfx/broom output)
        self.loglik = res.llf
        self.aic = res.aic
        self.bic = res.bic
        # Pseudo R2 for Beta regression often varies; using a simple ratio here
        # LogLik(null) / LogLik(full)
        null_model = sm.GLM(y, np.ones((self.nobs, 1)), family=sm.families.Binomial()).fit()
        self.pseudo_r2 = 1 - (null_model.llf / self.loglik)

# r2py:entity:tidy
    def tidy(self, conf_int=True):
        stat = self.mfx_estimate / self.mfx_se
        p_val = 2 * stats.norm.sf(np.abs(stat))
        
        df = pd.DataFrame({
            'term': ['x'],
            'atmean': [True],
            'estimate': [self.mfx_estimate],
            'std.error': [self.mfx_se],
            'statistic': [stat],
            'p.value': [p_val]
        })
        if conf_int:
            df['conf.low'] = df['estimate'] - 1.96 * df['std.error']
            df['conf.high'] = df['estimate'] + 1.96 * df['std.error']
        return df

# r2py:entity:augment
    def augment(self):
        res_df = self.data.copy()
        res_df['.fitted'] = self.mu
        # .cooksd is a diagnostic for influence. 
        # For betamfx, it's typically derived from the underlying beta regression.
        # We approximate with scaled residuals.
        residuals = self.data['y'].values - self.mu
        res_df['.cooksd'] = (residuals**2) / (np.var(self.data['y'].values) * self.nobs)
        return res_df

# r2py:entity:glance
    def glance(self):
        return pd.DataFrame({
            'pseudo.r.squared': [self.pseudo_r2],
            'df.null': [self.nobs - 1],
            'logLik': [self.loglik],
            'AIC': [self.aic],
            'BIC': [self.bic],
            'df.residual': [self.df_resid],
            'nobs': [self.nobs]
        })

# Initialize model
mod_betamfx = BetaMFX('y ~ x | x', d)

# r2py:entity:tidy
print(mod_betamfx.tidy(conf_int=True))

# r2py:entity:augment
print(mod_betamfx.augment())

# r2py:entity:glance
print(mod_betamfx.glance())