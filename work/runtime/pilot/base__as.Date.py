import numpy as np
import pandas as pd
from datetime import datetime

def r_as_Date(x, *args, **kwargs):
    # Handle None/Null
    if x is None:
        return np.array([], dtype='datetime64[D]')

    # Flatten matrices/arrays if they contain strings or numbers
    # R's as.Date often treats matrices as vectors (flattens them)
    original_x = x
    if isinstance(x, (np.ndarray, list)):
        # If it's a multi-dimensional array, flatten it like R does for as.Date
        if isinstance(x, np.ndarray) and x.ndim > 1:
            x = x.ravel()
        elif isinstance(x, list):
            # Check if it is a list of lists (matrix)
            if len(x) > 0 and isinstance(x[0], list):
                # Flatten nested list
                x = [item for sublist in x for item in sublist]

    # Detect if input is numeric
    is_numeric = False
    if isinstance(x, (int, float, np.integer, np.floating, np.ndarray)):
        if isinstance(x, np.ndarray) and x.dtype.kind in 'bif': # boolean, integer, float
            is_numeric = True
        elif not isinstance(x, np.ndarray):
            is_numeric = True

    if is_numeric:
        origin_val = kwargs.get('origin')
        if origin_val is None:
            origin_val = "1970-01-01"
        
        try:
            if isinstance(origin_val, (int, float, np.integer, np.floating)):
                origin_date = np.datetime64('1970-01-01') + np.timedelta64(int(origin_val), 'D')
            else:
                origin_date = np.datetime64(origin_val).astype('datetime64[D]')
        except:
            origin_date = np.datetime64('1970-01-01')

        vals = np.asanyarray(x, dtype=float)
        days = vals.astype('timedelta64[D]')
        result = origin_date + days
        
        if isinstance(original_x, (int, float, np.integer, np.floating)):
            return result.item()
        return result

    # Handle strings or arrays of strings
    if isinstance(x, (str, list, np.ndarray)):
        # Check if elements are strings
        is_str_type = False
        if isinstance(x, str):
            is_str_type = True
        elif isinstance(x, (list, np.ndarray)) and len(x) > 0:
            first_elem = x[0] if isinstance(x, list) else x.flat[0]
            if isinstance(first_elem, str) or (isinstance(first_elem, np.ndarray) and first_elem.dtype.kind in 'SU'):
                is_str_type = True
        
        if is_str_type:
            fmt = kwargs.get('format', '%Y-%m-%d')
            
            if isinstance(x, str):
                try:
                    dt = datetime.strptime(x, fmt)
                    return np.datetime64(dt.date())
                except ValueError:
                    return np.datetime64('NaT')
            else:
                results = []
                for item in x:
                    if pd.isna(item) or item is None:
                        results.append(np.datetime64('NaT'))
                    else:
                        try:
                            # cast to string to handle numpy.str_ etc
                            dt = datetime.strptime(str(item), fmt)
                            results.append(np.datetime64(dt.date()))
                        except ValueError:
                            results.append(np.datetime64('NaT'))
                
                # If the original input was a 1x1 matrix or single value, 
                # R's as.Date sometimes returns a scalar/single date
                res_array = np.array(results)
                if isinstance(original_x, np.ndarray) and original_x.size == 1:
                    return res_array[0]
                return res_array

    # Handle logical/NaN cases from the provided R source snippet
    if isinstance(x, np.ndarray) and x.dtype == bool:
        if np.all(pd.isna(x)):
            return np.array([], dtype='datetime64[D]')
    
    # Final fallback to pandas for other types
    try:
        # Handle lists/arrays by converting to Series first
        res = pd.to_datetime(x, format=kwargs.get('format'))
        if isinstance(res, pd.DatetimeIndex) or isinstance(res, pd.Series):
            return res.values.astype('datetime64[D]')
        if hasattr(res, 'date'):
            return np.datetime64(res.date())
        return np.datetime64(res)
    except:
        raise TypeError(f"do not know how to convert {original_x} to class Date")
