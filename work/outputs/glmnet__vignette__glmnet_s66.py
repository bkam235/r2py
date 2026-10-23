# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np

# r2py:entity:uvar
def uvar(x, means=False):
    # x is expected to be a pandas DataFrame or numpy array
    if isinstance(x, pd.DataFrame):
        m = x.mean()
        v = x.var()
    else:
        m = np.mean(x, axis=0)
        v = np.var(x, axis=0, ddof=1)
        
    if means:
        return {"mean": m, "var": v}
    else:
        return v

# r2py:entity:vfilter
def vfilter(q=0.3):
    def filter_func(x, *args, **kwargs):
        v = uvar(x)
        # Convert to numpy array to handle indexing/quantile similarly to R
        v_values = v.values if hasattr(v, 'values') else v
        threshold = np.quantile(v_values, q)
        return np.where(v_values < threshold)[0]
    return filter_func