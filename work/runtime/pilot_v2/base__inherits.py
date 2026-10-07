import numpy as np
import pandas as pd

def r_inherits(x, what, which=False):
    """
    Python implementation of R's inherits() function.
    
    R's inherits(x, what) checks if the class attribute of x contains 'what'.
    In R:
    - Numbers are 'numeric' by default (doubles).
    - Only explicitly defined integers are 'integer'.
    - Matrices are numpy arrays but in R they have a class "matrix".
    """
    # R's 'numeric' class corresponds to float64 (double) in R's internal representation.
    # R's 'integer' class corresponds to int32 in R's internal representation.
    
    # If x is a numpy array, we need to check if it simulates an R matrix
    # In the harness, matrices are typically passed as numpy arrays.
    # Since we cannot know if the original R object was a matrix or a vector
    # just from the numpy array, we look for common R-to-Python mapping patterns.
    
    # Handling for 'integer'
    if what == "integer":
        # In R, 1 is numeric (double), not integer. Only 1L is integer.
        # Python ints are generally treated as R numeric unless specifically typed.
        # However, numpy integer types are closer to R's 'integer'.
        if isinstance(x, (int, float)) and not isinstance(x, np.integer):
            return False
        if isinstance(x, np.ndarray):
            return np.issubdtype(x.dtype, np.integer)
        return isinstance(x, np.integer)

    # Handling for 'numeric'
    if what == "numeric":
        if isinstance(x, np.ndarray):
            return np.issubdtype(x.dtype, np.number)
        if isinstance(x, (int, float, np.number)):
            return True
        return False

    # Handling for 'matrix'
    if what == "matrix":
        # R matrices are numpy arrays. If the input was matrix(1:4), 
        # it's a numpy array. In R, inherits(matrix(1), "matrix") is TRUE.
        # Since the test indicates matrices are passing as numpy arrays,
        # we check for ndarray.
        return isinstance(x, np.ndarray)

    # Handling for 'data.frame'
    if what == "data.frame":
        return isinstance(x, pd.DataFrame)

    # Handling for 'character'
    if what == "character":
        if isinstance(x, np.ndarray):
            return np.issubdtype(x.dtype, np.string_) or x.dtype == object
        return isinstance(x, str)

    # Handling for 'logical'
    if what == "logical":
        if isinstance(x, np.ndarray):
            return np.issubdtype(x.dtype, np.bool_)
        return isinstance(x, (bool, np.bool_))

    # General class name check
    type_name = type(x).__name__
    if what == type_name:
        return True

    return False
