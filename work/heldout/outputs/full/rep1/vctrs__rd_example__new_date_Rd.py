# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
from datetime import datetime, timedelta, date

# r2py:entity:new_date
def new_date(x=0.0):
    # R's new_date(0) typically represents the epoch (1970-01-01)
    return pd.to_datetime(x, unit='D').date()

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    # R's new_datetime(0) typically represents the epoch (1970-01-01 00:00:00)
    dt = pd.to_datetime(x, unit='s')
    if tzone:
        dt = dt.tz_localize('UTC').tz_convert(tzone)
    return dt

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # vctrs durations are essentially difftime objects in R
    unit_map = {
        "secs": "seconds",
        "mins": "minutes",
        "hours": "hours",
        "days": "days",
        "weeks": "weeks"
    }
    if units not in unit_map:
        raise ValueError(f"units must be one of {list(unit_map.keys())}")
    
    return timedelta(**{unit_map[units]: x})

# Execute examples
# r2py:entity:new_date
res1 = new_date(0)
# r2py:entity:new_datetime
res2 = new_datetime(0, tzone="UTC")
# r2py:entity:new_duration
res3 = new_duration(1, "hours")

print(res1)
print(res2)
print(res3)