# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
from datetime import datetime, timedelta

# r2py:entity:x
def ymd(date_str):
    return pd.to_datetime(date_str)

# r2py:entity:minute
def minute(x):
    if isinstance(x, pd.Timestamp):
        return x.minute
    return None

# r2py:entity:minute(x)
def set_minute(x, val):
    # Handles the R logic where minute(x) <- val updates the object
    # and handles overflow (e.g., minute(x) <- 61)
    # R's lubridate allows setting minutes > 59, which rolls over into hours
    
    # First, normalize to the start of the hour
    base = x - pd.Timedelta(minutes=x.minute) - pd.Timedelta(seconds=x.second) - pd.Timedelta(microseconds=x.microsecond)
    
    # Add the new minute value (allows overflow)
    return base + pd.Timedelta(minutes=val)

# r2py:entity:x
x = ymd("2012-03-26")
# r2py:entity:minute
print(minute(x))

# minute(x) <- 1
# r2py:entity:minute(x)
x = set_minute(x, 1)

# minute(x) <- 61
# r2py:entity:minute(x)_1
x = set_minute(x, 61)

# minute(x) > 2
# r2py:entity:minute_1
print(minute(x) > 2)