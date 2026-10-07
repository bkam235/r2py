import numpy as np
import pandas as pd

def r_paste(*args, sep=" ", collapse=None, recycle0=False, **kwargs):
    processed_args = []
    for arg in args:
        # Handle matrices/dataframes/arrays by flattening to 1D as R does for paste()
        if isinstance(arg, (np.ndarray, pd.Series, pd.DataFrame)):
            # R's paste() flattens matrices column-major (Fortran order)
            if isinstance(arg, pd.DataFrame):
                # Convert DF to numpy and flatten in F order
                flat = arg.values.flatten(order='F')
            else:
                # numpy arrays: ensure we flatten in Fortran order to match R's matrix behavior
                flat = np.array(arg).flatten(order='F')
            processed_args.append(flat.astype(object))
        elif isinstance(arg, list):
            processed_args.append(np.array(arg, dtype=object))
        elif isinstance(arg, (int, float, str, bool, type(None))):
            processed_args.append(np.array([arg], dtype=object))
        else:
            processed_args.append(np.array([str(arg)], dtype=object))

    if not processed_args:
        res_list = [""]
    else:
        # Determine target length (max of all input lengths)
        lengths = [len(a) for a in processed_args]
        target_len = max(lengths)

        # Recycling shorter vectors
        expanded = []
        for a in processed_args:
            curr_len = len(a)
            if curr_len == target_len:
                expanded.append(a)
            else:
                reps = (target_len // curr_len) + 1
                tiled = np.tile(a, reps)[:target_len]
                expanded.append(tiled)

        def to_r_str(x):
            # Check for NaN/NA
            if pd.isna(x):
                return "NA"
            # Specifically handle the case where ints might be floats (e.g. 1.0 -> "1")
            if isinstance(x, float) and x.is_integer():
                return str(int(x))
            return str(x)

        res_list = []
        for i in range(target_len):
            row = [to_r_str(expanded[j][i]) for j in range(len(expanded))]
            res_list.append(sep.join(row))

    if collapse is not None:
        # collapse returns a single string as a vector element
        c_val = str(collapse)
        collapsed_str = c_val.join(res_list)
        return [collapsed_str]
    
    # Return as a list of strings (R character vector)
    return res_list
