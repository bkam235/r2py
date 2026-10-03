# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import pandas as pd
from datetime import timedelta

# r2py:entity:round_hms
def as_hms(x):
    if isinstance(x, str):
        parts = x.split(':')
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
        return h * 3600 + m * 60 + s
    return float(x)

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
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = td.total_seconds() % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".rstrip('0').rstrip('.')

def round_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    res = round(x / s_val) * s_val
    return res

# r2py:entity:trunc_hms
def trunc_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    res = np.trunc(x / s_val) * s_val
    return res

# r2py:entity:ceiling_hms
def ceiling_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    res = np.ceil(x / s_val) * s_val
    return res

# r2py:entity:floor_hms
def floor_hms(x, secs=None, digits=None):
    s_val = digits_to_secs(secs, digits)
    res = np.floor(x / s_val) * s_val
    return res

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