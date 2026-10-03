# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
from datetime import datetime, timedelta
import pytz

# r2py:entity:GMT
def timeDate(charvec, format=None, zone="", FinCenter=""):
    # In R's timeDate package, this object typically handles date-times 
    # with specific time zones. We represent this as a list of 
    # timezone-aware pandas Timestamps.
    tz = pytz.timezone(zone if zone else "UTC")
    
    # Assuming standard ISO format since format is None in example
    dt_list = []
    for s in charvec:
        dt = pd.to_datetime(s)
        # Localize to the specified zone
        localized = tz.localize(dt)
        dt_list.append(localized)
    
    # FinCenter is a metadata attribute in R's timeDate class.
    # We can store this as an attribute on the list or a custom object,
    # but for the arithmetic in the example, the Timestamp objects suffice.
    return dt_list

# create some data
# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
# r2py:entity:tms
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]

# r2py:entity:GMT
GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
# r2py:entity:ZUR
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")

# add one day
# In R, adding to a timeDate object adds seconds.
# We apply this to the collection.
GMT_plus_day = [dt + timedelta(seconds=24*3600) for dt in GMT]
print(GMT_plus_day)

# subtract
# R indices are 1-based. ZUR[2] - ZUR[1] translates to index 1 minus index 0.
diff = ZUR[1] - ZUR[0]
print(diff)