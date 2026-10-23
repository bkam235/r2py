# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__metafor_tidiers_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__metafor_tidiers_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['dat.bcg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from scipy import stats

# Access data from shim
dat_bcg_raw = globals().get('dat.bcg')
if dat_bcg_raw is None:
    raise ImportError("Data 'dat.bcg' not found in shim.")

df_input = pd.DataFrame(dat_bcg_raw)

# escalc(measure = "RR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat.bcg)
# r2py:entity:df
df = df_input.copy()
# For RR, yi = log( (ai/(ai+bi)) / (ci/(ci+di)) )
# vi = 1/ai + 1/bi + 1/ci + 1/di
df['yi'] = np.log(
    (df['tpos'] / (df['tpos'] + df['tneg'])) / 
    (df['cpos'] / (df['cpos'] + df['cneg']))
)
df['vi'] = (1.0 / df['tpos']) + (1.0 / df['tneg']) + (1.0 / df['cpos']) + (1.0 / df['cneg'])

# r2py:entity:meta_analysis
# rma(yi, vi, data = df, method = "EB")
yi = df['yi'].values
vi = df['vi'].values
w_fixed = 1.0 / vi

# Calculate Q for variance estimation
sum_w_yi = np.sum(w_fixed * yi)
sum_w = np.sum(w_fixed)
weighted_mean_fixed = sum_w_yi / sum_w

Q = np.sum(w_fixed * (yi - weighted_mean_fixed)**2)

# EB (Empirical Bayes) in metafor for a simple model is often approximated 
# by the DerSimonian-Laird estimator for tau^2
df_q = len(yi) - 1
sum_w_sq = np.sum(w_fixed**2)
tau2 = max(0, (Q - df_q) / (sum_w - (sum_w_sq / sum_w)))

# Random effects weights
w_random = 1.0 / (vi + tau2)
sum_w_rand = np.sum(w_random)
beta = np.sum(w_random * yi) / sum_w_rand
se = np.sqrt(1.0 / sum_w_rand)
zval = beta / se
pval = 2 * (1 - stats.norm.cdf(abs(zval)))

meta_analysis = {
    'beta': beta,
    'se': se,
    'zval': zval,
    'pval': pval,
    'tau2': tau2
}

# r2py:entity:tidy
def tidy(model):
    """Mimics broom::tidy for metafor rma objects"""
    return pd.DataFrame({
        'term': ['overall summary'],
        'type': ['summary'],
        'estimate': [model['beta']],
        'std.error': [model['se']],
        'statistic': [model['zval']],
        'p.value': [model['pval']]
    })

# Execution
# r2py:entity:tidy
result = tidy(meta_analysis)
print(result)