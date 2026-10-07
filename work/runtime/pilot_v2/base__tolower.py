import numpy as np
import pandas as pd

def r_tolower(x):
    """
    Python implementation of R's tolower function.
    Converts characters to lowercase.
    """
    # If x is not character-like (e.g., numeric, logical), 
    # R's as.character(x) conversion is simulated.
    # In R, tolower handles vectors.
    
    if isinstance(x, (list, np.ndarray, pd.Series)):
        # Convert elements to string, then to lowercase
        # Handle NaN as NA (which remains NaN or becomes 'nan' depending on implementation)
        # R's as.character(NA) is "NA" (character), but in the context of 
        # tolower, NA character vectors are preserved as NA.
        res = []
        for item in x:
            if pd.isna(item):
                res.append(np.nan)
            else:
                res.append(str(item).lower())
        return np.array(res, dtype=object)
    
    elif pd.isna(x):
        return np.nan
    
    else:
        # Single value case
        return str(x).lower()
