import numpy as np
import pandas as pd

def r_as_hms(x, *args, **kwargs):
    """
    Reproduces hms::as_hms in R.
    Converts inputs to hms format (HH:MM:SS[.s]).
    """
    # Track if input was scalar to return scalar
    is_scalar = False
    if isinstance(x, (str, int, float, np.number)):
        is_scalar = True
        x_list = [x]
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        x_list = x
    else:
        # Handle other iterables like seq outputs
        x_list = list(x)

    # Convert to numpy array for easier handling of NAs
    arr = np.array(x_list, dtype=object)
    
    # Check if the array contains numeric types (excluding strings)
    is_numeric = False
    if arr.size > 0:
        non_nas = [v for v in arr if not pd.isna(v)]
        if len(non_nas) > 0 and all(isinstance(v, (int, float, np.number)) for v in non_nas):
            is_numeric = True
        elif len(non_nas) == 0:
            is_numeric = True

    results = []
    if is_numeric:
        for val in arr:
            if pd.isna(val):
                results.append(None)
            else:
                total_seconds = float(val)
                sign = "-" if total_seconds < 0 else ""
                a = abs(total_seconds)
                
                h = int(a // 3600)
                m = int((a % 3600) // 60)
                s = a % 60
                
                # R's hms formatting for numeric:
                # If s is an integer, it is formatted as %02d.
                # If s has a fractional part, it is formatted as %06.1f 
                # BUT the '06' in printf includes the decimal point and the 2 digits before it.
                # The failing case "03:38:0058.9" suggests a mistake in my previous f-string.
                # %06.1f for 58.9 is "058.9". 
                # Actually, the correct R hms behavior for the seconds part is:
                # if s is integer: {:02d}
                # if s is float: {:04.1f} (e.g., 58.9 -> "58.9", 8.9 -> "08.9")
                
                if s % 1 == 0:
                    s_str = f"{int(s):02d}"
                else:
                    # Format to 1 decimal place, ensure at least 2 digits before decimal
                    # 8.9 -> "08.9", 58.9 -> "58.9"
                    s_str = f"{s:04.1f}"
                
                results.append(f"{sign}{h:02d}:{m:02d}:{s_str}")
    else:
        # String handling
        for val in arr:
            if pd.isna(val):
                results.append(None)
            else:
                results.append(str(val))

    if is_scalar:
        return results[0]
    
    return results
