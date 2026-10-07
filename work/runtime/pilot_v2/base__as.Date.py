import numpy as np
import pandas as pd
from datetime import datetime, date
import builtins

def r_as_Date(x, format=None, tryFormats=None, optional=False, *args, **kwargs):
    if tryFormats is None:
        tryFormats = ["%Y-%m-%d", "%Y/%m/%d"]
    
    # Handle input types to ensure we work with arrays/lists
    if isinstance(x, (str, int, float)):
        x_arr = np.array([x], dtype=object)
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        x_arr = np.array(x, dtype=object)
    else:
        # For other types, let pandas attempt conversion or treat as object
        x_arr = np.array([x], dtype=object)

    def strptime_r(vals, fmt):
        """Helper to mimic R's strptime returning NaT/NaN for failures."""
        results = []
        for v in vals:
            if pd.isna(v) or (isinstance(v, str) and not v.strip()):
                results.append(pd.NaT)
            else:
                try:
                    # R's strptime is based on C strptime; pandas to_datetime is close
                    # We use %z=GMT logic implicitly by not specifying TZ unless needed
                    dt = pd.to_datetime(v, format=fmt, errors='coerce')
                    results.append(dt)
                except:
                    results.append(pd.NaT)
        return pd.DatetimeIndex(results)

    if format is not None:
        # Use the specified format
        res_dt = strptime_r(x_arr, format)
    else:
        # charToDate logic
        # Normalize inputs: empty strings are NA
        normalized_x = []
        for val in x_arr:
            if isinstance(val, str) and not val:
                normalized_x.append(np.nan)
            else:
                normalized_x.append(val)
        
        # Find the first non-NA value to determine the format
        xx = None
        for val in normalized_x:
            if not pd.isna(val):
                xx = val
                break
        
        if xx is None:
            # All are NA, default to %Y-%m-%d (though it won't matter)
            res_dt = strptime_r(normalized_x, "%Y-%m-%d")
        else:
            # Try the provided tryFormats
            found_fmt = None
            for ff in tryFormats:
                # Test only the first non-NA value
                test_dt = strptime_r([xx], ff)
                if not pd.isna(test_dt[0]):
                    found_fmt = ff
                    break
            
            if found_fmt:
                res_dt = strptime_r(normalized_x, found_fmt)
            elif optional:
                # Return array of NAs
                res_dt = pd.DatetimeIndex([pd.NaT] * len(normalized_x))
            else:
                raise ValueError("character string is not in a standard unambiguous format")

    # Convert DatetimeIndex to a numpy array of datetime.date (R's Date class)
    # R's as.Date converts the result of strptime (POSIXct) to Date.
    final_dates = []
    for dt in res_dt:
        if pd.isna(dt):
            final_dates.append(np.nan)
        else:
            final_dates.append(dt.date())
    
    result = np.array(final_dates, dtype=object)
    
    # Return scalar if input was scalar
    if isinstance(x, (str, int, float)) and not isinstance(x, (list, np.ndarray, pd.Series)):
        return result[0]
    
    return result
