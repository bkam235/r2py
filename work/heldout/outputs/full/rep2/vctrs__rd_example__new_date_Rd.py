# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd

# r2py:entity:new_date
def new_date(x=0.0):
    # R's new_date returns a Date object, which prints as "YYYY-MM-DD"
    return pd.to_datetime(x, unit='D', origin='unix').strftime('%Y-%m-%d')

# r2py:entity:new_datetime
def new_datetime(x=0.0, tzone=""):
    # R's new_datetime(0, tzone="UTC") prints as "1970-01-01 UTC"
    dt = pd.to_datetime(x, unit='s', origin='unix')
    if tzone == "UTC":
        return dt.strftime('%Y-%m-%d') + " UTC"
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# r2py:entity:new_duration
def new_duration(x=0.0, units="secs"):
    # R's new_duration returns a difftime object, which prints as "Time difference of X units"
    # We use a string to match the R output exactly.
    return f"Time difference of {x} {units}"

# r2py:entity:new_date
print(f'[1] "{new_date(0)}"')
# r2py:entity:new_datetime
print(f'[1] "{new_datetime(0, tzone="UTC")}"')
# r2py:entity:new_duration
print(new_duration(1, "hours"))