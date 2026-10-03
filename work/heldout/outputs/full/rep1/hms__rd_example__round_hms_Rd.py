# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from datetime import timedelta

def as_hms(x):
    """Converts a time string 'HH:MM:SS.ss' to total seconds."""
    if isinstance(x, str):
        parts = x.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    return float(x)

# r2py:entity:round_hms
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
    """Helper to represent the 'hms' class output as a string."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = td.total_seconds() % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}".rstrip('0').rstrip('.')

def round_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return round(x / s) * s

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return np.trunc(x / s) * s

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return np.ceil(x / s) * s

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return np.floor(x / s) * s

# Executing the script logic
# r2py:entity:round_hms
print(format_hms(round_hms(as_hms("12:34:56"), 5)))
# r2py:entity:round_hms_1
print(format_hms(round_hms(as_hms("12:34:56"), 60)))
# r2py:entity:round_hms_2
print(format_hms(round_hms(as_hms("12:34:56.78"), 0.25)))
# r2py:entity:round_hms_3
print(format_hms(round_hms(as_hms("12:34:56.78"), digits=1)))
# r2py:entity:round_hms_4
print(format_hms(round_hms(as_hms("12:34:56.78"), digits=-2)))
# r2py:entity:trunc_hms
print(format_hms(trunc_hms(as_hms("12:34:56"), 60)))
# r2py:entity:ceiling_hms
print(format_hms(ceiling_hms(as_hms("12:34:56"), 60)))
# r2py:entity:floor_hms
print(format_hms(floor_hms(as_hms("12:34:56"), 60)))