# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import numpy as np
import pandas as pd

# r2py:entity:vec_c
def vec_c(*args):
    # Filter out None values (equivalent to compact)
    args = [arg for arg in args if arg is not None]
    
    if not args:
        return None

    # Use numpy to find the common type and concatenate
    # np.concatenate handles the casting to a common type automatically
    try:
        result = np.concatenate([np.asarray(arg) for arg in args])
        return result
    except ValueError:
        # Fallback for incompatible types (e.g., mixing strings and numbers)
        # Pandas series/arrays handle object-type mixing more like R's vec_c
        return pd.Series([item for arg in args for item in np.asarray(arg)]).values