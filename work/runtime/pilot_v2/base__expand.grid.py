import numpy as np
import pandas as pd

def r_expand_grid(*args, KEEP_OUT_ATTRS=True, stringsAsFactors=True, **kwargs):
    # In R, expand.grid(...) takes ... which can be named or unnamed arguments.
    # Python's *args is unnamed, **kwargs is named.
    # R's behavior: if the first arg is a list, it treats it as the set of arguments.
    
    # Combine args and kwargs into a list of values and a list of names
    actual_args = []
    names = []
    
    # Handle the "if (nargs == 1L && is.list(a1 <- args[[1L]]))" case
    # If the first positional argument is a dictionary (simulating a list with names), 
    # R uses that list.
    if len(args) == 1 and isinstance(args[0], dict):
        input_dict = args[0]
        # Note: R lists maintain order. Python dicts do too since 3.7.
        for k, v in input_dict.items():
            actual_args.append(v)
            names.append(k)
    else:
        # First, process positional arguments
        for i, arg in enumerate(args):
            # Special case: if the user passed KEEP_OUT_ATTRS or stringsAsFactors as positional
            # This is unlikely given the R signature, but we handle them as values if they 
            # aren't the specific named parameters.
            actual_args.append(arg)
            names.append(f"Var{i+1}")
        
        # Then process named arguments
        for k, v in kwargs.items():
            actual_args.append(v)
            names.append(k)

    # Remove the specific control arguments from the data if they were passed in kwargs
    # because in R, the ... is separate from KEEP.OUT.ATTRS and stringsAsFactors
    # (The function signature in R is expand.grid(..., KEEP.OUT.ATTRS = TRUE, ...))
    # However, in Python, we define them explicitly. If they are in kwargs, 
    # they are NOT part of the ...
    # But wait, the R function is `function (..., KEEP.OUT.ATTRS = TRUE, stringsAsFactors = TRUE)`.
    # In Python `def r_expand_grid(*args, KEEP_OUT_ATTRS=True, stringsAsFactors=True, **kwargs)`,
    # `kwargs` contains any named args that aren't KEEP_OUT_ATTRS or stringsAsFactors.
    
    # Re-evaluating the input gathering:
    final_args = []
    final_names = []
    
    # 1. Positional args
    for i, arg in enumerate(args):
        final_args.append(arg)
        final_names.append(f"Var{i+1}")
    
    # 2. Named args (kwargs)
    for k, v in kwargs.items():
        final_args.append(v)
        final_names.append(k)

    nargs = len(final_args)
    if nargs == 0:
        return pd.DataFrame()

    # lengths of inputs
    d = []
    for x in final_args:
        if isinstance(x, (list, np.ndarray, pd.Series)):
            d.append(len(x))
        elif isinstance(x, (int, float, str, bool)) or x is None:
            d.append(1)
        else:
            # Try to get length, otherwise 1
            try:
                d.append(len(x))
            except TypeError:
                d.append(1)

    orep = np.prod(d).astype(int)
    
    columns = {}
    rep_fac = 1
    
    if orep == 0:
        # R: for (i in iArgs) cargs[[i]] <- args[[i]][FALSE]
        for i in range(nargs):
            x = final_args[i]
            if isinstance(x, (list, np.ndarray, pd.Series)):
                columns[final_names[i]] = np.array([], dtype=np.array(x).dtype)
            else:
                columns[final_names[i]] = np.array([])
    else:
        for i in range(nargs):
            x = final_args[i]
            
            # Convert to numpy array for consistent indexing/repeating
            # R handles scalars as vectors of length 1
            if not isinstance(x, (list, np.ndarray, pd.Series)):
                x_vec = np.array([x])
            else:
                x_vec = np.array(x)
            
            nx = len(x_vec)
            
            # stringsAsFactors logic
            if stringsAsFactors and x_vec.dtype.kind in 'SU': # string or unicode
                # R factor: unique levels in order of appearance
                # we represent factors as lists of strings in this harness
                unique_vals = pd.unique(x_vec)
                # In R, factor is a specific type. Here we keep as is or cast.
                # The harness asks for factors as lists of str.
                # But expand.grid produces a dataframe. 
                pass

            # Calculate repeat patterns
            # x <- x[rep.int(rep.int(seq_len(nx), rep.int(rep_fac, nx)), orep)]
            # This is effectively: repeat each element rep_fac times, 
            # then repeat that whole block (orep / (nx * rep_fac)) times.
            
            current_orep = orep // (nx * rep_fac) if (nx * rep_fac) != 0 else 0
            
            # repeat each element rep_fac times
            repeated = np.repeat(x_vec, rep_fac)
            # repeat the whole sequence current_orep times
            full_col = np.tile(repeated, current_orep)
            
            columns[final_names[i]] = full_col
            rep_fac *= nx

    df = pd.DataFrame(columns)
    
    # R's expand.grid doesn't have a named index by default, 
    # but it is 1-based. pandas is 0-based.
    # The harness says to return the natural Python object.
    # DataFrames are returned as DataFrames.
    
    return df
