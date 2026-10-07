import numpy as np
import pandas as pd

def r_factor(x=None, levels=None, labels=None, exclude=np.nan, ordered=False, nmax=np.nan):
    # Handle R's default for x = character()
    if x is None:
        x_values = np.array([], dtype=object)
    else:
        # Ensure x is treated as an array-like object even if it's a scalar
        if isinstance(x, (pd.Series, pd.Index)):
            x_values = x.values
        elif isinstance(x, (list, np.ndarray)):
            x_values = np.asanyarray(x, dtype=object)
        else:
            # Scalar case
            x_values = np.array([x], dtype=object)

    # matchAsChar logic: is.object(x) || !(is.character(x) || is.integer(x) || is.logical(x))
    is_char = (x_values.dtype == object)
    is_int = np.issubdtype(x_values.dtype, np.integer)
    is_bool = np.issubdtype(x_values.dtype, np.bool_)
    
    match_as_char = not (is_char or is_int or is_bool)
    
    if match_as_char:
        x_values = x_values.astype(str)

    # Determine levels if missing
    if levels is None:
        # R's unique(x, nmax = nmax)
        y_list = []
        seen = set()
        
        limit = int(nmax) if not pd.isna(nmax) else len(x_values)
        search_space = x_values[:limit]
        
        for val in search_space:
            # Handle NaN as a distinct key for the set
            key = (val,) if pd.isna(val) else val
            if key not in seen:
                y_list.append(val)
                seen.add(key)
        
        # R's factor levels are sorted unique values (excluding NAs)
        clean_y = [val for val in y_list if not pd.isna(val)]
        # Sort using R's sort order (strings sorted alphabetically)
        clean_y.sort()
        levels = np.array(clean_y, dtype=object)
    else:
        levels = np.asanyarray(levels, dtype=object)

    # exclude logic: levels <- levels[is.na(match(levels, exclude))]
    if not pd.isna(exclude):
        exclude_vals = {exclude} if np.isscalar(exclude) else set(exclude)
        levels = np.array([l for l in levels if l not in exclude_vals], dtype=object)

    # f <- match(x, levels)
    res_indices = []
    lev_list = levels.tolist()
    for val in x_values:
        if pd.isna(val):
            res_indices.append(np.nan)
        else:
            try:
                res_indices.append(lev_list.index(val) + 1)
            except ValueError:
                res_indices.append(np.nan)
    
    f_indices = np.array(res_indices, dtype=float)

    # labels logic
    if labels is None:
        final_levels = [str(l) for l in levels]
    else:
        labels = np.asanyarray(labels, dtype=object)
        nlab = len(labels)
        nlev = len(levels)
        if nlab == nlev:
            xlevs = [str(l) for l in labels]
            nlevs = []
            seen_levs = set()
            for v in xlevs:
                if v not in seen_levs:
                    nlevs.append(v)
                    seen_levs.add(v)
            
            mapping = {val: i + 1 for i, val in enumerate(nlevs)}
            xlevs_ranks = np.array([mapping[v] for v in xlevs])
            
            new_f_indices = []
            for val in f_indices:
                if pd.isna(val):
                    new_f_indices.append(np.nan)
                else:
                    new_f_indices.append(xlevs_ranks[int(val)-1])
            f_indices = np.array(new_f_indices, dtype=float)
            final_levels = nlevs
        elif nlab == 1:
            label_prefix = str(labels[0])
            final_levels = [f"{label_prefix}{i+1}" for i in range(nlev)]
        else:
            raise ValueError(f"invalid 'labels'; length {nlab} should be 1 or {nlev}")

    # Convert indices back to the levels (labels)
    result_vals = []
    for val in f_indices:
        if pd.isna(val):
            result_vals.append(np.nan)
        else:
            idx = int(val) - 1
            if 0 <= idx < len(final_levels):
                result_vals.append(final_levels[idx])
            else:
                result_vals.append(np.nan)
                
    # The R harness expects a result compatible with the input shape.
    # If input x was a scalar, return a scalar.
    is_scalar_input = not isinstance(x, (list, np.ndarray, pd.Series, pd.Index))
    if is_scalar_input and len(result_vals) == 1:
        return result_vals[0]
        
    return result_vals
