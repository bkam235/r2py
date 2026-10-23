import numpy as np
import pandas as pd

def r_row_match(x, table, nomatch=np.nan):
    """
    Reproduces prodlim::row.match.
    
    R source:
    function (x, table, nomatch = NA) 
    {
        if (inherits(table, "matrix")) 
            table <- as.data.frame(table)
        if (is.null(dim(x))) 
            x <- as.data.frame(matrix(x, nrow = 1))
        cx <- do.call("paste", c(x[, , drop = FALSE], sep = "\r"))
        ct <- do.call("paste", c(table[, , drop = FALSE], sep = "\r"))
        match(cx, ct, nomatch = nomatch)
    }
    """
    # Convert table to DataFrame
    if isinstance(table, np.ndarray):
        table_df = pd.DataFrame(table)
    elif isinstance(table, pd.DataFrame):
        table_df = table
    else:
        table_df = pd.DataFrame(table)

    # Convert x to DataFrame
    # If x is 1D (numpy array or list), R treats it as a single row
    if isinstance(x, pd.DataFrame):
        x_df = x
    elif isinstance(x, np.ndarray) and x.ndim > 1:
        x_df = pd.DataFrame(x)
    elif isinstance(x, list) and (len(x) == 0 or not isinstance(x[0], (list, np.ndarray, pd.Series))):
        # 1D list/array -> 1 row
        x_df = pd.DataFrame([x])
    elif isinstance(x, list) and len(x) > 0 and isinstance(x[0], (list, np.ndarray, pd.Series)):
        x_df = pd.DataFrame(x)
    elif isinstance(x, np.ndarray) and x.ndim == 1:
        x_df = pd.DataFrame([x])
    else:
        # Scalar or other
        x_df = pd.DataFrame([x])

    def r_paste_rows(df):
        # R's paste() with sep="\r" across columns. 
        # R coerces NA to "NA" and elements to character.
        # we convert all to string, replace NaN with "NA", then join with \r.
        def format_val(v):
            if pd.isna(v):
                return "NA"
            # R's as.character for integers/floats typically doesn't use .0 for ints
            if isinstance(v, (float, np.floating)) and float(v).is_integer():
                return str(int(v))
            return str(v)

        # Apply row-wise concatenation
        return df.apply(lambda row: "\r".join(row.map(format_val)), axis=1)

    cx = r_paste_rows(x_df)
    ct = r_paste_rows(table_df)

    # match(cx, ct, nomatch) in R:
    # Returns the index of the first occurrence of cx in ct.
    # Indices are 1-based.
    
    # Create a map for ct values to their first 1-based index
    # ct.values is a pandas series of concatenated strings
    ct_vals = ct.values
    
    results = []
    for val in cx:
        try:
            # find first index where ct_vals == val
            idx = np.where(ct_vals == val)[0][0]
            results.append(idx + 1)
        except IndexError:
            # Not found
            results.append(nomatch)

    res_array = np.array(results)
    
    # If the result is a single value, R returns a scalar (integer/numeric)
    # but the example shows it returning an integer vector [1] 3. 
    # In R, match() always returns a vector.
    
    # Handle the dtype to mimic R's integer return when possible
    if np.all(np.floor(res_array) == res_array) and not np.isnan(res_array).any():
        return res_array.astype(int)
    
    return res_array
