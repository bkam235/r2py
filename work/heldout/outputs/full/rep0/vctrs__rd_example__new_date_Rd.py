# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
from datetime import datetime, timedelta, date, timezone

# r2py:entity:new_date
def new_date(x=0.0):
    # In R vctrs, new_date(0) typically represents the origin date (1970-01-01)
    # R prints as "YYYY-MM-DD"
    return pd.to_datetime(x, unit='D').strftime('%Y-%m-%d')

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    # In R vctrs, new_datetime(0) represents the Unix epoch in the specified timezone
    ts = pd.to_datetime(x, unit='s', utc=True)
    if tzone != "":
        import pytz
        ts = ts.tz_convert(tzone)
    # R prints as "YYYY-MM-DD TZ" (for simple dates) or "YYYY-MM-DD HH:MM:SS TZ"
    # Based on R output "1970-01-01 UTC", we format accordingly
    return ts.strftime('%Y-%m-%d %Z').strip() if ts.hour == 0 and ts.minute == 0 and ts.second == 0 else ts.strftime('%Y-%m-%d %H:%M:%S %Z')

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # Map R duration units to pandas Timedelta keywords
    unit_map = {
        "secs": "seconds",
        "mins": "minutes",
        "hours": "hours",
        "days": "days",
        "weeks": "weeks"
    }
    if units not in unit_map:
        raise ValueError(f"units must be one of {list(unit_map.keys())}")
    
    # R's new_duration returns a difftime object. 
    # Output format: "Time difference of 1 hours"
    return f"Time difference of {x} {units.rstrip('s') if units != 'secs' else 'secs' if x == 1 else 'secs'}" 
    # Note: The R output provided was "Time difference of 1 hours", implying it might keep the 's' or have specific pluralization.
    # Let's match the exact R output: "Time difference of 1 hours"
    
# Redefining new_duration to match the specific R output "Time difference of 1 hours"
# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # R output: "Time difference of 1 hours"
    # The R implementation is actually structure(x, units = units, class_val= "difftime")
    # Which prints as "Time difference of X units"
    return f"Time difference of {x} {units}"

# Executing the examples
# r2py:entity:new_date
print(f'[1] "{new_date(0)}"')
# r2py:entity:new_datetime
print(f'[1] "{new_datetime(0, tzone="UTC")}"')
# r2py:entity:new_duration
print(new_duration(1, "hours"))