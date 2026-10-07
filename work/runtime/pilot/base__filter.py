import numpy as np
import pandas as pd

def r_filter(x, filter, method="convolution", sides=2, circular=False, init=None):
    """
    Python implementation of R's filter function.
    """
    # Handle input conversion for x
    if isinstance(x, (list, np.ndarray)):
        x_arr = np.asarray(x, dtype=float)
    elif isinstance(x, pd.Series):
        x_arr = x.values.astype(float)
    elif isinstance(x, pd.DataFrame):
        x_arr = x.values.astype(float)
    else:
        x_arr = np.asarray(x, dtype=float)

    # Ensure x_arr is at least 1D
    if x_arr.ndim == 0:
        x_arr = x_arr.reshape(1)

    n = len(x_arr)
    if x_arr.ndim == 1:
        nser = 1
        x_mat = x_arr.reshape(n, 1)
    else:
        n, nser = x_arr.shape
        x_mat = x_arr

    # Handle filter conversion - must be treatable as a vector
    filter_arr = np.atleast_1d(np.asarray(filter, dtype=float))
    nfilt = len(filter_arr)

    if np.any(np.isnan(filter_arr)):
        raise ValueError("missing values in 'filter'")

    if method == "convolution":
        if nfilt > n:
            raise ValueError("'filter' is longer than time series")
        if sides not in (1, 2):
            raise ValueError("argument 'sides' must be 1 or 2")

        y = np.full((n, nser), np.nan)
        
        # R's filter side logic:
        # sides=1: window is [i - nfilt + 1, i]
        # sides=2: window is [i - floor(nfilt/2), i + ceiling(nfilt/2) - 1]
        # Wait, R's C_cfilter implementation for sides=2 actually uses
        # a window that centers the filter. If nfilt=3, it takes x[i-1], x[i], x[i+1].
        # If nfilt=1, it takes x[i].
        
        shift = nfilt // 2 if sides == 2 else nfilt - 1

        for j in range(nser):
            series = x_mat[:, j]
            for i in range(n):
                start = i - shift
                end = start + nfilt
                
                if circular:
                    indices = np.arange(start, end) % n
                    window = series[indices]
                    if not np.any(np.isnan(window)):
                        y[i, j] = np.dot(window, filter_arr[::-1])
                else:
                    if start >= 0 and end <= n:
                        window = series[start:end]
                        if not np.any(np.isnan(window)):
                            y[i, j] = np.dot(window, filter_arr[::-1])

    elif method == "recursive":
        if init is None:
            init_mat = np.zeros((nfilt, nser))
        else:
            init_mat = np.asarray(init, dtype=float)
            if init_mat.ndim == 1:
                if len(init_mat) != nfilt:
                    raise ValueError("length of 'init' must equal length of 'filter'")
                init_mat = init_mat.reshape(nfilt, 1)
            elif init_mat.shape[0] != nfilt:
                raise ValueError("length of 'init' must equal length of 'filter'")
            
            if init_mat.shape[1] != 1 and init_mat.shape[1] != nser:
                raise ValueError(f"'init' must have 1 or {nser} columns")
            if init_mat.shape[1] == 1:
                init_mat = np.tile(init_mat, (1, nser))

        y = np.full((n, nser), np.nan)
        for j in range(nser):
            series = x_mat[:, j]
            # R's recursive filter: y[i] = x[i] + f[1]*y[i-1] + f[2]*y[i-2] ...
            # init is passed as the values of y before the series starts.
            # R's C_rfilter takes rev(init) as the starting state.
            state = list(init_mat[:, j][::-1])
            for i in range(n):
                val = series[i]
                if np.isnan(val):
                    res = np.nan
                else:
                    res = val
                    for k in range(1, nfilt + 1):
                        prev_y = state[-k]
                        if np.isnan(prev_y):
                            res = np.nan
                            break
                        res += filter_arr[k-1] * prev_y
                y[i, j] = res
                state.append(res)

    if nser == 1:
        return y.flatten()
    else:
        return y
