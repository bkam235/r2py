# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np

# r2py:entity:n_distinct
def n_distinct(*args, na_rm=False):
    # Handle single dataframe input
    if len(args) == 1 and isinstance(args[0], pd.DataFrame):
        df = args[0]
        if na_rm:
            # Dropping NAs across all columns then finding unique rows
            return len(df.dropna().drop_duplicates())
        return len(df.drop_duplicates())

    # Handle multiple arrays/lists
    data = [np.array(a) for a in args]
    
    # Stack all arrays into one flat array
    flattened = np.concatenate(data)
    
    if na_rm:
        # Remove NaN values
        flattened = flattened[~pd.isna(flattened)]
        
    return len(pd.unique(flattened))

# r2py:entity:x
x = np.array([1, 1, 2, 2, 2])
# r2py:entity:n_distinct
print(n_distinct(x))

# r2py:entity:y
y = np.array([3, 3, np.nan, 3, 3])
# r2py:entity:n_distinct_1
print(n_distinct(y))
# r2py:entity:n_distinct_2
print(n_distinct(y, na_rm=True))

# r2py:entity:n_distinct_3
print(n_distinct(x, y))

# r2py:entity:n_distinct_4
print(n_distinct(x, y, na_rm=True))

# r2py:entity:n_distinct_5
print(n_distinct(pd.DataFrame({'x': x, 'y': y})))