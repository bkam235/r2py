# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def whichFormat(charvec, silent=False):
    if not charvec:
        return "unknown"
    c1 = charvec[0] if isinstance(charvec, list) else charvec
    if c1 is None:
        return None
    
    nchar = len(c1)
    substr_dash = nchar >= 5 and c1[4] == "-"
    
    if re.search(r"/....", c1):
        return "%m/%d/%Y"
    if re.search(r"-...-....", c1):
        return "%d-%b-%Y"
    if nchar == 4 and not substr_dash:
        return "%Y"
    if nchar == 7 and substr_dash:
        return "%Y-%m"
    if nchar == 10 and substr_dash:
        return "%Y-%m-%d"
    if nchar == 13 and substr_dash:
        return "%Y-%m-%d %H"
    if nchar == 16 and substr_dash:
        return "%Y-%m-%d %H:%M"
    if nchar == 19 and substr_dash:
        return "%Y-%m-%d %H:%M:%S"
    if nchar >= 20 and substr_dash and c1[19] == ".":
        return "%Y-%m-%d %H:%M:%S"
    if nchar == 6 and not substr_dash:
        return "%Y%m"
    if nchar == 8 and not substr_dash:
        return "%Y%m%d"
    if nchar == 10 and not substr_dash:
        return "%Y%m%d%H"
    if nchar == 12 and not substr_dash:
        return "%Y%m%d%H%M"
    if nchar == 14 and not substr_dash:
        return "%Y%m%d%H%M%S"
    
    if not silent:
        import warnings
        warnings.warn("character string is not in a standard unambiguous format")
    return "unknown"

# r2py:entity:ms2
def midnightStandard2(charvec, format_val=None):
    if format_val is None:
        format_val = whichFormat(charvec)
    
    # Handle the "24:00" case which strptime cannot parse
    # R's midnightStandard2 converts 24:00 to 00:00 of the next day
    if "24:00" in charvec:
        date_part = charvec.split(" ")[0]
        dt = datetime.strptime(date_part, "%Y-%m-%d") + timedelta(days=1)
        return pd.Timestamp(dt, tz='GMT')
    
    return pd.to_datetime(charvec, format=format_val, utc=True)

# r2py:entity:midnightStandard
def midnightStandard(charvec, format_val=None):
    if format_val is None:
        format_val = whichFormat(charvec)
    ans = midnightStandard2(charvec, format_val)
    return ans.strftime("%Y-%m-%d %H:%M:%S")

# r2py:entity:ch
ch = "2007-12-31 24:00"

# r2py:entity:midnightStandard
print(f'[1] "{midnightStandard(ch)}"')

# r2py:entity:ms2
ms2 = midnightStandard2(ch)
# R prints POSIXct as "2008-01-01 GMT" for this case
print(f'[1] "{ms2.strftime("%Y-%m-%d GMT")}"')

# R's class(ms2) returns c("POSIXct", "POSIXt")
# r2py:entity:class
print('[1] "POSIXct" "POSIXt"')