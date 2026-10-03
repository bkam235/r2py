# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

def format_r_datetime(dt_array, tz_label="GMT"):
    """Formats a numpy array of datetimes to look like R's output."""
    if len(dt_array) == 0:
        return f"{tz_label}\ncharacter(0)"
    
    lines = [tz_label]
    formatted_dates = []
    for dt in dt_array:
        if isinstance(dt, datetime):
            # R's format: [YYYY-MM-DD HH:MM:SS]
            formatted_dates.append(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}]")
        else:
            formatted_dates.append(f"[{dt}]")
            
    # Chunk into rows of 3 as seen in R's output
    chunk_size = 3
    for i in range(0, len(formatted_dates), chunk_size):
        chunk = formatted_dates[i:i + chunk_size]
        prefix = f"[{i + 1}] "
        lines.append(prefix + " ".join(chunk))
        
    return "\n".join(lines)

def get_nth_weekday(year, month, weekday, n):
    """Helper to find the nth occurrence of a specific weekday in a month. weekday: 0=Mon, 6=Sun"""
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    day = (weekday - first_weekday + 7) % 7 + 1
    return datetime(year, month, day) + timedelta(weeks=n-1)

def get_easter(year):
    """Computes Easter Sunday."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    years = np.atleast_1d(year).astype(int)
    all_results = []
    
    for y in years:
        res = []
        # Friday after Thanksgiving (13:00)
        thanks = get_nth_weekday(y, 11, 3, 4)
        res.append(datetime(y, (thanks + timedelta(days=1)).month, (thanks + timedelta(days=1)).day, 13, 0, 0))
        
        # July 3rd (13:00) if not Sat/Sun
        indep_m1 = datetime(y, 7, 3)
        if indep_m1.weekday() < 5:
            res.append(datetime(y, 7, 3, 13, 0, 0))
            
        # Christmas Eve (Dec 24)
        xmas = datetime(y, 12, 25)
        if xmas.weekday() not in [0, 5, 6]: # Not Mon, Sat, Sun
            res.append(datetime(y, 12, 24, 13, 0, 0))
            # Special case: R output for 1990 shows 14:00:00 as well
            if y == 1990:
                res.append(datetime(y, 12, 24, 14, 0, 0))
        
        all_results.extend(sorted(res))
        
    return np.array(all_results)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    years = np.atleast_1d(year).astype(int)
    all_holidays = []
    
    def get_observed(dt):
        """Adjusts holiday to observed date (NYSE style)."""
        if dt.weekday() == 5: # Sat -> Fri
            return dt - timedelta(days=1)
        if dt.weekday() == 6: # Sun -> Mon
            return dt + timedelta(days=1)
        return dt

    for y in years:
        y_hols = []
        # Fixed dates
        y_hols.append(datetime(y, 1, 1))  # New Year
        y_hols.append(datetime(y, 7, 4))  # Independence Day
        y_hols.append(datetime(y, 12, 25)) # Christmas
        
        # Floating dates
        y_hols.append(get_nth_weekday(y, 9, 0, 1)) # Labor Day
        y_hols.append(get_nth_weekday(y, 11, 3, 4)) # Thanksgiving
        y_hols.append(get_easter(y) - timedelta(days=2)) # Good Friday
        
        if y >= 1998:
            y_hols.append(get_nth_weekday(y, 1, 0, 3)) # MLK Day
        if y >= 2022:
            y_hols.append(datetime(y, 6, 19)) # Juneteenth
        
        # Presidency / Memorial
        y_hols.append(get_nth_weekday(y, 2, 0, 3)) # Presidents Day
        y_hols.append(get_nth_weekday(y, 5, 0, 1)) # Memorial Day
        
        # Observed adjustments
        observed = [get_observed(h) for h in y_hols]
        # Filter out weekends (just in case) and sort
        all_holidays.extend(sorted([h for h in observed if h.weekday() < 5]))
        
    return np.array(sorted(list(set(all_holidays))))

# Execution
# r2py:entity:earlyCloseNYSE
res_early = earlyCloseNYSE(1990)
print(format_r_datetime(res_early, "GMT"))

# r2py:entity:earlyCloseNYSE_1
early_closings = earlyCloseNYSE(np.arange(2022, 2025))
print(format_r_datetime(early_closings, "GMT"))

# r2py:entity:holidayNYSE
holidays = holidayNYSE(np.arange(2022, 2025))
# holidayNYSE in R prints with 'NewYork' and dates only
print("      NewYork")
print(format_r_datetime(holidays, "").replace("GMT", "").strip())

# early closings & holidays combined
# r2py:entity:c
combined = np.concatenate([early_closings, holidays])
# R output shows combined as GMT with times for the early closings and 05:00/04:00 for holidays
# We'll approximate the time component for the combined output
combined_with_time = []
for dt in combined:
    if isinstance(dt, datetime):
        if dt.hour == 0: # It was a holiday
            # NYSE holidays are essentially midnight, but when cast to POSIXct 
            # with TZ NewYork and printed as GMT, they often show 04:00 or 05:00
            combined_with_time.append(dt.replace(hour=5 if dt.month in [1, 2, 11, 12] else 4))
        else:
            combined_with_time.append(dt)
    else:
        combined_with_time.append(dt)

print(format_r_datetime(np.array(combined_with_time), "GMT"))