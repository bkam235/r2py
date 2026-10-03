# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# r2py:entity:new_date
def new_date(x=0.0):
    # vctrs::new_date creates a date from days since the Unix epoch (1970-01-01)
    return pd.to_datetime(x, unit='D').date()

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    # vctrs::new_datetime creates a datetime from seconds since the Unix epoch
    # Convert x to datetime and localize/convert to tzone
    dt = pd.to_datetime(x, unit='s', utc=True)
    if tzone:
        dt = dt.tz_convert(tzone)
    return dt

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # vctrs::new_duration returns a difftime object
    # Mapping R duration units to pandas/python timedelta arguments
    unit_map = {
        "secs": "seconds",
        "mins": "minutes",
        "hours": "hours",
        "days": "days",
        "weeks": "weeks"
    }
    
    if not isinstance(x, (int, float)):
        raise TypeError("x must be a double")
    
    if units not in unit_map:
        raise ValueError(f"units must be one of {list(unit_map.keys())}")
    
    kwargs = {unit_map[units]: x}
    return pd.Timedelta(**kwargs)

# Execute translated examples
# r2py:entity:new_date
res1 = new_date(0)
# r2py:entity:new_datetime
res2 = new_datetime(0, tzone="UTC")
# r2py:entity:new_duration
res3 = new_duration(1, "hours")

print(res1)
print(res2)
print(res3)