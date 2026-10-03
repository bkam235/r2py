import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# Mocking .RmetricsOptions environment
# r2py:entity:getRmetricsOptions
RmetricsOptions = {
    "currentYear": datetime.now().year,
    "myFinCenter": "GMT"
}

def getRmetricsOptions(x=None, unset=""):
    if x is None:
        return {k: v for k, v in RmetricsOptions.items()}
    return RmetricsOptions.get(x, unset)

# r2py:entity:timeCalendar
def timeCalendar(y=None, m=None, d=None, h=None, min_val=None, s=None, zone="", FinCenter=""):
    # Defaults
    if y is None:
        y = getRmetricsOptions("currentYear")
    if m is None:
        m = list(range(1, 13))
    if d is None:
        d = [1]
    if h is None:
        h = [0]
    if min_val is None:
        min_val = [0]
    if s is None:
        s = [0]
        
    if zone == "":
        zone = getRmetricsOptions("myFinCenter")
    if FinCenter == "":
        FinCenter = getRmetricsOptions("myFinCenter")
        
    # Recyling logic
    # R uses length(m), length(d), etc.
    # We ensure inputs are lists/arrays
    m_list = np.atleast_1d(m)
    d_list = np.atleast_1d(d)
    y_list = np.atleast_1d(y)
    h_list = np.atleast_1d(h)
    min_list = np.atleast_1d(min_val)
    s_list = np.atleast_1d(s)
    
    data_len = max(len(m_list), len(d_list), len(y_list), len(h_list), len(min_list), len(s_list))
    
    def recycle(arr, length):
        if len(arr) == 0: return np.full(length, np.nan)
        return np.resize(arr, length)

    m_rec = recycle(m_list, data_len)
    d_rec = recycle(d_list, data_len)
    y_rec = recycle(y_list, data_len)
    h_rec = recycle(h_list, data_len)
    min_rec = recycle(min_list, data_len)
    s_rec = recycle(s_list, data_len)
    
    tz = pytz.timezone(FinCenter if FinCenter else zone)
    results = []
    for i in range(data_len):
        # Create naive datetime then localize
        dt_naive = datetime(int(y_rec[i]), int(m_rec[i]), int(d_rec[i]), 
                            int(h_rec[i]), int(min_rec[i]), int(s_rec[i]))
        dt_localized = tz.localize(dt_naive)
        results.append(dt_localized)
    
    # To match R's output printing style (just the dates/times)
    # In a real scenario, timeDate returns a specific class, but for stdout:
    return results

# Current Year:
# r2py:entity:getRmetricsOptions
res_year = getRmetricsOptions("currentYear")
print(f"currentYear \n{res_year}")

# 12 months of current year
# r2py:entity:timeCalendar
res_cal = timeCalendar()
print(f"GMT\n{['[' + d.strftime('%Y-%m-%d') + ']' for d in res_cal]}")

# timeCalendar(m = c(9, 1, 8, 2), d = c(28, 15, 30, 9), y = c(1989, 2001, 2004, 1990), FinCenter = "GMT")
# r2py:entity:timeCalendar_1
res_cal1 = timeCalendar(m=[9, 1, 8, 2], d=[28, 15, 30, 9], y=[1989, 2001, 2004, 1990], FinCenter="GMT")
print(f"GMT\n{['[' + d.strftime('%Y-%m-%d') + ']' for d in res_cal1]}")

# timeCalendar(m = c(9, 1, 8, 2), d = c(28, 15, 30, 9), y = c(1989, 2001, 2004, 1990), FinCenter = "Europe/Zurich")
# r2py:entity:timeCalendar_2
res_cal2 = timeCalendar(m=[9, 1, 8, 2], d=[28, 15, 30, 9], y=[1989, 2001, 2004, 1990], FinCenter="Europe/Zurich")
print(f"Europe/Zurich\n{['[' + d.strftime('%Y-%m-%d %H:%M:%S') + ']' for d in res_cal2]}")

# timeCalendar(h = c(9, 14), min = c(15, 23))
# r2py:entity:timeCalendar_3
res_cal3 = timeCalendar(h=[9, 14], min_val=[15, 23])
print(f"GMT\n{['[' + d.strftime('%Y-%m-%d %H:%M:%S') + ']' for d in res_cal3]}")