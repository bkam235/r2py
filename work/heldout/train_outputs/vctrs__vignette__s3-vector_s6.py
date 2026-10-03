# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:is_percent
def is_percent(x):
    return hasattr(x, "vctrs_percent")