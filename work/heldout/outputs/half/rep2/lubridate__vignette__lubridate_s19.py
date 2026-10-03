# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from datetime import timedelta
from pandas.tseries.offsets import MonthEnd

# r2py:entity:last_day
def last_day(date):
    return pd.to_datetime(date) + MonthEnd(0)