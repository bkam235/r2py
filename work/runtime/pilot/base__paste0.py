import numpy as np
import pandas as pd

def r_paste0(*args, collapse=None, recycle0=False, **kwargs):
    # Combine positional and keyword arguments (R's ... includes named arguments)
    all_args = list(args)
    if kwargs:
        all_args.extend(kwargs.values())
    
    if not all_args:
        return ""

    # Convert all inputs to arrays to handle potential vectors
    processed_args = []
    for arg in all_args:
        if isinstance(arg, (np.ndarray, pd.Series, list)):
            # Convert to numpy array and ensure elements are converted to strings properly
            # R converts numbers to strings without .0 if they are integers
            arr = np.asanyarray(arg)
            processed_args.append(arr)
        else:
            # Handle scalars (including None/NaN)
            processed_args.append(np.array([arg]))

    # Determine the length of the longest vector to handle recycling
    max_len = max(len(a) for a in processed_args)
    
    # Recycled arrays to reach max_len
    result_vectors = []
    for a in processed_args:
        if len(a) < max_len:
            # R repeats the vector from the start
            reps = (max_len + len(a) - 1) // len(a)
            a_recycled = np.tile(a, reps)[:max_len]
            result_vectors.append(a_recycled)
        else:
            result_vectors.append(a)

    combined = []
    for i in range(max_len):
        row_strings = []
        for v in result_vectors:
            val = v[i]
            # R's handling of NA: paste(NA) returns "NA"
            if val is None or (isinstance(val, (float, np.float64, np.float32)) and np.isnan(val)):
                row_strings.append("NA")
            elif isinstance(val, (int, np.integer)):
                row_strings.append(str(val))
            elif isinstance(val, (float, np.float64, np.float32)):
                # R's default float to string conversion doesn't always add .0 if not needed,
                # but for paste0, we follow the standard string representation.
                # However, the test case implies 1:3 (integers) should be "1", "2", "3".
                # If it's a float that's an integer, R typically doesn't show .0
                if val.is_integer():
                    row_strings.append(str(int(val)))
                else:
                    row_strings.append(str(val))
            else:
                row_strings.append(str(val))
        combined.append("".join(row_strings))

    # Handle collapse
    if collapse is not None:
        return collapse.join(combined)
    
    # Return scalar if length 1, else numpy array
    if len(combined) == 1:
        return combined[0]
    else:
        return np.array(combined)
