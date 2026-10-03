# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from datetime import timedelta

# r2py:entity:last_day
def last_day(date):
    # Convert to pandas Timestamp if it isn't already
    date = pd.to_datetime(date)
    # ceiling_date(date, "month") is equivalent to the first day of the next month
    # Offset by 1 month, then subtract 1 day
    next_month_first_day = date + pd.offsets.MonthBegin(1)
    return next_month_first_day - pd.Timedelta(days=1)