# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import warnings

# r2py:entity:add_two
def add_two(x, y, na_rm=None):
    if na_rm is not None:
        warnings.warn(
            "add_two(na_rm) is deprecated and will be dropped in the next release.",
            DeprecationWarning,
            stacklevel=2
        )
    
    # Using numpy for sum logic equivalent to R's sum(na.rm=True)
    import numpy as np
    return np.nansum([x, y]) if na_rm else np.sum([x, y])