# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import pandas as pd
import numpy as np

# r2py:entity:list_c
def list_c(x, ptype=None):
    """
    Flatten a list into a vector.
    Equivalent to R's list_c or unlist().
    """
    # Convert list to a flat list of values
    flat_list = []
    for item in x.values() if isinstance(x, dict) else x:
        if isinstance(item, (list, np.ndarray, pd.Series)):
            flat_list.extend(item)
        else:
            flat_list.append(item)
    return np.array(flat_list)

# r2py:entity:list_rbind
def list_rbind(x, names_to=None, ptype=None):
    """
    Combine a list of data frames by row.
    """
    # Handle named vs unnamed list (dict vs list)
    if isinstance(x, dict):
        dfs = [df for df in x.values()]
        keys = list(x.keys())
    else:
        dfs = x
        keys = [None] * len(x)

    # In R, list_rbind with names_to creates a column with the list names
    combined = pd.concat(dfs, axis=0, ignore_index=True)
    
    if names_to is not None:
        # If we have keys, we use them; otherwise, we can't populate names_to
        if keys[0] is not None:
            # Repeat keys based on length of each dataframe
            id_col = []
            for k, df in zip(keys, dfs):
                id_col.extend([k] * len(df))
            combined.insert(0, names_to, id_col)
            
    return combined

# r2py:entity:list_cbind
def list_cbind(x, name_repair="unique", size=None):
    """
    Combine a list of data frames by column.
    """
    dfs = [df for df in x.values()] if isinstance(x, dict) else x
    return pd.concat(dfs, axis=1)

# --- Execution ---

# r2py:entity:x1
x1 = {'a': 1, 'b': 2, 'c': 3}
# r2py:entity:list_c
print(list_c(x1))

# r2py:entity:x2
x2 = {
    'a': pd.DataFrame({'x': [1, 2]}),
    'b': pd.DataFrame({'y': ['a']})
}

# r2py:entity:list_rbind
print(list_rbind(x2))
# r2py:entity:list_rbind_1
print(list_rbind(x2, names_to="id"))

# unname(x2) equivalent: convert dict to list of dataframes
# r2py:entity:list_rbind_2
x2_unnamed = list(x2.values())
print(list_rbind(x2_unnamed, names_to="id"))

# r2py:entity:list_cbind
print(list_cbind(x2))