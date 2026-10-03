# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
from datetime import timedelta
import math

def as_hms(x):
    """Convert a time string 'HH:MM:SS[.ms]' to total seconds."""
    parts = x.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

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
        return 60
    elif digits == -3:
        return 600
    elif digits <= -4:
        return 3600 * (10**(-digits - 4))
    return None

def format_hms(seconds):
    """Helper to return a representation similar to hms class."""
    return str(timedelta(seconds=seconds))

def round_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return format_hms(round(x / s) * s)

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return format_hms(math.trunc(x / s) * s)

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return format_hms(math.ceil(x / s) * s)

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s = digits_to_secs(secs, digits)
    return format_hms(math.floor(x / s) * s)

# Executing example code
# r2py:entity:round_hms
print(round_hms(as_hms("12:34:56"), secs=5))
# r2py:entity:round_hms_1
print(round_hms(as_hms("12:34:56"), secs=60))
# r2py:entity:round_hms_2
print(round_hms(as_hms("12:34:56.78"), secs=0.25))
# r2py:entity:round_hms_3
print(round_hms(as_hms("12:34:56.78"), digits=1))
# r2py:entity:round_hms_4
print(round_hms(as_hms("12:34:56.78"), digits=-2))
# r2py:entity:trunc_hms
print(trunc_hms(as_hms("12:34:56"), secs=60))
# r2py:entity:ceiling_hms
print(ceiling_hms(as_hms("12:34:56"), secs=60))
# r2py:entity:floor_hms
print(floor_hms(as_hms("12:34:56"), secs=60))