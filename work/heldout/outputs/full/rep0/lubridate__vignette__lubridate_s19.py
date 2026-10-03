# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from datetime import timedelta

# r2py:entity:last_day
def last_day(date):
    # ceiling_date(date, "month") - days(1)
    # Shift to the first of the next month, then subtract one day
    next_month = date.replace(day=1) + pd.DateOffset(months=1)
    return next_month - timedelta(days=1)