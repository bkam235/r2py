# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
from datetime import datetime, timedelta

# r2py:entity:parse_hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    """
    Equivalent to the hms function which calculates total seconds.
    """
    total_secs = 0.0
    if days is not None:
        total_secs += days * 86400
    if hours is not None:
        total_secs += hours * 3600
    if minutes is not None:
        total_secs += minutes * 60
    if seconds is not None:
        total_secs += seconds
    
    # R's hms returns a specialized duration object. In Python, 
    # we represent this as a timedelta or the total seconds.
    return timedelta(seconds=total_secs)

def parse_time(x, format_str):
    """
    Helper to parse time strings based on a format.
    """
    if x is None or x == "":
        return hms()
    
    # Mimic R's strptime logic by adding a base date
    full_str = f"1970-01-01 {x}"
    full_format = f"%Y-%m-%d {format_str}"
    
    try:
        dt = datetime.strptime(full_str, full_format)
        # R's parse_time uses mday to handle overflows or specific offsets
        # For standard time strings, we extract hours, minutes, seconds
        return hms(
            hours=dt.hour, 
            minutes=dt.minute, 
            seconds=dt.second + (dt.microsecond / 1_000_000)
        )
    except ValueError:
        return None

def parse_hms(x):
    """
    Parse string as hours:minutes:seconds.
    """
    # %OS in R allows for fractional seconds. 
    # Python's %S is seconds, we handle the fraction via datetime.
    # We adjust the format to be compatible with strptime.
    fmt = "%H:%M:%S"
    if "." in x:
        # If milliseconds are present, %S in Python handles them if using %f
        # but strptime is strict. We'll manually handle common R %OS cases.
        # For simplicity in this translation, we adapt the format.
        fmt = "%H:%M:%S.%f"
    
    return parse_time(x, fmt)

# r2py:entity:parse_hm
def parse_hm(x):
    """
    Parse string as hours:minutes.
    """
    return parse_time(x, "%H:%M")

# Main script execution
# r2py:entity:parse_hms
print(parse_hms("12:34:56"))
# r2py:entity:parse_hms_1
print(parse_hms("12:34:56.789"))
# r2py:entity:parse_hm
print(parse_hm("12:34"))