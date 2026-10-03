# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:entity:new_date
def new_date(x=0.0):
    # R's new_date returns a Date object. 
    # In R, printing a Date object results in "YYYY-MM-DD"
    return pd.to_datetime(x, unit='D').strftime('%Y-%m-%d')

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    # R's new_datetime returns a POSIXct object.
    # Printing it often looks like "YYYY-MM-DD UTC" or "YYYY-MM-DD HH:MM:SS TZ"
    dt = pd.to_datetime(x, unit='s', utc=True)
    if tzone == "UTC":
        return dt.strftime('%Y-%m-%d UTC')
    return dt

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # R's new_duration creates a difftime object.
    # R prints this as "Time difference of X units"
    # Note: The R source shows it uses structure(x, units=units, class_val="difftime")
    return f"Time difference of {x} {units}"

# Execute example calls
# r2py:entity:new_date
print(f'[1] "{new_date(0)}"')
# r2py:entity:new_datetime
print(f'[1] "{new_datetime(0, tzone="UTC")}"')
# r2py:entity:new_duration
print(new_duration(1, "hours"))