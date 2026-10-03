# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# In R, new_date(0) represents the epoch date (1970-01-01)
# The R expression is auto-printed.
# r2py:entity:new_date
new_date_res = pd.to_datetime(0, unit='D', origin='unix').date()
print(new_date_res)

# In R, new_datetime(0, tzone = "UTC") represents the epoch timestamp
# The R expression is auto-printed.
# r2py:entity:new_datetime
new_datetime_res = pd.to_datetime(0, unit='s', utc=True)
print(new_datetime_res)

# In R, new_duration(1, "hours") represents a duration of 1 hour
# The R expression is auto-printed.
# r2py:entity:new_duration
new_duration_res = pd.Timedelta(hours=1)
print(new_duration_res)