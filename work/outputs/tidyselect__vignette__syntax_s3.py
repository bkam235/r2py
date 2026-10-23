# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd

# r2py:entity:select_loc
def select_loc(data, *args):
    """
    Select columns from a pandas DataFrame.
    Equivalent to the provided R select_loc function.
    """
    return data[list(args)]

# r2py:entity:rename_loc
def rename_loc(data, **kwargs):
    """
    Rename columns in a pandas DataFrame.
    Equivalent to the provided R rename_loc function.
    Usage: rename_loc(df, new_name='old_name')
    """
    # R's rename is new = old, pandas rename is {'old': 'new'}
    inv_map = {v: k for k, v in kwargs.items()}
    return data.rename(columns=inv_map)