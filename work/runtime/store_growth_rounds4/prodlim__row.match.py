import numpy as np
import pandas as pd

def r_row_match(x, table, nomatch=np.nan):
    """
    Reproduces prodlim::row.match in R.
    """
    # --- Handle table ---
    # if (inherits(table, "matrix")) table <- as.data.frame(table)
    if isinstance(table, np.ndarray):
        table_df = pd.DataFrame(table)
    elif isinstance(table, pd.DataFrame):
        table_df = table
    else:
        # Handle cases where table might be a dict or other compatible type
        table_df = pd.DataFrame(table)

    # --- Handle x ---
    # if (is.null(dim(x))) x <- as.data.frame(matrix(x, nrow = 1))
    # In R, if x is a vector, it's converted to a matrix with 1 row.
    # Then it's converted to a data frame.
    if isinstance(x, pd.DataFrame):
        x_df = x
    elif isinstance(x, (np.ndarray, list)):
        # Treat as a single row (vector in R)
        # We create a DataFrame with 1 row and columns matching the length of x
        x_df = pd.DataFrame([x])
    else:
        # Scalar
        x_df = pd.DataFrame([[x]])

    # R's logic:
    # cx <- do.call("paste", c(x[, , drop = FALSE], sep = "\r"))
    # ct <- do.call("paste", c(table[, , drop = FALSE], sep = "\r"))
    # In R, paste() on a data frame treats each column as a separate argument.
    # For a 1-row data frame, it joins the elements of that row.
    
    def r_paste_df(df):
        # Convert to string. R's paste() handles NAs by converting to "NA"
        # and integers/floats without trailing zeros for whole numbers.
        # We ensure the string representation matches R's paste behavior.
        def to_r_str(val):
            if pd.isna(val):
                return "NA"
            # Float formatting to avoid .0 where R doesn't have it is complex,
            # but for the given examples, simple str() or format usually suffice.
            # We use a format that avoids scientific notation for these ranges.
            if isinstance(val, float):
                return ('%g' % val)
            return str(val)

        # Apply the conversion to every element
        df_str = df.applymap(to_r_str) if hasattr(df, 'applymap') else df.map(to_r_str)
        
        # Join columns with \r
        return df_str.apply(lambda row: "\r".join(row), axis=1).values

    cx = r_paste_df(x_df)
    ct = r_paste_df(table_df)

    # match(cx, ct, nomatch = nomatch)
    # returns the index of the first occurrence of each element of cx in ct.
    # 1-based indexing.
    results = []
    for val in cx:
        # Find indices where the string matches
        indices = np.where(ct == val)[0]
        if indices.size > 0:
            results.append(indices[0] + 1)
        else:
            results.append(nomatch)

    # Result should be a vector (numpy array)
    res_array = np.array(results)

    # If x was a vector (represented as 1 row in x_df), R returns a vector of results.
    # If x was a single vector and only one match is returned, 
    # we should return it as a vector if x was treated as a vector.
    
    # R's match() returns a vector of the same length as the first argument (cx).
    # If the result is essentially integers, return as int array.
    if np.all(np.isnan(res_array)) if res_array.dtype.kind == 'f' else False:
        return res_array
    
    # Filter out NaNs for type checking
    mask = ~np.isnan(res_array) if res_array.dtype.kind == 'f' else np.ones_like(res_array, dtype=bool)
    if np.all(res_array[mask] % 1 == 0) if res_array.dtype.kind == 'f' else True:
        # If nomatch is NA (NaN), we must return a float array or object array because ints can't be NaN
        if np.any(~mask):
            return res_array
        else:
            return res_array.astype(int)

    return res_array
