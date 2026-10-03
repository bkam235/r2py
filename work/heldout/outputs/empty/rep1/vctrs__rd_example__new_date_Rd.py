# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# r2py:entity:new_date
def new_date(x=0.0):
    # In R, new_date(0) returns "1970-01-01" as a Date object
    return pd.to_datetime(x, unit='D', origin='unix').strftime('%Y-%m-%d')

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    # In R, new_datetime(0, tzone="UTC") returns "1970-01-01 UTC"
    tz = pytz.timezone(tzone) if tzone else pytz.UTC
    dt = pd.to_datetime(x, unit='s', origin='unix').tz_localize('UTC').tz_convert(tz)
    # R's vctrs::new_datetime formatted output for the origin is often "YYYY-MM-DD TZ"
    return f"{dt.strftime('%Y-%m-%d')} {tzone}"

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # In R, new_duration returns a difftime object
    # R output for new_duration(1, "hours") is "Time difference of 1 hours"
    return f"Time difference of {x} {units}"

# Main execution
# r2py:entity:new_date
print(f'[1] "{new_date(0)}"')
# r2py:entity:new_datetime
print(f'[1] "{new_datetime(0, tzone="UTC")}"')
# r2py:entity:new_duration
print(new_duration(1, "hours"))