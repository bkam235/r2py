# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import numpy as np
import pandas as pd

# r2py:entity:add_two
def add_two(x, y, na_rm=True):
    if na_rm:
        return np.nansum([x, y])
    else:
        return np.sum([x, y])