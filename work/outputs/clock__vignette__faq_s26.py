# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
from datetime import datetime
import pytz

# r2py:entity:as.Date
def date_time_zone(x):
    """
    Extracts the time zone from a datetime-like object.
    In Python, this is the tzinfo attribute.
    """
    if x.tzinfo is None:
        return ""
    return str(x.tzinfo)

# r2py:entity:as.Date
def as_date(x, tz=None):
    """
    Translates as.Date logic.
    R's as.Date with a specified tz converts the POSIXct time to the date 
    that would be observed in that specific time zone.
    """
    # Convert the datetime object to the specified time zone
    target_tz = pytz.timezone(tz) if tz else pytz.UTC
    
    # Localize/convert to the target timezone
    if x.tzinfo is None:
        # If naive, assume UTC or treat as local and then convert
        x_localized = pytz.UTC.localize(x)
    else:
        x_localized = x.astimezone(target_tz)
        
    # Convert to the target timezone if it wasn't already
    x_in_tz = x_localized.astimezone(target_tz)
    
    # Return the date component
    return x_in_tz.date()

# x <- as.POSIXct("2019-01-01 23:00:00", "America/New_York")
# r2py:entity:x
tz_ny = pytz.timezone("America/New_York")
x = tz_ny.localize(datetime.strptime("2019-01-01 23:00:00", "%Y-%m-%d %H:%M:%S"))

# as.Date(x, tz = date_time_zone(x))
# r2py:entity:as.Date
result = as_date(x, tz=date_time_zone(x))
print(result)