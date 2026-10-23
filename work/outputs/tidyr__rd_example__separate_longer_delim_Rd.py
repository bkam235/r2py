# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np

# r2py:entity:separate_longer_delim
def separate_longer_delim(data, cols, delim):
    """
    Equivalent to tidyr::separate_longer_delim.
    Splits a column by a delimiter and expands the data frame.
    """
    df = data.copy()
    if isinstance(cols, str):
        cols = [cols]
    
    # Split specified columns into lists
    for col in cols:
        df[col] = df[col].str.split(delim)
    
    # Use explode to expand the lists into rows
    # We explode sequentially for each column specified
    for col in cols:
        df = df.explode(col)
    
    return df.reset_index(drop=True)

# r2py:entity:separate_longer_position
def separate_longer_position(data, cols, width, keep_empty=False):
    """
    Equivalent to tidyr::separate_longer_position.
    Splits a column by a fixed length and expands the data frame.
    """
    df = data.copy()
    if isinstance(cols, str):
        cols = [cols]

    def split_pos(val):
        if pd.isna(val):
            return [np.nan]
        val = str(val)
        # R's separate_longer_position splits into chunks of 'width'
        # Example: "abcde", width 2 -> "ab", "cd", "e"
        res = [val[i:i+width] for i in range(0, len(val), width)]
        if not keep_empty and "" in res:
            res = [x for x in res if x != ""]
        return res if res else [np.nan]

    for col in cols:
        df[col] = df[col].apply(split_pos)
    
    for col in cols:
        df = df.explode(col)
        
    return df.reset_index(drop=True)

# --- Example 1 ---
# r2py:entity:df
df = pd.DataFrame({'id': range(1, 5), 'x': ["x", "x y", "x y z", np.nan]})
# r2py:entity:separate_longer_delim
print(separate_longer_delim(df, 'x', delim=" "))

# --- Example 2 ---
# You can separate multiple columns at once if they have the same structure
# r2py:entity:df_1
df = pd.DataFrame({'id': range(1, 4), 'x': ["x", "x y", "x y z"], 'y': ["a", "a b", "a b c"]})
# r2py:entity:separate_longer_delim_1
print(separate_longer_delim(df, ['x', 'y'], delim=" "))

# --- Example 3 ---
# Or instead split by a fixed length
# r2py:entity:df_2
df = pd.DataFrame({'id': range(1, 4), 'x': ["ab", "def", ""]})
# r2py:entity:separate_longer_position
print(separate_longer_position(df, 'x', 1))
# r2py:entity:separate_longer_position_1
print(separate_longer_position(df, 'x', 2))
# r2py:entity:separate_longer_position_2
print(separate_longer_position(df, 'x', 2, keep_empty=True))