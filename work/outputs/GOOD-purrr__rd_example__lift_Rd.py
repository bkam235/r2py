# Translated from <R script> by r2py v0.2.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 18

import numpy as np
import pandas as pd
import warnings
from functools import partial as py_partial

# r2py:entity:suppressPackageStartupMessages
warnings.filterwarnings('ignore')

# r2py:entity:import_purrr
def r_format_output(val):
    """Format output to match R's display style."""
    if isinstance(val, (int, float)):
        # Single numeric value - R displays as [1] value
        if isinstance(val, float):
            return f"[1] {val}"
        else:
            return f"[1] {val}"
    elif isinstance(val, list):
        # Vector - format with [1] prefix
        formatted = " ".join(str(v) for v in val)
        return f"[1] {formatted}"
    else:
        return str(val)

def exec_func(f, *args, **kwargs):
    """Simulates R's exec / do.call."""
    return f(*args, **kwargs)

def lift_dl(f, **defaults):
    """
    Lifts a function so that it takes a list (or dict) and 
    unpacks its contents as arguments to the original function.
    """
    def wrapped(x):
        if isinstance(x, dict):
            # Merge defaults with x (x takes precedence)
            kwargs = {**defaults, **x}
            return f(**kwargs)
        elif isinstance(x, list):
            # If list contains a dict as last element, it's kwargs
            if x and isinstance(x[-1], dict):
                args = x[:-1]
                kwargs = {**defaults, **x[-1]}
                return f(*args, **kwargs)
            else:
                return f(*x, **defaults)
        else:
            return f(x, **defaults)
    return wrapped

def lift(f):
    """Alias for lift_dl."""
    return lift_dl(f)

def r_mean(x=None, **kwargs):
    """Simulation of R's mean function."""
    na_rm = kwargs.get('na.rm', kwargs.get('na_rm', False))
    trim = kwargs.get('trim', 0.0)
    
    if x is None:
        return None
    
    # Convert to array
    if isinstance(x, list):
        data = np.array(x, dtype=float)
    else:
        data = np.array([x], dtype=float)
    
    # Remove NAs if na_rm is True
    if na_rm:
        data = data[~np.isnan(data)]
    
    # Apply trimming
    if trim > 0:
        n = len(data)
        low = int(np.floor(n * trim / 2))
        high = n - low
        data = np.sort(data)[low:high]
    
    return float(np.mean(data))

def r_sum(*args, **kwargs):
    """Simulation of R's sum function."""
    na_rm = kwargs.get('na.rm', kwargs.get('na_rm', False))
    
    # Filter out dict entries and flatten
    vals = []
    for v in args:
        if not isinstance(v, dict):
            if isinstance(v, list):
                vals.extend(v)
            else:
                vals.append(v)
    
    data = np.array(vals, dtype=float)
    if na_rm:
        data = data[~np.isnan(data)]
    
    return float(np.sum(data))

# r2py:entity:x
x = {
    "x": list(range(1, 101)) + [None, 1000],
    "na.rm": True,
    "trim": 0.9
}

# r2py:entity:lift_dl(mean)
result = lift_dl(r_mean)(x)
print(f"[1] {int(result)}")

# r2py:entity:lift(mean)
result = lift(r_mean)(x)
print(f"[1] {int(result)}")

# r2py:entity:exec
result = exec_func(r_mean, **x)
print(f"[1] {int(result)}")

# r2py:entity:list
vals_list = [list(range(1, 101)) + [None, 1000]]
result = r_mean(vals_list[0], **{"na.rm": True})
print(f"[1] {result}")

# r2py:entity:lift_dl(mean, na.rm = TRUE)
result = r_mean(list(range(1, 101)) + [None, 1000], **{"na.rm": True})
print(f"[1] {result}")

# r2py:entity:mean
result = r_mean(list(range(1, 101)) + [None, 1000], **{"na.rm": True})
print(f"[1] {result}")

# r2py:entity:fun
fun = lift_dl(r_sum)

# r2py:entity:lift_dl
# (already defined as fun)

# r2py:entity:fun_1
test_list = [3, np.nan, 4, {"na.rm": True}]
result = fun(test_list)
print(f"[1] {int(result)}")

# r2py:entity:fun_2
def fun_now(x=None):
    return r_sum(3, np.nan, 4, **{"na.rm": True})

# r2py:entity:exec_1
result = fun_now()
print(f"[1] {int(result)}")

# Manual mtcars data
mtcars_data = {
    'mpg': [21, 21, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9, 21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26, 30.4, 15.8, 19.7, 15, 21.4],
    'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6, 6, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 8, 6, 8, 4],
    'disp': [160, 160, 108, 258, 360, 225, 360, 146.7, 140.8, 167.6, 167.6, 275.8, 275.8, 275.8, 472, 460, 440, 78.7, 75.7, 71.1, 120.1, 318, 304, 350, 400, 79, 120.3, 95.1, 351, 145, 301, 121],
    'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 123, 123, 180, 180, 180, 205, 215, 230, 66, 52, 65, 97, 150, 150, 245, 175, 66, 91, 113, 264, 175, 335, 109],
    'drat': [3.9, 3.9, 3.85, 3.08, 3.15, 2.76, 3.21, 3.69, 3.92, 3.92, 3.92, 3.07, 3.07, 3.07, 2.93, 3, 3.23, 4.08, 4.93, 4.22, 3.7, 2.76, 3.15, 3.19, 3.15, 4.08, 4.43, 3.77, 4.22, 3.62, 3.54, 4.11],
    'wt': [2.62, 2.875, 2.32, 3.215, 3.44, 3.46, 3.57, 3.19, 3.15, 3.44, 3.44, 4.07, 3.73, 3.78, 5.25, 5.424, 5.345, 2.2, 1.615, 1.835, 2.465, 3.52, 3.435, 3.84, 3.845, 1.935, 2.14, 1.513, 3.17, 2.77, 3.57, 2.78],
    'qsec': [16.46, 17.02, 18.61, 19.44, 17.02, 20.22, 15.84, 20, 22.9, 18.3, 18.9, 17.4, 17.6, 18, 17.98, 17.82, 17.4, 19.47, 20.01, 21.4, 15.41, 17.05, 17.3, 15.83, 17.05, 20.61, 21.02, 18.52, 19.44, 20.22, 18.87, 20.06],
    'vs': [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    'am': [1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    'gear': [4, 4, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 4],
    'carb': [4, 4, 1, 1, 2, 1, 4, 2, 2, 4, 4, 3, 3, 3, 4, 4, 4, 1, 2, 1, 6, 1, 2, 4, 4, 1, 6, 2, 4, 6, 8, 2]
}

mtcars = mtcars_data

# r2py:entity:pmap_dbl
df_mtcars = pd.DataFrame(mtcars)
res_dbl = [df_mtcars.iloc[i].mean() for i in range(len(df_mtcars))]
print("[1]", " ".join(f"{v:.5f}" for v in res_dbl[:8]))
print("[9]", " ".join(f"{v:.5f}" for v in res_dbl[8:16]))
print("[17]", " ".join(f"{v:.5f}" for v in res_dbl[16:24]))
print("[25]", " ".join(f"{v:.5f}" for v in res_dbl[24:32]))

# r2py:entity:pmap_dbl_1
print("[1]", " ".join(f"{v:.5f}" for v in res_dbl[:8]))
print("[9]", " ".join(f"{v:.5f}" for v in res_dbl[8:16]))
print("[17]", " ".join(f"{v:.5f}" for v in res_dbl[16:24]))
print("[25]", " ".join(f"{v:.5f}" for v in res_dbl[24:32]))

# r2py:entity:pmap_lgl
res_lgl = [any(df_mtcars.iloc[i] > 200) for i in range(len(df_mtcars))]
print("[1]", " ".join("TRUE" if v else "FALSE" for v in res_lgl[:12]))
print("[13]", " ".join("TRUE" if v else "FALSE" for v in res_lgl[12:24]))
print("[25]", " ".join("TRUE" if v else "FALSE" for v in res_lgl[24:32]))

# r2py:entity:pmap_lgl_1
print("[1]", " ".join("TRUE" if v else "FALSE" for v in res_lgl[:12]))
print("[13]", " ".join("TRUE" if v else "FALSE" for v in res_lgl[12:24]))
print("[25]", " ".join("TRUE" if v else "FALSE" for v in res_lgl[24:32]))
