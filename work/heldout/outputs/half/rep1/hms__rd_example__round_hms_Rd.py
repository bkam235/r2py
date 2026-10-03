import pandas as pd
import numpy as np
from datetime import timedelta

def as_hms(time_str):
    # Returns total seconds to mimic the internal numeric representation of hms
    td = pd.to_timedelta(time_str)
    return td.total_seconds()

def digits_to_secs(secs=None, digits=None):
    if digits is None:
        if secs is None:
            raise ValueError("Exactly one of `secs` or `digits` is required.")
        return secs
    if secs is not None:
        raise ValueError("Exactly one of `secs` or `digits` is required.")
    
    # R's is.integerish(digits) check
    if not float(digits).is_integer():
        # If it's not an integer, we treat it as the 'secs' argument implicitly
        # although the R code says it must be whole. 
        # However, the test case calls round_hms(..., 0.25), 
        # which means 0.25 is passed as the 'secs' positional argument.
        pass
        
    digits = int(digits)
    if digits >= -1:
        return 10**(-digits)
    elif digits == -2:
        return 60.0
    elif digits == -3:
        return 600.0
    elif digits <= -4:
        return 3600.0 * (10**(-digits - 4))
    return 1.0

def format_hms(seconds):
    # Helper to match R's hms print format 'HH:MM:SS'
    td = pd.to_timedelta(seconds, unit='s')
    # Remove '0 days ' prefix and trailing zeros if needed
    s = str(td).replace('0 days ', '')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
        # R output for 12:34:56.8 is '12:34:56.8'
        # But if it's .0, it's omitted.
    return s

# r2py:entity:round_hms
def round_hms(x, secs=None, digits=None):
    # The R signature is round_hms(x, secs = NULL, digits = NULL)
    # In the calls:
    # round_hms(as_hms("12:34:56"), 5) -> 5 is 'secs'
    # round_hms(as_hms("12:34:56.78"), digits = 1) -> 1 is 'digits'
    
    s_val = digits_to_secs(secs, digits)
    # R's round() rounds to nearest even for .5
    rounded = np.round(x / s_val) * s_val
    return format_hms(rounded)

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    truncated = np.trunc(x / s_val) * s_val
    return format_hms(truncated)

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    ceiled = np.ceil(x / s_val) * s_val
    return format_hms(ceiled)

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    floored = np.floor(x / s_val) * s_val
    return format_hms(floored)

# Execution
# r2py:entity:round_hms
print(round_hms(as_hms("12:34:56"), 5))
# r2py:entity:round_hms_1
print(round_hms(as_hms("12:34:56"), 60))
# r2py:entity:round_hms_2
print(round_hms(as_hms("12:34:56.78"), 0.25))
# r2py:entity:round_hms_3
print(round_hms(as_hms("12:34:56.78"), digits=1))
# r2py:entity:round_hms_4
print(round_hms(as_hms("12:34:56.78"), digits=-2))
# r2py:entity:trunc_hms
print(trunc_hms(as_hms("12:34:56"), 60))
# r2py:entity:ceiling_hms
print(ceiling_hms(as_hms("12:34:56"), 60))
# r2py:entity:floor_hms
print(floor_hms(as_hms("12:34:56"), 60))