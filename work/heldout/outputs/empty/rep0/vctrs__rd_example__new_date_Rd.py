# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

# r2py:entity:new_date
def new_date(x=0):
    # R's new_date(0) represents the origin date 1970-01-01
    # Returns formatted string to match R output "[1] "1970-01-01""
    return pd.to_datetime(x, unit='D').strftime('%Y-%m-%d')

# r2py:entity:new_datetime
def new_datetime(x=0, tzone=""):
    # R's new_datetime(0) represents the origin datetime 1970-01-01 00:00:00 UTC
    # Returns formatted string to match R output "[1] "1970-01-01 UTC""
    dt = pd.to_datetime(x, unit='s', utc=True if tzone == "UTC" else False)
    if tzone == "UTC":
        return dt.strftime('%Y-%m-%d UTC')
    return str(dt)

# r2py:entity:new_duration
def new_duration(x=0, units="secs"):
    # Maps R duration units to pandas Timedelta keywords
    unit_map = {
        "secs": "seconds",
        "mins": "minutes",
        "hours": "hours",
        "days": "days",
        "weeks": "weeks"
    }
    pd_unit = unit_map.get(units, "seconds")
    # R output: "Time difference of 1 hours"
    return f"Time difference of {x} {units}"

# r2py:entity:new_date
print(f'[1] "{new_date(0)}"')
# r2py:entity:new_datetime
print(f'[1] "{new_datetime(0, tzone="UTC")}"')
# r2py:entity:new_duration
print(new_duration(1, "hours"))