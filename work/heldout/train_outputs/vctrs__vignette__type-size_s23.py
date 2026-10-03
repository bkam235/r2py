# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import numpy as np
import pandas as pd

# r2py:entity:allow_lossy_cast
def vec_ptype(x):
    """Returns a representation of the type of x."""
    if isinstance(x, (int, np.integer)):
        return np.dtype('int64')
    if isinstance(x, (float, np.floating)):
        return np.dtype('float64')
    if isinstance(x, (list, np.ndarray, pd.Series)):
        if len(x) == 0:
            return np.dtype('float64') # Default vctrs behavior
        return np.array(x).dtype
    return np.dtype('object')

def vec_is(x, ptype=None, size=None):
    """Checks if x matches the given ptype and size."""
    if ptype is not None:
        x_type = vec_ptype(x)
        if x_type != ptype:
            return False
    if size is not None:
        x_size = len(x) if hasattr(x, '__len__') else 1
        if x_size != size:
            return False
    return True

class CastLossyError(Exception):
    """Custom exception to simulate vctrs_error_cast_lossy."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super().__init__(f"Lossy cast from {vec_ptype(x)} to {vec_ptype(y)}")

def vec_cast(x, to):
    """
    Simulates vctrs::vec_cast. 
    In vctrs, casting float to int is lossy if decimals exist.
    """
    x_arr = np.asanyarray(x)
    to_type = vec_ptype(to)
    
    # Logic for lossy cast: if casting float to int and values are not whole numbers
    if np.issubdtype(x_arr.dtype, np.floating) and np.issubdtype(to_type, np.integer):
        if not np.all(np.mod(x_arr, 1) == 0):
            raise CastLossyError(x, to)
            
    return x_arr.astype(to_type)

def allow_lossy_cast(expr_func, x_ptype=None, to_ptype=None):
    """
    Executes expr_func and suppresses CastLossyError if types match x_ptype and to_ptype.
    Since Python doesn't have R's 'withCallingHandlers', we use try-except.
    """
    try:
        return expr_func()
    except CastLossyError as err:
        # We simulate the logic: if types match the provided constraints, we "restart" 
        # which in this context means we perform the cast anyway (lossy).
        if x_ptype is not None and not vec_is(err.x, x_ptype):
            raise err
        if to_ptype is not None and not vec_is(err.y, to_ptype):
            raise err
        
        # "invokeRestart" for lossy cast simply means doing the cast regardless of loss
        return np.asanyarray(err.x).astype(vec_ptype(err.y))

# Main execution
# R: vec_cast(c(1.5, 2), integer())
# In Python, we wrap the call in a lambda to pass it as an expression to allow_lossy_cast
# r2py:entity:allow_lossy_cast
result = allow_lossy_cast(
    lambda: vec_cast([1.5, 2], np.array([0], dtype='int64')),
    x_ptype=np.dtype('float64'),
    to_ptype=np.dtype('int64')
)

print(result)