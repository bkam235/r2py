import pandas as pd
import numpy as np
from datetime import timedelta

def as_hms(time_str):
    # Return a timedelta representing the hms time
    return pd.to_timedelta(time_str)

def format_hms(td):
    # Format timedelta to HH:MM:SS[.sss] to match R hms output
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    
    if seconds == int(seconds):
        return f"{hours:02}:{minutes:02}:{int(seconds):02}"
    else:
        # Remove trailing zeros and unnecessary decimal point to match R's rounding
        s_str = f"{seconds:.6f}".rstrip('0').rstrip('.')
        # R's hms usually keeps a reasonable precision
        # The verification shows "12:34:56.75" and "12:34:56.8"
        # We'll use a simpler formatting and let the rounding logic handle the value
        return f"{hours:02}:{minutes:02}:{seconds:g}"

# r2py:entity:round_hms
def digits_to_secs(secs=None, digits=None):
    if digits is None:
        if secs is None:
            raise ValueError("Exactly one of `secs` or `digits` is required.")
        return secs
    if secs is not None:
        raise ValueError("Exactly one of `secs` or `digits` is required.")
    
    # R logic for digits_to_secs
    if digits >= -1:
        return 10**(-digits)
    elif digits == -2:
        return 60.0
    elif digits == -3:
        return 600.0
    elif digits <= -4:
        return 3600.0 * (10**(-digits - 4))
    return 1.0

def round_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    total_seconds = x.total_seconds()
    # R's round() typically rounds to nearest even for .5, 
    # but for these intervals, standard rounding is usually intended.
    # np.round is round-to-even.
    rounded_seconds = np.round(total_seconds / s) * s
    return pd.to_timedelta(rounded_seconds, unit='s')

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    total_seconds = x.total_seconds()
    truncated_seconds = np.trunc(total_seconds / s) * s
    return pd.to_timedelta(truncated_seconds, unit='s')

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    total_seconds = x.total_seconds()
    ceiled_seconds = np.ceil(total_seconds / s) * s
    return pd.to_timedelta(ceiled_seconds, unit='s')

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    total_seconds = x.total_seconds()
    floored_seconds = np.floor(total_seconds / s) * s
    return pd.to_timedelta(floored_seconds, unit='s')

# The R calls pass the second argument as 'secs' because they are passed positionally.
# In R: round_hms(as_hms("12:34:56"), 5) -> x=as_hms, secs=5
# round_hms(as_hms("12:34:56.78"), digits = 1) -> x=as_hms, digits=1

# r2py:entity:round_hms
print(format_hms(round_hms(as_hms("12:34:56"), secs=5)))
# r2py:entity:round_hms_1
print(format_hms(round_hms(as_hms("12:34:56"), secs=60)))
# r2py:entity:round_hms_2
print(format_hms(round_hms(as_hms("12:34:56.78"), secs=0.25)))
# r2py:entity:round_hms_3
print(format_hms(round_hms(as_hms("12:34:56.78"), digits=1)))
# r2py:entity:round_hms_4
print(format_hms(round_hms(as_hms("12:34:56.78"), digits=-2)))
# r2py:entity:trunc_hms
print(format_hms(trunc_hms(as_hms("12:34:56"), secs=60)))
# r2py:entity:ceiling_hms
print(format_hms(ceiling_hms(as_hms("12:34:56"), secs=60)))
# r2py:entity:floor_hms
print(format_hms(floor_hms(as_hms("12:34:56"), secs=60)))