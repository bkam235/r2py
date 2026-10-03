# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from datetime import timedelta

def as_hms(time_str):
    return pd.to_timedelta(time_str)

# r2py:entity:round_hms
def round_hms(t, digits):
    # R's round_hms: if digits is a small number, it's seconds. 
    # If digits is large/specific, it's a rounding interval.
    # R implementation treats digits as the unit to round to (in seconds).
    seconds = t.total_seconds()
    rounded_seconds = round(seconds / digits) * digits
    return pd.to_timedelta(rounded_seconds, unit='s')

# r2py:entity:trunc_hms
def trunc_hms(t, digits):
    seconds = t.total_seconds()
    truncated_seconds = np.floor(seconds / digits) * digits
    return pd.to_timedelta(truncated_seconds, unit='s')

# r2py:entity:ceiling_hms
def ceiling_hms(t, digits):
    seconds = t.total_seconds()
    ceiled_seconds = np.ceil(seconds / digits) * digits
    return pd.to_timedelta(ceiled_seconds, unit='s')

# r2py:entity:floor_hms
def floor_hms(t, digits):
    seconds = t.total_seconds()
    floored_seconds = np.floor(seconds / digits) * digits
    return pd.to_timedelta(floored_seconds, unit='s')

# r2py:entity:round_hms
print(round_hms(as_hms("12:34:56"), 5))
# r2py:entity:round_hms_1
print(round_hms(as_hms("12:34:56"), 60))
# r2py:entity:round_hms_2
print(round_hms(as_hms("12:34:56.78"), 0.25))
# r2py:entity:round_hms_3
print(round_hms(as_hms("12:34:56.78"), 1))
# r2py:entity:round_hms_4
print(round_hms(as_hms("12:34:56.78"), -2)) # Note: R's round_hms with negative digits is unusual, Python follows math logic
# r2py:entity:trunc_hms
print(trunc_hms(as_hms("12:34:56"), 60))
# r2py:entity:ceiling_hms
print(ceiling_hms(as_hms("12:34:56"), 60))
# r2py:entity:floor_hms
print(floor_hms(as_hms("12:34:56"), 60))