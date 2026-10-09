import numpy as np
import pandas as pd

def r_row_match(x, table, nomatch=np.nan):
    """
    Python implementation of prodlim::row.match
    """
    # Ensure table is a DataFrame
    if isinstance(table, np.ndarray):
        table = pd.DataFrame(table)
    elif not isinstance(table, pd.DataFrame):
        table = pd.DataFrame(table)

    # Handle x: if it's not a DataFrame, it's treated as a vector 
    # which R's matrix(x, nrow = 1) turns into a single row.
    if not isinstance(x, pd.DataFrame):
        # If x is passed as a list or numpy array, it's treated as a single row
        if isinstance(x, (list, np.ndarray)):
            # Create a DataFrame where the list elements are columns of one row
            x_df = pd.DataFrame([x])
        else:
            # Scalar case
            x_df = pd.DataFrame([[x]])
    else:
        x_df = x

    # R's `do.call("paste", c(x[, , drop = FALSE], sep = "\r"))`
    # This effectively treats the DataFrame as a list of columns and pastes them.
    # Crucially, R's as.character conversion for numbers (like 1, 2, 3) 
    # doesn't include a trailing .0.
    def r_paste_df(df):
        # Convert elements to string. We use a lambda to avoid pandas' 
        # default float string representation (e.g. '1.0' instead of '1')
        # to mimic R's paste behavior on numeric types.
        def to_r_str(val):
            if pd.isna(val):
                return "NA"
            if isinstance(val, (float, np.floating)):
                # If it's actually an integer, remove the .0
                if val.is_integer():
                    return str(int(val))
            return str(val)

        # Apply the string conversion across the dataframe and join by \r
        return df.applymap(to_r_str).apply(lambda row: "\r".join(row), axis=1).values

    cx = r_paste_df(x_df)
    ct = r_paste_df(table)

    # R: match(cx, ct, nomatch = nomatch)
    # Returns 1-based index of first occurrence.
    lookup = {}
    for i, val in enumerate(ct):
        if val not in lookup:
            lookup[val] = i + 1

    results = []
    for val in cx:
        results.append(lookup.get(val, nomatch))

    res_array = np.array(results)
    
    # Cast to int64 if all values are integers to match R's 'integer' class
    if np.all(np.modf(res_array)[0] == 0) and not np.isnan(res_array).any():
        return res_array.astype(np.int64)
    
    return res_array
