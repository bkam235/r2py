# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__glance_varest_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__glance_varest_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Canada']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:import_vars
from statsmodels.tsa.vector_ar.var_model import VAR

# r2py:entity:tidy
def tidy(res):
    """Mimics broom::tidy for VAR model results."""
    params = res.params
    rows = []
    
    for col in params.columns:
        group = col
        # R's broom::tidy for varest typically lists lags first, then const, then trend
        # We sort the indices to ensure lags (L1.x) come before 'const' and 'trend'
        sorted_index = sorted(params.index, key=lambda x: (not x.startswith('L'), x))
        
        for idx in sorted_index:
            term = idx
            # Rename statsmodels terms to R's broom style: L1.e -> e.l1
            if term.startswith('L'):
                parts = term.split('.')
                term = f"{parts[1]}.{parts[0].lower()}"
            
            estimate = params.loc[idx, col]
            std_err = res.bse.loc[idx, col] if hasattr(res, 'bse') else np.nan
            stat = estimate / std_err if std_err != 0 else np.nan
            p_val = res.pvalues.loc[idx, col] if hasattr(res, 'pvalues') else np.nan
            
            rows.append({
                'group': group,
                'term': term,
                'estimate': estimate,
                'std.error': std_err,
                'statistic': stat,
                'p.value': p_val
            })
    
    return pd.DataFrame(rows)

# r2py:entity:glance
def glance(res):
    """Mimics broom::glance for VAR model results."""
    # R's varest glance: lag.order, logLik, nobs, n
    # Statsmodels llf is the total log-likelihood.
    nobs = res.nobs
    n = nobs + res.k_ar
    
    data = {
        'lag.order': res.k_ar,
        'logLik': res.llf,
        'nobs': nobs,
        'n': n
    }
    return pd.DataFrame([data])

# Canada is provided by shim as a list of lists
# r2py:entity:data
df_canada = pd.DataFrame(Canada, columns=['e', 'prod', 'rw', 'U'])

# R: VAR(Canada, p = 1, type = "both")
# 'both' means include constant and trend. 
# In statsmodels VAR.fit(), trend='ct' provides constant and linear trend.
# r2py:entity:mod
model = VAR(df_canada)
results = model.fit(1, trend='ct')

# tidy(mod)
# r2py:entity:tidy
tidy_df = tidy(results)
print(tidy_df.to_string())

# glance(mod)
# r2py:entity:glance
glance_df = glance(results)
print(glance_df.to_string())