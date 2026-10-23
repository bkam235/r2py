# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd
from datetime import datetime

# r2py:entity:tC
def timeDate(charvec, format=None, zone="", FinCenter=""):
    # In the R package timeDate, this typically returns a character vector
    # with specific attributes. We represent this as a dictionary.
    return {
        "Data": list(charvec),
        "format": format,
        "zone": zone,
        "FinCenter": FinCenter
    }

def timeCalendar(y=datetime.now().year, m=None, d=1, h=0, min_val=0, s=0, zone="", FinCenter=""):
    if m is None:
        m = list(range(1, 13))
    
    # Default values for Rmetrics options mimics
    default_zone = "GMT"
    default_fincenter = "GMT"
    
    if zone == "":
        zone = default_zone
    if FinCenter == "":
        FinCenter = default_fincenter
    
    # Handle vectorization logic
    y = np.atleast_1d(y)
    m = np.atleast_1d(m)
    d = np.atleast_1d(d)
    h = np.atleast_1d(h)
    min_val = np.atleast_1d(min_val)
    s = np.atleast_1d(s)
    
    data_len = max(len(y), len(m), len(d), len(h), len(min_val), len(s))
    
    def broadcast(arr, length):
        if len(arr) < length:
            return np.repeat(arr, length // len(arr))
        return arr

    y = broadcast(y, data_len)
    m = broadcast(m, data_len)
    d = broadcast(d, data_len)
    h = broadcast(h, data_len)
    min_val = broadcast(min_val, data_len)
    s = broadcast(s, data_len)
    
    # Compute CCYYMMDD and xhhmmss logic as per R source
    # CCYYMMDD = y * 10000 + m * 100 + d
    # xhhmmss = 1e6 + h * 10000 + min * 100 + s
    
    charvec = []
    is_time_default = np.all(1e6 + h * 10000 + min_val * 100 + s == 1e6)
    
    for i in range(data_len):
        date_str = f"{int(y[i]):04d}{int(m[i]):02d}{int(d[i]):02d}"
        if is_time_default:
            charvec.append(date_str)
        else:
            time_str = f"{int(h[i]):02d}{int(min_val[i]):02d}{int(s[i]):02d}"
            charvec.append(date_str + time_str)
            
    format_str = "%Y%m%d" if is_time_default else "%Y%m%d%H%M%S"
    
    return timeDate(charvec=charvec, format=format_str, zone=zone, FinCenter=FinCenter)

# r2py:entity:dayOfWeek
def dayOfWeek(x):
    # x is expected to be the dict returned by timeCalendar
    dates_raw = x["Data"]
    fmt = x["format"]
    
    wd = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    results = []
    names = []
    
    for ds in dates_raw:
        dt = datetime.strptime(ds, fmt)
        # R's wday is 0 (Sun) to 6 (Sat)
        # Python's weekday() is 0 (Mon) to 6 (Sun)
        # strftime('%a') is the most direct way to get 'Sun', 'Mon', etc.
        results.append(dt.strftime('%a'))
        # R's format(x) for timeDate objects usually returns YYYY-MM-DD
        names.append(dt.strftime('%Y-%m-%d'))
        
    return pd.Series(results, index=names)

# Main execution
# r2py:entity:tC
tC = timeCalendar(2022)
# r2py:entity:dayOfWeek
print(dayOfWeek(tC))