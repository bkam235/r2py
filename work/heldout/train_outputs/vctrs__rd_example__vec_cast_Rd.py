import pandas as pd
import numpy as np

def vec_ptype(x):
    """Returns a representation of the type of x."""
    if isinstance(x, (int, np.integer)):
        return np.dtype('int64')
    if isinstance(x, (float, np.floating)):
        return np.dtype('float64')
    if isinstance(x, (list, np.ndarray, pd.Series)):
        if len(x) == 0:
            return np.dtype('float64')
        return np.array(x).dtype
    if isinstance(x, pd.Categorical):
        return 'category'
    if isinstance(x, str):
        return np.dtype('O')
    return np.dtype('object')

class CastLossyError(Exception):
    """Custom exception to simulate vctrs_error_cast_lossy."""
    def __init__(self, x, to, result):
        self.x = x
        self.y = to
        self.result = result
        super().__init__(f"Lossy cast from {vec_ptype(x)} to {vec_ptype(to)}")

# r2py:entity:vec_cast
def vec_cast_with_result(x, to):
    x_arr = np.asanyarray(x)
    to_type = vec_ptype(to)
    
    if to_type == 'category':
        # In R, vec_cast(1.5, factor("a")) generates an error because no sensible coercion is possible
        raise TypeError("Cannot cast to factor")
        
    # Calculate the result regardless of loss
    res = x_arr.astype(to_type)
    
    # Check for lossy cast from float to int
    if np.issubdtype(x_arr.dtype, np.floating) and np.issubdtype(to_type, np.integer):
        if not np.all(np.mod(x_arr, 1) == 0):
            raise CastLossyError(x, to, res)
    
    # Check for lossy cast from int to bool
    if np.issubdtype(x_arr.dtype, np.integer) and to_type == np.bool_:
        if not np.all((x_arr == 0) | (x_arr == 1)):
            raise CastLossyError(x, to, res)
            
    return res

# r2py:entity:allow_lossy_cast
def allow_lossy_cast_exec(func, to_ptype=None):
    try:
        return func()
    except CastLossyError as e:
        # Check if to_ptype matches the target ptype
        if to_ptype is not None:
            target_type = vec_ptype(to_ptype)
            if target_type != vec_ptype(e.y):
                raise e
        return e.result

# r2py:entity:vec_cast_common
def vec_cast_common(*args):
    # Common type for factors is a factor with the union of all levels
    all_vals = []
    for arg in args:
        all_vals.extend(list(arg))
    
    common_levels = sorted(list(set(all_vals)))
    
    results = []
    for arg in args:
        # Create categorical with union of levels
        s = pd.Series(arg, dtype='category').astype(pd.CategoricalDtype(categories=common_levels))
        results.append(s)
    return results

# --- Execution ---

# vec_cast(1, integer())
# r2py:entity:vec_cast
res_1 = vec_cast_with_result([1], np.int32)
print(f"[1] {res_1[0]}")

# try(vec_cast(c(1, 1.5), integer()))
# r2py:entity:try
try:
    vec_cast_with_result([1, 1.5], np.int32)
except Exception:
    pass

# try(vec_cast(c(1, 2), logical()))
# r2py:entity:try_1
try:
    vec_cast_with_result([1, 2], np.bool_)
except Exception:
    pass

# allow_lossy_cast(vec_cast(c(1, 1.5), integer()))
# r2py:entity:allow_lossy_cast
res_alc1 = allow_lossy_cast_exec(lambda: vec_cast_with_result([1, 1.5], np.int32))
print(f"[1] {' '.join(map(str, res_alc1.astype(int)))}")

# allow_lossy_cast(vec_cast(c(1, 2), logical()))
# r2py:entity:allow_lossy_cast_1
res_alc2 = allow_lossy_cast_exec(lambda: vec_cast_with_result([1, 2], np.bool_))
print(f"[1] {' '.join(map(str, res_alc2)).upper().replace('TRUE', 'TRUE').replace('FALSE', 'FALSE')}")

# allow_lossy_cast(vec_cast(c(1, 1.5), integer()), to_ptype = integer())
# r2py:entity:allow_lossy_cast_2
res_alc3 = allow_lossy_cast_exec(lambda: vec_cast_with_result([1, 1.5], np.int32), to_ptype=np.int32)
print(f"[1] {' '.join(map(str, res_alc3.astype(int)))}")

# try(allow_lossy_cast(vec_cast(c(1, 2), logical()), to_ptype = integer()))
# r2py:entity:try_2
try:
    allow_lossy_cast_exec(lambda: vec_cast_with_result([1, 2], np.bool_), to_ptype=np.int32)
except Exception:
    pass

# try(vec_cast(1.5, factor("a")))
# r2py:entity:try_3
try:
    vec_cast_with_result([1.5], 'category')
except Exception:
    pass

# vec_cast_common(factor("a"), factor(c("a", "b")))
# r2py:entity:vec_cast_common
common = vec_cast_common(["a"], ["a", "b"])
for i, s in enumerate(common, 1):
    print(f"[[{i}]]")
    print(f"[1] {' '.join(map(str, s.values))}")
    print(f"Levels: {' '.join(map(str, s.cat.categories))}")
    print()