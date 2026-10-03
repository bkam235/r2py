# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
from datetime import datetime, timedelta, date
import pytz

# r2py:entity:new_date
def new_date(x=0.0):
    """
    Equivalent to vctrs::new_date.
    In R, new_date(0) refers to the origin 1970-01-01.
    """
    return pd.to_datetime(x, unit='D', origin='unix').date()

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    """
    Equivalent to vctrs::new_datetime.
    """
    dt = pd.to_datetime(x, unit='s', origin='unix')
    if tzone:
        dt = dt.tz_localize('UTC').tz_convert(tzone)
    return dt

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    """
    Equivalent to vctrs::new_duration.
    """
    if not isinstance(x, (int, float)):
        raise TypeError("x must be a double (int or float)")
    
    unit_map = {
        "secs": "seconds",
        "mins": "minutes",
        "hours": "hours",
        "days": "days",
        "weeks": "weeks"
    }
    
    if units not in unit_map:
        raise ValueError(f"units must be one of {list(unit_map.keys())}")
    
    # R's difftime is essentially a numeric value with a unit attribute.
    # For the sake of the example output "Time difference of 1 hours", 
    # we simulate the string representation.
    class Difftime:
        def __init__(self, value, unit):
            self.value = value
            self.unit = unit
        def __repr__(self):
            return f"Time difference of {self.value} {self.unit}"
        def __str__(self):
            return self.__repr__()

    return Difftime(x, units)

# suppressPackageStartupMessages(library(vctrs))
# Equivalent to importing the logic provided above.

# r2py:entity:new_date
print(f'[1] "{new_date(0)}"')

# r2py:entity:new_datetime
res_dt = new_datetime(0, tzone="UTC")
# Formatting to match "1970-01-01 UTC"
print(f'[1] "{res_dt.strftime("%Y-%m-%d %Z")}"')

# r2py:entity:new_duration
print(new_duration(1, "hours"))