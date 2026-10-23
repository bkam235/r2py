# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import numpy as np
import pandas as pd

# r2py:entity:vec_math.vctrs_cached_sum
def vec_math_vctrs_cached_sum(fn, x, **kwargs):
    # In Python/Pandas, we can store cached attributes in a custom object 
    # or a dictionary, as standard numpy arrays don't have a 'sum' attribute 
    # in the same way R attributes work.
    
    cached_sum = getattr(x, "sum_cache", None)
    
    if fn == "sum":
        return cached_sum if cached_sum is not None else np.sum(x)
    elif fn == "mean":
        return (cached_sum / len(x)) if cached_sum is not None else np.mean(x)
    else:
        # Simple substitute for vec_math_base
        return getattr(np, fn)(x, **kwargs)