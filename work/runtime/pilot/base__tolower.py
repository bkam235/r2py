import numpy as np
import pandas as pd

def r_tolower(x):
    """
    Reproduce R's tolower function.
    R's tolower converts all characters in a character vector to lowercase.
    If x is not character, it is coerced to character.
    """
    # R's is.character check and as.character coercion
    # In Python, if x is a scalar string, we handle it. 
    # If it's a list/numpy array/pandas Series, we process each element.
    
    if isinstance(x, (np.ndarray, pd.Series, list)):
        # Convert elements to string, handling NaN (which remains NaN in R's tolower)
        # R's as.character(NA) is "NA", but tolower(NA) returns NA.
        # However, standard numpy/pandas NaN behavior for character vectors is handled here.
        res = []
        for item in x:
            if pd.isna(item):
                res.append(np.nan)
            else:
                res.append(str(item).lower())
        
        # Return as numpy array to match R vector output type for lists/arrays
        return np.array(res, dtype=object)
    
    elif pd.isna(x):
        return np.nan
    
    else:
        # Scalar case
        return str(x).lower()
