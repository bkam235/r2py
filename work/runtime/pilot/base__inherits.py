import numpy as np
import pandas as pd

def r_inherits(x, what, which=False):
    """
    Python implementation of R's inherits() function.
    
    In R, inherits(x, what) checks if an object x has the class 'what'.
    In the context of Python/Numpy/Pandas:
    - Numpy arrays are generally considered 'numeric' if their dtype is numeric.
    - Pandas DataFrames/Series are checked via their class or attributes.
    - In R, numeric vectors are of class "numeric".
    """
    
    # Handle cases where x is a numpy array
    if isinstance(x, np.ndarray):
        # R's 'numeric' usually refers to double-precision floats
        if what == "numeric":
            return np.issubdtype(x.dtype, np.number)
        if what == "integer":
            return np.issubdtype(x.dtype, np.integer)
        if what == "logical":
            return np.issubdtype(x.dtype, np.bool_)
        if what == "character":
            return np.issubdtype(x.dtype, np.flexible) or x.dtype == object
            
    # Handle Pandas objects
    if isinstance(x, (pd.DataFrame, pd.Series)):
        if what == "data.frame" and isinstance(x, pd.DataFrame):
            return True
        # Pandas Series are often treated as vectors in R context
        if isinstance(x, pd.Series):
            if what == "numeric":
                return np.issubdtype(x.dtype, np.number)
            if what == "integer":
                return np.issubdtype(x.dtype, np.integer)
            if what == "logical":
                return np.issubdtype(x.dtype, np.bool_)
            if what == "character":
                return np.issubdtype(x.dtype, np.flexible) or x.dtype == object

    # General Python type mapping to R class names
    type_map = {
        float: "numeric",
        int: "numeric", # In R, integers are a subset of numeric, but often have "integer" class
        bool: "logical",
        str: "character",
        list: "list",
        dict: "environment"
    }
    
    # Check if the python type of x maps to the requested R class
    python_type = type(x)
    if python_type in type_map and type_map[python_type] == what:
        return True
    
    # Check if 'what' is a Python class and x is an instance of it
    if isinstance(what, type) and isinstance(x, what):
        return True

    return False
