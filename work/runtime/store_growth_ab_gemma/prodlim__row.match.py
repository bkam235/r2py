import numpy as np
import pandas as pd

def r_row_match(x, table, nomatch=np.nan):
    """
    Python implementation of prodlim::row.match.
    """
    # Handle table conversion: inherits(table, "matrix") -> as.data.frame(table)
    if isinstance(table, np.ndarray):
        table_df = pd.DataFrame(table)
    elif isinstance(table, pd.DataFrame):
        table_df = table
    else:
        # For lists of lists or dicts
        table_df = pd.DataFrame(table)

    # Handle x conversion: is.null(dim(x)) -> as.data.frame(matrix(x, nrow = 1))
    if isinstance(x, np.ndarray):
        if x.ndim == 1:
            x_df = pd.DataFrame([x])
        else:
            x_df = pd.DataFrame(x)
    elif isinstance(x, list):
        # R's c(1, "a") results in a character vector. 
        # If x is a list/vector, it's treated as a single row if it has no dim.
        x_df = pd.DataFrame([x])
    elif isinstance(x, pd.DataFrame):
        x_df = x
    else:
        # Scalar
        x_df = pd.DataFrame([[x]])

    # R's do.call("paste", c(df, sep = "\r")):
    # R's paste() on a dataframe with sep="\r" concatenates all columns for each row.
    # Crucially, R converts all elements to character. 
    # In R, paste(1, "a", sep="\r") is "1\ra".
    
    def r_paste_df(df):
        # We must ensure we are treating the dataframe as a collection of columns.
        # df.astype(str) is close, but R's string conversion for numbers 
        # avoids trailing .0 for integers.
        def to_r_str(val):
            if pd.isna(val):
                return "NA"
            # If it's a float that's actually an integer, R's paste converts it to "1" not "1.0"
            if isinstance(val, float) and val.is_integer():
                return str(int(val))
            return str(val)

        # Apply to_r_str to every element, then join by \r
        # We use a list comprehension to avoid pandas' dtype coercion issues
        rows = []
        for row in df.values:
            rows.append("\r".join([to_r_str(v) for v in row]))
        return np.array(rows)

    cx = r_paste_df(x_df)
    ct = r_paste_df(table_df)

    # match(cx, ct, nomatch = nomatch)
    # Returns the 1-based index of the first match in ct for each element in cx.
    lookup = {}
    for i, val in enumerate(ct):
        if val not in lookup:
            lookup[val] = i + 1

    results = []
    for val in cx:
        res = lookup.get(val, nomatch)
        results.append(res)

    # Return as numpy array
    res_array = np.array(results)
    
    # Return as integer if no NAs are present, otherwise float (to accommodate NaN)
    if np.any(pd.isna(res_array)):
        return res_array.astype(float)
    else:
        return res_array.astype(int)
