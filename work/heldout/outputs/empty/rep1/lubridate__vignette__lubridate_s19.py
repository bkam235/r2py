# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from datetime import timedelta

# r2py:entity:last_day
def last_day(date):
    # Convert to pandas Timestamp if not already
    date = pd.to_datetime(date)
    # Move to the first day of the next month, then subtract one day
    next_month = date + pd.offsets.MonthBegin(1)
    return next_month - pd.Timedelta(days=1)