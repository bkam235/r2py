# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from datetime import timedelta

# r2py:entity:last_day
def last_day(date):
    # ceiling_date(date, "month") logic:
    # Get the first day of the next month and subtract one day
    # Convert to period to find the end of the current month
    return pd.to_datetime(date) + pd.offsets.MonthEnd(0)