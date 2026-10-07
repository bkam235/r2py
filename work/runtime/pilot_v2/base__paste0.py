import numpy as np
import pandas as pd

def r_paste0(*args, collapse=None, recycle0=False, **kwargs):
    # Combine positional and keyword arguments into one sequence
    items = list(args)
    if kwargs:
        items.extend(kwargs.values())
    
    if not items:
        return [""]

    processed = []
    max_len = 1
    for item in items:
        if isinstance(item, (list, np.ndarray, pd.Series)):
            item_strs = []
            for val in item:
                if pd.isna(val):
                    item_strs.append("NA")
                # R converts numeric to string without .0 if it's a whole number
                elif isinstance(val, (float, np.floating)) and float(val).is_integer():
                    item_strs.append(str(int(val)))
                else:
                    item_strs.append(str(val))
            processed.append(np.array(item_strs))
            max_len = max(max_len, len(item_strs))
        else:
            # Scalar handling
            if pd.isna(item):
                val_str = "NA"
            elif isinstance(item, (float, np.floating)) and float(item).is_integer():
                val_str = str(int(item))
            else:
                val_str = str(item)
            processed.append(val_str)

    results = []
    for i in range(max_len):
        current_str = ""
        for item in processed:
            if isinstance(item, np.ndarray):
                # R recycles vectors to match the longest one
                current_str += item[i % len(item)]
            else:
                current_str += item
        results.append(current_str)

    if collapse is not None:
        # R's collapse returns a single string (scalar)
        return collapse.join(results)
    else:
        # Return as a character vector (list of strings)
        # If max_len was 1 and we only have one element, it's still a vector in R
        return results
