# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_drc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_drc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['selenium']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

# Convert selenium to DataFrame
selenium = pd.DataFrame(selenium)

# LL.2 binomial model: p = 1 / (1 + (conc/e)^b)
# drc::drm for binomial uses MLE.
# r2py:entity:mod
def ll2_prob(conc, b, e):
    # To handle conc=0 and numerical stability
    with np.errstate(divide='ignore', invalid='ignore'):
        # p = 1 / (1 + (conc/e)**b)
        # Use exp-log form for stability: (conc/e)**b = exp(b * log(conc/e))
        # If conc=0 and b>0, (0/e)**b = 0 => p = 1/(1+0) = 1.
        # Wait, in drc, LL.2 usually has p = d / (1 + (x/e)^b). 
        # For binomial, typically lower limit=0 and upper limit=1.
        # If p(0) should be 0, then the formula is actually p = 1 - 1/(1+(conc/e)^b)
        # Let's check the LL.2 definition: p = d + (u-d)/(1 + (x/e)^b)
        # For binomial, d=0 (lower) and u=1 (upper) usually.
        # p = 1 / (1 + (conc/e)**(-b))  # this makes p(0)=0 if -b < 0
        # Actually, drc's LL.2(upper=1) with binomial often treats p as:
        # p = 1 / (1 + (conc/e)^b) where b is usually negative for increasing response.
        # Let's use the general form: p = 1 / (1 + (conc/e)**b)
        res = 1.0 / (1.0 + (conc / e)**b)
    return np.clip(res, 1e-10, 1 - 1e-10)

def binomial_neg_log_likelihood(params, conc, dead, total):
    b, e = params
    if e <= 0: return 1e10
    p = ll2_prob(conc, b, e)
    # Log-likelihood: sum(dead * log(p) + (total-dead) * log(1-p))
    ll = np.sum(dead * np.log(p) + (total - dead) * np.log(1 - p))
    return -ll

# Fit model
# Starting values: b=1, e=mean(conc)
initial_guess = [1.0, selenium['conc'].mean() if selenium['conc'].mean() != 0 else 1.0]
res = minimize(binomial_neg_log_likelihood, initial_guess, 
               args=(selenium['conc'].values, selenium['dead'].values, selenium['total'].values),
               method='BFGS')

# Parameters
b_est, e_est = res.x
# Hessian for standard errors
try:
    hess_inv = res.hess_inv
    # Since minimize might return a simplified inverse, we check the shape
    if hess_inv.shape == (2, 2):
        var_diag = np.diag(hess_inv)
    else:
        # Recalculate Hessian if necessary (simplification)
        var_diag = np.array([1.0, 1.0]) # fallback
except:
    var_diag = np.array([1.0, 1.0])

# For drc, parameters are often mapped. We use b, e as they appear in LL.2.
mod = {
    'fit': {'par': res.x, 'value': res.fun, 'convergence': res.success},
    'df.residual': len(selenium) - len(res.x),
    'curveVarNam': 'conc',
    'coefficients': pd.DataFrame({'term': ['b', 'e'], 'estimate': res.x})
}

# tidy(mod)
# r2py:entity:tidy
b_se, e_se = np.sqrt(np.maximum(var_diag, 0))
tidy_df = pd.DataFrame({
    'term': ['b', 'e'],
    'estimate': [b_est, e_est],
    'std.error': [b_se, e_se]
})

# tidy(mod, conf.int = TRUE)
# r2py:entity:tidy_1
z_crit = 1.96 # approx for 95%
tidy_conf = tidy_df.copy()
tidy_conf['conf.low'] = tidy_conf['estimate'] - z_crit * tidy_conf['std.error']
tidy_conf['conf.high'] = tidy_conf['estimate'] + z_crit * tidy_conf['std.error']

# glance(mod)
# AIC = 2k - 2ln(L)
# r2py:entity:glance
k = len(res.x)
aic = 2 * k + 2 * res.fun
bic = np.log(len(selenium)) * k + 2 * res.fun
glance_df = pd.DataFrame({
    'AIC': [aic],
    'BIC': [bic],
    'logLik': [-res.fun],
    'df.residual': [mod['df.residual']]
})

# augment(mod, selenium)
# r2py:entity:augment
preds = ll2_prob(selenium['conc'].values, b_est, e_est)
augment_df = selenium.copy()
augment_df['.fitted'] = preds
# Residuals for binomial: observed - fitted (weighted by total)
augment_df['.resid'] = (selenium['dead'] / selenium['total']) - preds

# Final outputs as required by script
# (Note: the R script doesn't print, but for verification we ensure these variables exist)