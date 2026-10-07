import numpy as np
import pandas as pd
import builtins

def r_table(*args, exclude=None, useNA="no", dnn=None, deparse_level=1, **kwargs):
    # Handle R's default argument for exclude if not provided
    if exclude is None:
        if useNA == "no":
            exclude = [np.nan]
        else:
            exclude = []

    # Argument parsing for '...'
    inputs = list(args)
    
    # If kwargs were passed as data (e.g., x=..., y=...), add them to inputs
    # R's table() takes ... which handles named arguments.
    if kwargs:
        # In Python, the signature separates formal args from kwargs.
        # We treat kwargs as potential data columns if they aren't the formal options.
        # (The formal options are already explicitly listed in the signature).
        # Since Python's *args doesn't capture named args, we use kwargs.
        inputs.extend(kwargs.values())

    if not inputs:
        raise ValueError("nothing to tabulate")

    # R behavior: if first arg is a list/df, treat its elements as separate args
    if len(inputs) == 1 and isinstance(inputs[0], pd.DataFrame):
        inputs = [inputs[0][col] for col in inputs[0].columns]

    # Determine dnn (dimension names)
    if dnn is None:
        # If we have kwargs, we might have names. Otherwise, use default sequence.
        # This is a simplified reproduction of list.names()
        dnn = [f"V{i+1}" for i in range(len(inputs))]

    doNA = (useNA != "no")
    
    processed_inputs = []
    dim_names = []
    dims = []
    
    for a in inputs:
        # Convert to numpy array and flatten to match R vector behavior
        a = np.asanyarray(a).flatten()
        
        # Get unique values excluding NaNs for the basic levels
        mask_nan = pd.isna(a)
        non_nan_vals = a[~mask_nan]
        
        # R's factor levels are sorted
        unique_vals = np.unique(non_nan_vals)
        
        # Filter levels based on exclude
        current_levels = []
        for v in unique_vals:
            # check if v is in exclude
            is_excluded = False
            for ex in exclude:
                if pd.isna(ex) and pd.isna(v):
                    is_excluded = True; break
                if v == ex:
                    is_excluded = True; break
            if not is_excluded:
                current_levels.append(v)
        
        current_levels = np.array(current_levels)
        
        # Handle NA levels logic from R
        add_na = False
        if doNA:
            if useNA == "ifany":
                if np.any(mask_nan):
                    add_na = True
            elif useNA == "always":
                add_na = True
        
        if add_na:
            lvl_list = list(current_levels)
            lvl_list.append(np.nan)
            full_levels = np.array(lvl_list, dtype=object)
        else:
            full_levels = current_levels
            
        # Map input values to indices (1-based internally, 0-based for numpy)
        mapped = np.full(a.shape, np.nan)
        for idx, lvl in enumerate(full_levels):
            if pd.isna(lvl):
                mask = pd.isna(a)
            else:
                mask = (a == lvl)
            mapped[mask] = idx + 1
            
        processed_inputs.append(mapped)
        dim_names.append(full_levels)
        dims.append(len(full_levels))

    # Result array
    res = np.zeros(dims, dtype=np.int64)
    
    # Convert processed inputs to a coordinate array for indexing
    # Process inputs as a stack. 
    # For 1D case, coords will be (N, 1). For multi-D, (N, k).
    coords = np.array(processed_inputs) 
    
    # Find rows where no element is NaN
    # Use np.isnan on float representation
    valid_mask = ~np.isnan(coords).any(axis=0)
    
    # Extract valid coordinates and convert to 0-based integers
    # coords is (k, N), so we transpose to (N, k)
    valid_coords = coords[:, valid_mask].astype(int) - 1
    
    # Increment the counts
    # np.add.at expects (array, tuple_of_indices, value)
    # valid_coords.T provides the tuple of indices for each dimension
    np.add.at(res, tuple(valid_coords), 1)
    
    # Return result matching R's table output
    if len(dims) == 1:
        # R returns a vector (1D array in numpy)
        # If the result is a single value, R still treats it as a vector of length 1
        return res.flatten()
    
    return res
