import numpy as np
import pandas as pd

def r_mean(x, trim=0, na_rm=False, *args, **kwargs):
    # Handle input type conversion to numpy array
    if isinstance(x, (list, tuple)):
        x = np.array(x)
    elif isinstance(x, pd.Series):
        x = x.to_numpy()
    elif isinstance(x, (int, float, np.float64, np.int64)):
        x = np.array([x])
    
    # R: if (!is.numeric(x) && !is.complex(x) && !is.logical(x))
    # In Python context, we check if the dtype is numeric or boolean
    if not (np.issubdtype(x.dtype, np.number) or np.issubdtype(x.dtype, np.bool_)):
        # R returns NA_real_
        return np.nan

    # Handle na.rm
    if na_rm:
        # x <- x[!is.na(x)]
        x = x[~np.isnan(x) if np.issubdtype(x.dtype, np.number) else x]
    
    # Validate trim
    if not isinstance(trim, (int, float, np.number)) or np.ndim(trim) != 0:
        raise ValueError("'trim' must be numeric of length one")

    n = len(x)
    if n == 0:
        return np.nan

    if trim > 0:
        # Trimmed means are not defined for complex data (handled by dtype check above for this impl)
        # if (anyNA(x)) return(NA_real_)
        if np.any(np.isnan(x)):
            return np.nan
        
        if trim >= 0.5:
            # return(stats::median(x, na.rm = FALSE))
            # np.median handles the logic; R's median handles NA by returning NA if na.rm=FALSE
            return np.median(x)
        
        # lo <- floor(n * trim) + 1
        # hi <- n + 1 - lo
        # x <- sort.int(x, partial = unique(c(lo, hi)))[lo:hi]
        lo = int(np.floor(n * trim))
        # R is 1-indexed, [lo+1:hi] in R is [lo:hi] in 0-indexed Python slicing
        # lo_r = floor(n*trim)+1. hi_r = n + 1 - lo_r. 
        # Slicing [lo_r : hi_r] in R means indices from lo_r to hi_r inclusive.
        # In 0-index: index (lo_r - 1) to (hi_r - 1).
        # lo_idx = floor(n*trim).
        # hi_idx = (n + 1 - (floor(n*trim)+1)) - 1 = n - floor(n*trim) - 1.
        # Python slice [lo_idx : hi_idx + 1]
        hi = n - lo
        
        sorted_x = np.sort(x)
        x = sorted_x[lo:hi]

    # .Internal(mean(x))
    # If x is empty after trim or contains NaN and na.rm was False, 
    # np.mean returns NaN which matches R's behavior.
    result = np.mean(x)
    
    # Return as a scalar if it's a single value, matching R's behavior for mean()
    return float(result) if isinstance(result, (np.float64, np.float32)) else result
