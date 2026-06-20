# Translated from <R script> by r2py v0.2.0
# Model: claude-haiku-4-5  ScriptMap entities: 18

import numpy as np
import math
import statistics
import warnings

warnings.filterwarnings('ignore')

# r2py:entity:suppressPackageStartupMessages
pass

# r2py:entity:import_purrr
# purrr library import
pass

# mtcars dataset (built-in R dataset)
mtcars = {
    'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9, 21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],
    'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6, 6, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 8, 6, 8, 4],
    'disp': [160.0, 160.0, 108.0, 258.0, 360.0, 225.0, 360.0, 146.7, 140.8, 167.6, 167.6, 275.8, 275.8, 275.8, 472.0, 460.0, 440.0, 78.7, 75.7, 71.1, 120.1, 318.0, 304.0, 350.0, 400.0, 79.0, 120.3, 95.1, 351.0, 145.0, 301.0, 121.0],
    'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 123, 123, 180, 180, 180, 205, 215, 230, 66, 52, 65, 97, 150, 150, 245, 175, 66, 91, 113, 264, 175, 335, 109],
    'drat': [3.9, 3.9, 3.85, 3.08, 3.15, 2.76, 3.21, 3.69, 3.92, 3.92, 3.92, 3.07, 3.07, 3.07, 2.93, 3.0, 3.23, 4.08, 4.93, 4.22, 3.7, 2.76, 3.15, 3.73, 3.08, 4.08, 4.43, 3.77, 4.22, 3.62, 3.54, 4.11],
    'wt': [2.62, 2.875, 2.32, 3.215, 3.44, 3.46, 3.57, 3.19, 3.15, 3.44, 3.44, 4.07, 3.73, 3.78, 5.25, 5.424, 5.345, 2.2, 1.615, 1.835, 2.465, 3.52, 3.435, 3.84, 3.845, 1.935, 2.14, 1.513, 3.17, 2.77, 3.57, 2.78],
    'qsec': [16.46, 17.02, 18.61, 19.44, 17.02, 20.22, 15.84, 20.0, 22.9, 18.3, 18.9, 17.4, 17.6, 18.0, 17.98, 17.82, 17.0, 19.47, 20.01, 21.4, 18.52, 16.87, 17.3, 15.41, 17.05, 18.52, 19.44, 18.07, 16.9, 16.4, 14.6, 18.6],
    'vs': [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    'am': [1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    'gear': [4, 4, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 4],
    'carb': [4, 4, 1, 1, 2, 1, 4, 2, 2, 4, 4, 3, 3, 3, 4, 4, 4, 1, 2, 1, 1, 2, 2, 4, 2, 1, 2, 2, 4, 6, 8, 2]
}

# r2py:entity:x
x = {"x": list(range(1, 101)) + [None, 1000], "na.rm": True, "trim": 0.9}

def mean_with_trim(values, na_rm=False, trim=0.0):
    """
    Compute mean with optional NA removal and trimming.
    Trim follows R's behavior: trim fraction from each end after sorting.
    """
    # Filter NAs if requested
    if na_rm:
        vals = [v for v in values if v is not None]
    else:
        vals = list(values)
    
    if not vals:
        return float('nan')
    
    # Apply trim if specified
    if trim > 0 and trim < 0.5:
        # Sort and remove trim fraction from each end
        sorted_vals = sorted(vals)
        n = len(sorted_vals)
        # R's trim: floor(n * trim) values removed from each end
        trim_count = int(n * trim)
        if trim_count > 0:
            vals = sorted_vals[trim_count:n - trim_count]
    
    if not vals:
        return float('nan')
    
    return sum(vals) / len(vals)

def lift_dl(f, **defaults):
    """
    Lift a function to accept a dict/list and expand as arguments.
    Based on purrr::lift_dl pattern: converts list(...) to f(...)
    """
    def wrapper(data=None, **extra_kwargs):
        # Merge defaults with extra_kwargs (extra_kwargs override defaults)
        merged_kwargs = {**defaults, **extra_kwargs}
        
        if isinstance(data, dict):
            # If 'x' key exists, use it as first positional arg
            if 'x' in data:
                positional = data['x']
                # Merge other keys from data into kwargs (excluding 'x')
                for k, v in data.items():
                    if k != 'x':
                        # Convert dot notation to underscore
                        k_normalized = k.replace('.', '_')
                        merged_kwargs[k_normalized] = v
            else:
                # Use all dict items as kwargs
                positional = None
                for k, v in data.items():
                    k_normalized = k.replace('.', '_')
                    merged_kwargs[k_normalized] = v
        else:
            # Assume data is a list/tuple
            positional = data
        
        # Call function
        if positional is not None:
            return f(positional, **merged_kwargs)
        else:
            return f(**merged_kwargs)
    
    return wrapper

# r2py:entity:lift_dl(mean)
result_1 = lift_dl(mean_with_trim)(x)
print(f"[1] {result_1:.5g}")

# r2py:entity:lift(mean)
# lift is an alias for lift_dl
result_2 = lift_dl(mean_with_trim)(x)
print(f"[1] {result_2:.5g}")

# r2py:entity:exec
def exec_r(fn, *args, **kwargs):
    """
    Execute a function with splat arguments (R's exec with !!!unpacking).
    """
    return fn(*args, **kwargs)

result_3 = exec_r(mean_with_trim, x['x'], na_rm=True)
print(f"[1] {result_3:.5g}")

# r2py:entity:list
# Piped version: list(c(1:100, NA, 1000)) |> lift_dl(mean, na.rm = TRUE)()
data_list = list(range(1, 101)) + [None, 1000]
result_4 = lift_dl(mean_with_trim, na_rm=True)(data_list)
print(f"[1] {result_4:.5g}")

# r2py:entity:lift_dl(mean, na.rm = TRUE)
result_5 = lift_dl(mean_with_trim, na_rm=True)(data_list)
print(f"[1] {result_5:.5g}")

# r2py:entity:mean
result_6 = mean_with_trim(data_list, na_rm=True)
print(f"[1] {result_6:.5g}")

# r2py:entity:fun
fun = lift_dl(lambda x, **kwargs: sum([v for v in x if v is not None]))

# r2py:entity:lift_dl
fun_lifted = lift_dl(lambda x, **kwargs: sum([v for v in x if v is not None]))

# r2py:entity:fun_1
result_7 = fun([3, None, 4])
print(f"[1] {result_7}")

# r2py:entity:fun_2
def fun_def(x, **kwargs):
    # Extract numeric values, handling NA
    total = sum([v for v in x if v is not None])
    return total

# r2py:entity:exec_1
result_8 = exec_r(fun_def, [3, None, 4])
print(f"[1] {result_8}")

# r2py:entity:pmap_dbl
def pmap_dbl(data_dict, f):
    """
    Apply function to parallel elements (rows) of a dict of columns.
    Equivalent to R's pmap_dbl().
    Each row is passed as unpacked arguments to f.
    """
    if not isinstance(data_dict, dict):
        return []
    
    # Get column names and length
    keys = list(data_dict.keys())
    if not keys:
        return []
    
    n_rows = len(data_dict[keys[0]])
    results = []
    
    # For each row, collect values and apply function
    for i in range(n_rows):
        row_values = [data_dict[k][i] for k in keys]
        results.append(f(*row_values))
    
    return results

def lift_vd(f):
    """
    Lift a function to take vector/list as separate arguments.
    Equivalent to purrr::lift_vd().
    """
    def wrapper(*args):
        # Combine all args into a list and pass to f
        return f(list(args))
    return wrapper

# Apply pmap_dbl with lift_vd(mean)
result_pmap = pmap_dbl(mtcars, lift_vd(mean_with_trim))

def print_r_vector(values, width=8):
    """
    Print vector in R format with proper spacing and significant digits.
    """
    output_lines = []
    current_line = ""
    
    for i, val in enumerate(values):
        if i % width == 0:
            if current_line:
                output_lines.append(current_line)
            current_line = f"[{i+1}] "
        
        if isinstance(val, float):
            # Format with 5 significant digits like R
            formatted = f"{val:.5g}"
        else:
            formatted = str(val)
        
        current_line += formatted + " "
    
    if current_line:
        output_lines.append(current_line.rstrip())
    
    for line in output_lines:
        print(line)

print_r_vector(result_pmap)

# r2py:entity:pmap_dbl_1
result_pmap_1 = pmap_dbl(mtcars, lambda *row: mean_with_trim(list(row)))
print_r_vector(result_pmap_1)

# r2py:entity:pmap_lgl
def pmap_lgl(data_dict, f):
    """
    Apply function to parallel elements returning logical (boolean) vector.
    Equivalent to R's pmap_lgl().
    Each row is passed as unpacked arguments to f.
    """
    if not isinstance(data_dict, dict):
        return []
    
    keys = list(data_dict.keys())
    if not keys:
        return []
    
    n_rows = len(data_dict[keys[0]])
    results = []
    
    for i in range(n_rows):
        row_values = [data_dict[k][i] for k in keys]
        results.append(bool(f(*row_values)))
    
    return results

def lift_ld(f, *args):
    """
    Lift a function to take list/vector as first arg instead of ...
    Equivalent to purrr::lift_ld().
    """
    def wrapper(*inner_args):
        # Call f with list as first argument, then any extra args
        return f(list(inner_args), *args)
    return wrapper

def partial(f, *partial_args, **partial_kwargs):
    """
    Partially apply arguments to a function.
    """
    def wrapper(*args, **kwargs):
        return f(*partial_args, *args, **partial_kwargs, **kwargs)
    return wrapper

def some(x, predicate):
    """
    Check if any element in x satisfies the predicate.
    Equivalent to purrr::some().
    """
    for item in x:
        try:
            if predicate(item):
                return True
        except (TypeError, ValueError):
            pass
    return False

# Main pmap_lgl call
result_pmap_lgl = pmap_lgl(mtcars, lift_ld(some, partial(lambda x, y: x < y, 200)))

def print_r_logical_vector(values, width=12):
    """
    Print logical vector in R format with proper spacing.
    """
    output_lines = []
    current_line = ""
    
    for i, val in enumerate(values):
        if i % width == 0:
            if current_line:
                output_lines.append(current_line)
            current_line = f"[{i+1}] "
        
        current_line += ("TRUE" if val else "FALSE") + " "
    
    if current_line:
        output_lines.append(current_line.rstrip())
    
    for line in output_lines:
        print(line)

print_r_logical_vector(result_pmap_lgl)

# r2py:entity:pmap_lgl_1
# Alternative: using lambda instead of lift_ld
result_pmap_lgl_1 = pmap_lgl(mtcars, lambda *row: any(c > 200 for c in row))
print_r_logical_vector(result_pmap_lgl_1)
