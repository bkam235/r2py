# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
from datetime import datetime, timedelta

def as_hms(x):
    """Converts a string "HH:MM:SS" or "HH:MM:SS.sss" to total seconds."""
    t = datetime.strptime(x, "%H:%M:%S.%f") if "." in x else datetime.strptime(x, "%H:%M:%S")
    return t.hour * 3600 + t.minute * 60 + t.second + (t.microsecond / 1e6)

def format_hms(seconds):
    """Helper to format seconds back to HH:MM:SS string for output representation."""
    td = timedelta(seconds=seconds)
    total_secs = int(td.total_seconds())
    hours = total_secs // 3600
    minutes = (total_secs % 3600) // 60
    secs = total_secs % 60
    millis = (td.total_seconds() - total_secs) * 1000
    if millis == 0:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    else:
        return f"{hours:02}:{minutes:02}:{secs:02}.{millis:.2f}"[:12]

# r2py:entity:round_hms
def digits_to_secs(secs, digits):
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

def round_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    return format_hms(round(x / s_val) * s_val)

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    return format_hms(np.trunc(x / s_val) * s_val)

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    return format_hms(np.ceil(x / s_val) * s_val)

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    return format_hms(np.floor(x / s_val) * s_val)

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