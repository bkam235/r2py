import numpy as np
import pandas as pd

def r_paste(*args, sep=" ", collapse=None, recycle0=False, **kwargs):
    # Collect all positional arguments into a list
    inputs = list(args)
    
    if not inputs:
        return ""

    # Convert all inputs to numpy arrays to handle vectorization
    processed_inputs = []
    for item in inputs:
        if isinstance(item, (list, np.ndarray, pd.Series)):
            processed_inputs.append(np.array(item, dtype=object))
        elif isinstance(item, pd.DataFrame):
            processed_inputs.append(np.array(item.values.flatten(), dtype=object))
        else:
            processed_inputs.append(np.array([item], dtype=object))

    # Determine the length of the resulting vector (max length among inputs)
    lengths = [len(x) for x in processed_inputs]
    max_len = max(lengths)
    
    # Expand inputs to match max_len via recycling
    expanded = []
    for x in processed_inputs:
        ln = len(x)
        if ln == 0:
            expanded.append(np.array([""] * max_len, dtype=object))
        else:
            reps = (max_len + ln - 1) // ln
            repeated = np.tile(x, reps)
            expanded.append(repeated[:max_len])

    def clean_val(v):
        # R converts NA to the string "NA"
        if v is None or (isinstance(v, (float, np.floating)) and np.isnan(v)):
            return "NA"
        
        # Handle numeric types to avoid trailing .0 for integers
        if isinstance(v, (int, np.integer)):
            return str(int(v))
        if isinstance(v, (float, np.floating)):
            # If it's a whole number, R's paste typically formats it without .0 
            # when it comes from an integer sequence like 1:3.
            # However, R's default string conversion for numeric is complex.
            # For the common case of 1:3 (integers in R), they are converted to "1", "2", "3".
            if v == int(v):
                return str(int(v))
            return str(v)
            
        return str(v)

    # Join elements for each index
    results = []
    for i in range(max_len):
        row_vals = [clean_val(expanded[j][i]) for j in range(len(expanded))]
        results.append(sep.join(row_vals))

    # Handle collapse
    if collapse is not None:
        return collapse.join(results)
    else:
        # Return scalar if result length is 1, otherwise numpy array
        if max_len == 1:
            return results[0]
        else:
            return np.array(results, dtype=object)
