# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
from datetime import timedelta

def as_hms(x):
    """Convert a time string 'HH:MM:SS[.ms]' to total seconds."""
    parts = x.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def digits_to_secs(secs=None, digits=None):
    if digits is None:
        if secs is None:
            raise ValueError("Exactly one of `secs` or `digits` is required.")
        return secs
    if secs is not None:
        raise ValueError("Exactly one of `secs` or `digits` is required.")
    
    if not float(digits).is_integer():
        raise ValueError("`digits` must be a whole number")
    
    digits = int(digits)
    if digits >= -1:
        return 10**-digits
    elif digits == -2:
        return 60.0
    elif digits == -3:
        return 600.0
    elif digits <= -4:
        return 3600.0 * (10**(-digits - 4))
    return None

def format_hms(seconds):
    """Helper to represent the result as a time string similar to hms class."""
    # hms objects represent time since midnight.
    # Total seconds can be slightly off due to precision; round to a reasonable level.
    total_secs = round(seconds, 6)
    
    hours = int(total_secs // 3600)
    minutes = int((total_secs % 3600) // 60)
    secs = total_secs % 60
    
    # If seconds is a whole number, format as HH:MM:SS
    if secs == int(secs):
        return f"{hours:02}:{minutes:02}:{int(secs):02}"
    else:
        # If fractional, format as HH:MM:SS.s
        # R's hms format typically shows enough decimals to represent the value
        return f"{hours:02}:{minutes:02}:{secs:06.3g}"

# r2py:entity:round_hms
def round_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    # R's round() uses "round to even" for .5
    val = np.round(x / s) * s
    return format_hms(val)

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    val = np.trunc(x / s) * s
    return format_hms(val)

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    val = np.ceil(x / s) * s
    return format_hms(val)

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    val = np.floor(x / s) * s
    return format_hms(val)

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