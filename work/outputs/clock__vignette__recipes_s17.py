# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

import pandas as pd
import numpy as np

# Define dates
# r2py:entity:x
x = pd.to_datetime(["2019-01-01", "2019-02-01"]).date

# Shift to the most recent Monday
# r2py:entity:monday
# In pandas, weekday() returns 0 for Monday. 
# To shift back to the previous Monday: date - timedelta(days=weekday)
# r2py:entity:date_shift
x_shifted = pd.to_datetime(x) - pd.to_timedelta(pd.to_datetime(x).weekday, unit='D')
print(x_shifted.date)

# Define POSIXct equivalent with timezone
# r2py:entity:y
y = pd.to_datetime(
    ["2019-01-01 02:30:30", "2019-02-01 05:20:22"]
).tz_localize("America/New_York")

# Shift to the most recent Monday while preserving time
# r2py:entity:date_shift_1
y_shifted = y - pd.to_timedelta(y.weekday, unit='D')
print(y_shifted)