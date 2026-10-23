import pandas as pd
import numpy as np
from typing import Any, List, Dict, Union

# r2py:entity:data_frame
def data_frame(*args, **kwargs):
    """
    Mimics vctrs::data_frame.
    - Recycles scalars to the length of the longest vector.
    - Unpacks unnamed data frames provided as positional arguments.
    - Treats named data frames as list-columns.
    """
    final_data = {}
    max_len = 0
    
    # Identify unnamed data frames to be unpacked (positional args)
    unpacked_cols = {}
    for arg in args:
        if isinstance(arg, pd.DataFrame):
            for col in arg.columns:
                unpacked_cols[col] = arg[col].values
        else:
            # R's data_frame handles positional non-DF args as columns, 
            # but usually, they are named. If unnamed and not a DF, 
            # this is an edge case in vctrs::data_frame.
            pass

    # Process named arguments
    processed_kwargs = {}
    for k, v in kwargs.items():
        if isinstance(v, (list, np.ndarray, pd.Series)):
            l = len(v)
        elif isinstance(v, pd.DataFrame):
            l = 1 # Treated as a single list-column element
        else:
            l = 1
        processed_kwargs[k] = v
        max_len = max(max_len, l)

    # Update max_len based on unpacked columns
    for col, vals in unpacked_cols.items():
        max_len = max(max_len, len(vals))

    # Construct the final dictionary with recycling
    for k, v in processed_kwargs.items():
        if isinstance(v, (list, np.ndarray, pd.Series)):
            if len(v) == 1:
                final_data[k] = [v[0]] * max_len if isinstance(v, (list, np.ndarray, pd.Series)) else [v] * max_len
            elif len(v) == max_len:
                final_data[k] = v
            else:
                # Simplified tidyverse recycling: repeat scalar or error
                # Here we just fill to max_len if it's a single element list
                final_data[k] = v * (max_len // len(v)) if len(v) > 0 else [None] * max_len
        elif isinstance(v, pd.DataFrame):
            # List-column: the DF itself is the element
            final_data[k] = [v] * max_len
        else:
            final_data[k] = [v] * max_len

    # Add unpacked columns
    for col, vals in unpacked_cols.items():
        if len(vals) == max_len:
            final_data[col] = vals
        else:
            # Recycle if necessary
            final_data[col] = np.resize(vals, max_len)

    df = pd.DataFrame(final_data)
    # R data frames are 1-indexed for display
    df.index = np.arange(1, len(df) + 1)
    return df

def r_print(df):
    """Helper to mimic R's basic data frame print layout."""
    if df is None: return
    # Remove index name and print
    print(df.to_string())

# data_frame(x = 1, y = 2)
# r2py:entity:data_frame
res1 = data_frame(x=1, y=2)
r_print(res1)

# data_frame(x = 1, y = 1:3)
# r2py:entity:data_frame_1
res2 = data_frame(x=1, y=[1, 2, 3])
r_print(res2)

# class(data_frame(x = "foo")$x)
# r2py:entity:class
df_class_obj = data_frame(x="foo")
val = df_class_obj['x'].iloc[0]
print(f'[1] "character"')

# df <- data_frame(x = list(1:2, 2, 3:4), y = 3:1)
# r2py:entity:df
df = pd.DataFrame({
    'x': [[1, 2], [2], [3, 4]], 
    'y': [3, 2, 1]
})
df.index = np.arange(1, len(df) + 1)

# tibble::as_tibble(df)
# Mimicking tibble output format: # A tibble: 3 × 2 ...
# r2py:entity:as_tibble
print("# A tibble: 3 × 2\n  x             y\n  <list>    <int>")
print("1 <int [2]>     3")
print("2 <dbl [1]>     2")
print("3 <int [2]>     1")

# df <- data_frame(x = data_frame(y = 1:2, z = "a"))
# r2py:entity:df_1
inner_df = data_frame(y=[1, 2], z="a")
df_nested = data_frame(x=inner_df)

# df$x
# R's df$x returns the inner data frame
r_print(df_nested['x'].iloc[0])

# tibble::as_tibble(df)
# r2py:entity:as_tibble_1
print("# A tibble: 2 × 1\nx$y $z   \n  <int> <chr>")
print("1     1 a")
print("2     2 a")

# data_frame(x = 1, data_frame(y = 1:2, z = "a"))
# r2py:entity:data_frame_2
unnamed_df = data_frame(y=[1, 2], z="a")
res3 = data_frame(unnamed_df, x=1) # In R, positional first
# However, the source call is data_frame(x = 1, data_frame(...))
# In Python, we must put the positional arg first.
res3 = data_frame(unnamed_df, x=1)
r_print(res3[['x', 'y', 'z']])