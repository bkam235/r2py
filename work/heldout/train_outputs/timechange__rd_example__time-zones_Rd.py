# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# Helper function to mimic time_at_tz
# r2py:entity:time_at_tz
def time_at_tz(dt, tz_name):
    return dt.astimezone(pytz.timezone(tz_name))

# Helper function to mimic time_force_tz
# r2py:entity:time_force_tz
def time_force_tz(dt, tz_name, roll=None, roll_dst=None, tzout=None):
    if isinstance(dt, (list, pd.Series, np.ndarray)):
        results = []
        for i, val in enumerate(dt):
            # Handle vector tz inputs
            current_tz = tz_name[i] if isinstance(tz_name, (list, np.ndarray)) else tz_name
            # Handle vector roll_dst inputs
            current_roll = roll_dst[i] if isinstance(roll_dst, (list, np.ndarray)) else roll
            
            # Force timezone (strip existing tz and attach new one)
            naive = val.replace(tzinfo=None)
            try:
                localized = pytz.timezone(current_tz).localize(naive, is_dst=None)
            except pytz.AmbiguousTimeError:
                # Handle roll logic for ambiguous times (DST transition)
                if current_roll == "pre": localized = pytz.timezone(current_tz).localize(naive, is_dst=True)
                elif current_roll == "post": localized = pytz.timezone(current_tz).localize(naive, is_dst=False)
                else: localized = pytz.timezone(current_tz).localize(naive, is_dst=None)
            except pytz.NonExistentTimeError:
                # Handle roll logic for non-existent times (Spring forward)
                if current_roll == "boundary": localized = pytz.timezone(current_tz).localize(naive, is_dst=True) # approximation
                elif current_roll == "post": localized = pytz.timezone(current_tz).localize(naive, is_dst=False) # approximation
                elif current_roll == "pre": localized = pytz.timezone(current_tz).localize(naive, is_dst=True) # approximation
                elif current_roll == "NA": localized = pd.NaT
                else: localized = pytz.timezone(current_tz).localize(naive, is_dst=None)
            
            if tzout:
                localized = localized.astimezone(pytz.timezone(tzout))
            results.append(localized)
        return pd.Series(results)
    else:
        naive = dt.replace(tzinfo=None)
        try:
            localized = pytz.timezone(tz_name).localize(naive, is_dst=None)
        except (pytz.AmbiguousTimeError, pytz.NonExistentTimeError):
            # Simple roll handling for scalar
            if roll == "boundary": localized = pytz.timezone(tz_name).localize(naive, is_dst=True)
            elif roll == "post": localized = pytz.timezone(tz_name).localize(naive, is_dst=False)
            elif roll == "pre": localized = pytz.timezone(tz_name).localize(naive, is_dst=True)
            elif roll == "NA": return pd.NaT
            else: localized = pytz.timezone(tz_name).localize(naive, is_dst=None)
        
        if tzout:
            localized = localized.astimezone(pytz.timezone(tzout))
        return localized

# Helper function to mimic time_clock_at_tz
# r2py:entity:time_clock_at_tz
def time_clock_at_tz(dt, units="secs", tz=None):
    if isinstance(dt, (list, pd.Series, np.ndarray)):
        results = []
        for val in dt:
            target_tz = tz if not isinstance(tz, (list, np.ndarray)) else tz[0] # simplified
            localized = val.astimezone(pytz.timezone(target_tz)) if tz else val
            if units == "secs": results.append(localized.time())
            elif units == "hours": results.append(localized.hour)
            else: results.append(localized.time())
        return pd.Series(results)
    else:
        target_tz = tz if not isinstance(tz, (list, np.ndarray)) else tz[0]
        localized = dt.astimezone(pytz.timezone(target_tz)) if tz else dt
        if units == "secs": return localized.time()
        elif units == "hours": return localized.hour
        return localized.time()

# r2py:entity:x
x = pd.to_datetime("2009-08-07 00:00:00").tz_localize("America/New_York")
# r2py:entity:time_at_tz
print(time_at_tz(x, "UTC"))
# r2py:entity:time_force_tz
print(time_force_tz(x, "UTC"))
# r2py:entity:time_force_tz_1
print(time_force_tz(x, "Europe/Amsterdam"))

# r2py:entity:y
y = pd.to_datetime("2010-03-14 02:05:05").tz_localize("UTC")
# r2py:entity:time_force_tz_2
print(time_force_tz(y, "America/New_York", roll="boundary"))
# r2py:entity:time_force_tz_3
print(time_force_tz(y, "America/New_York", roll="post"))
# r2py:entity:time_force_tz_4
print(time_force_tz(y, "America/New_York", roll="pre"))
# r2py:entity:time_force_tz_5
print(time_force_tz(y, "America/New_York", roll="NA"))

# r2py:entity:y_1
y = pd.to_datetime(["2010-03-14 02:05:05 UTC", "2014-11-02 01:35:00"]).tz_localize("UTC")
# r2py:entity:time_force_tz_6
print(time_force_tz(y, "America/New_York", roll_dst=["NA", "pre"]))
# r2py:entity:time_force_tz_7
print(time_force_tz(y, "America/New_York", roll_dst=["boundary", "post"]))

# r2py:entity:x_1
x = pd.to_datetime(["2009-08-07 00:00:01", "2009-08-07 01:02:03"]).tz_localize("UTC")
# r2py:entity:time_force_tz_8
print(time_force_tz(x, tz=["America/New_York", "Europe/Amsterdam"]))
# r2py:entity:time_force_tz_9
print(time_force_tz(x, tz=["America/New_York", "Europe/Amsterdam"], tzout="America/New_York"))

# r2py:entity:x_2
x = pd.to_datetime("2009-08-07 00:00:01").tz_localize("UTC")
# r2py:entity:time_force_tz_10
print(time_force_tz(x, tz=["America/New_York", "Europe/Amsterdam"]))

# r2py:entity:x_3
x = pd.to_datetime(["2009-08-07 01:02:03", "2009-08-07 10:20:30"]).tz_localize("UTC")
# r2py:entity:time_clock_at_tz
print(time_clock_at_tz(x, units="secs"))
# r2py:entity:time_clock_at_tz_1
print(time_clock_at_tz(x, units="hours"))
# r2py:entity:time_clock_at_tz_2
print(time_clock_at_tz(x, tz="Europe/Amsterdam"))

# r2py:entity:x_4
x = pd.to_datetime("2009-08-07 01:02:03").tz_localize("UTC")
# r2py:entity:time_clock_at_tz_3
print(time_clock_at_tz(x, tz=["America/New_York", "Europe/Amsterdam", "Asia/Shanghai"], units="hours"))