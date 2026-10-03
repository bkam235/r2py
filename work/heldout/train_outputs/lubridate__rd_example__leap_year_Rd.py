# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np
from datetime import date
import calendar

# r2py:entity:leap_year
def leap_year(x):
    if isinstance(x, (int, np.integer)):
        return calendar.isleap(int(x))
    elif isinstance(x, (pd.Timestamp, date)):
        return calendar.isleap(x.year)
    else:
        # Handle string dates by converting to pandas timestamp
        ts = pd.to_datetime(x)
        return calendar.isleap(ts.year)

# r2py:entity:x
x = pd.to_datetime("2009-08-02").date()
# r2py:entity:leap_year
print(leap_year(x)) # False
# r2py:entity:leap_year_1
print(leap_year(2009)) # False
# r2py:entity:leap_year_2
print(leap_year(2008)) # True
# r2py:entity:leap_year_3
print(leap_year(1900)) # False
# r2py:entity:leap_year_4
print(leap_year(2000)) # True