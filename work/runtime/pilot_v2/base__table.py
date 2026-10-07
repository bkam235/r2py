import numpy as np
import pandas as pd

def r_table(*args, exclude=None, useNA="no", dnn=None, deparse_level=1, **kwargs):
    # Combine args and kwargs into a list of inputs
    inputs = list(args)
    combined_data = []
    combined_names = []
    
    # 1. Positional args
    for i, val in enumerate(inputs):
        combined_data.append(val)
        combined_names.append(f"V{i+1}")
        
    # 2. Keyword args (excluding the control parameters)
    control_params = {'exclude', 'useNA', 'dnn', 'deparse_level'}
    for k, v in kwargs.items():
        if k not in control_params:
            combined_data.append(v)
            combined_names.append(k)

    # R's behavior: if the first argument is a list/dict, it's unpacked.
    if len(combined_data) == 1 and isinstance(combined_data[0], (list, dict, tuple)):
        if isinstance(combined_data[0], dict):
            item = combined_data[0]
            combined_data = list(item.values())
            combined_names = list(item.keys())
        else:
            # In R, if the first arg is a list, it treats it as a set of columns
            # But if it's a vector (which in Python might be passed as a list), 
            # we must determine if it's meant to be the data or the list of columns.
            # The R source says: if (length(args) == 1L && is.list(args[[1L]])) { args <- args[[1L]] }
            # In the context of the test cases failing, they are passing a single vector.
            # A single vector in Python is a list. We must distinguish between a "vector of data"
            # and a "list of vectors".
            # Usually, if it's a list of scalars (like [1, 2, NA, 1]), it's one column.
            first = combined_data[0]
            if len(first) > 0 and isinstance(first[0], (list, np.ndarray, pd.Series)):
                combined_data = list(first)
                combined_names = [f"V{i+1}" for i in range(len(combined_data))]
            else:
                # Keep it as a single column
                pass

    if not combined_data:
        raise ValueError("nothing to tabulate")

    # Handle defaults for useNA
    if useNA not in ["no", "ifany", "always"]:
        useNA = "no"
    
    if exclude is None:
        exclude = [np.nan] if useNA == "no" else []

    # Ensure all inputs are numpy arrays and have same length
    processed_arrays = []
    for x in combined_data:
        # Force to numpy array. Scalars become 1D arrays.
        arr = np.asanyarray(x)
        if arr.ndim == 0:
            arr = arr.reshape(1)
        processed_arrays.append(arr)
        
    lengths = [len(a) for a in processed_arrays]
    if len(set(lengths)) > 1:
        raise ValueError("all arguments must have the same length")
    n = lengths[0] if lengths else 0

    final_dims = []
    final_codes = [] 
    do_na = (useNA != "no")

    for arr in processed_arrays:
        a_obj = arr.astype(object)
        
        # Mask for values to exclude
        mask_exclude = np.zeros(n, dtype=bool)
        for ex in exclude:
            if pd.isna(ex):
                mask_exclude |= pd.isna(a_obj)
            else:
                mask_exclude |= (a_obj == ex)
                
        # Get unique sorted levels of non-excluded values
        non_excluded = a_obj[~mask_exclude]
        if non_excluded.size > 0:
            try:
                levels = np.unique(non_excluded)
            except TypeError:
                levels = np.unique(non_excluded.astype(str))
        else:
            levels = np.array([])

        current_levels = list(levels)
        has_na_in_data = np.any(pd.isna(a_obj))
        
        add_na_level = False
        if do_na:
            if useNA == "always" or (useNA == "ifany" and has_na_in_data):
                add_na_level = True
        
        if add_na_level:
            current_levels.append(np.nan)
            
        codes = np.full(n, -1, dtype=int)
        for idx, lvl in enumerate(current_levels):
            if pd.isna(lvl):
                # NA is assigned to the specific NA level if it exists
                mask = pd.isna(a_obj)
                codes[mask] = idx
            else:
                mask = (a_obj == lvl)
                codes[mask] = idx
        
        # Values in 'exclude' that aren't handled by the NA level remain -1
        # But if useNA == "no", we must ensure they are truly excluded.
        if not do_na:
            for ex in exclude:
                if not pd.isna(ex):
                    codes[a_obj == ex] = -1
            codes[pd.isna(a_obj)] = -1

        final_dims.append(len(current_levels))
        final_codes.append(codes)

    # Result array
    res = np.zeros(final_dims, dtype=np.int64)
    
    # Only rows where ALL dimensions have a valid level index (not -1) are counted
    valid_rows_mask = np.all(np.array(final_codes) != -1, axis=0)
    
    coords = np.array(final_codes)[:, valid_rows_mask].T
    for coord in coords:
        res[tuple(coord)] += 1
        
    # R's table returns a 1D array if only one input was provided
    if len(final_dims) == 1:
        return res.flatten()
        
    return res
