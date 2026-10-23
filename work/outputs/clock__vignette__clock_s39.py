# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

try:
# r2py:entity:x
    # date_time_build equivalent using pandas/pytz
    # 1970, 04, 25, 02, 30, 00
    x = pd.Timestamp(year=1970, month=4, day=25, hour=2, minute=30, second=0, tz="America/New_York")
    print(x)

# r2py:entity:add_days
    # add_days(1) equivalent
    print(x + pd.Timedelta(days=1))
except Exception as e:
    print(e)