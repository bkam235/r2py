import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Union, List, Callable, Any

# r2py:entity:Easter_1
def Easter(year, shift=0):
    years = np.atleast_1d(year)
    # Computus algorithm for Gregorian Easter
    a = years % 19
    b = years // 100
    c = years % 100
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
    
    dates = [datetime(int(y), int(m), int(d)) for y, m, d in zip(years, month, day)]
    shifted_dates = [d + timedelta(days=shift) for d in dates]
    
    res = [d.strftime('%Y-%m-%d') for d in shifted_dates]
    return np.array(res) if np.ndim(year) > 0 else res[0]

# r2py:entity:GoodFriday
def GoodFriday(year, value="timeDate", na_drop=True):
    return Easter(year, -2)

def ChristmasDay(year, value="timeDate", na_drop=True):
    years = np.atleast_1d(year)
    res = [f"{int(y)}-12-25" for y in years]
    return np.array(res) if np.ndim(year) > 0 else res[0]

def GBEarlyMayBankHoliday(year, value="timeDate", na_drop=True):
    years = np.atleast_1d(year)
    res = []
    for y in years:
        if y < 1978:
            res.append(np.nan if not na_drop else None)
            continue
        
        if y in [1995, 2020]:
            res.append(f"{int(y)}-05-08")
        else:
            # First Monday of May
            d = datetime(int(y), 5, 1)
            offset = (0 - d.weekday()) % 7
            res.append((d + timedelta(days=offset)).strftime('%Y-%m-%d'))
            
    return np.array(res) if np.ndim(year) > 0 else res[0]

def _get_holiday_func(name):
    mapping = {
        "Easter": Easter,
        "GoodFriday": GoodFriday,
        "ChristmasDay": ChristmasDay,
        "GBEarlyMayBankHoliday": GBEarlyMayBankHoliday
    }
    return mapping.get(name, Easter)

# r2py:entity:holiday_21
def holiday(year=None, Holiday="Easter", names=False):
    if year is None:
        year = datetime.now().year
    
    years = np.atleast_1d(year)
    
    # Mimic R's substitute/all.names for naming
    # This is a simplified version of the R logic
    if isinstance(Holiday, str):
        holiday_funcs = [_get_holiday_func(Holiday)]
        holiday_names = [Holiday]
    elif callable(Holiday):
        holiday_funcs = [Holiday]
        holiday_names = [Holiday.__name__]
    elif isinstance(Holiday, (list, np.ndarray)):
        holiday_funcs = [_get_holiday_func(h) if isinstance(h, str) else h for h in Holiday]
        holiday_names = [h if isinstance(h, str) else (h.__name__ if callable(h) else f"h{i+1}") 
                        for i, h in enumerate(Holiday)]
    else:
        holiday_funcs = [_get_holiday_func(str(Holiday))]
        holiday_names = [str(Holiday)]

    all_dates = []
    all_labels = []
    
    for func, name in zip(holiday_funcs, holiday_names):
        vals = func(years)
        # Ensure vals is iterable
        if not isinstance(vals, (list, np.ndarray)):
            vals = [vals]
        
        all_dates.extend(vals)
        if names:
            all_labels.extend([name] * len(vals))

    if names:
        return pd.Series(all_dates, index=all_labels)
    return np.array(all_dates)

# --- Example Execution ---

# Dates for GoodFriday from 2000 until 2005:
# r2py:entity:holiday
print(holiday(np.arange(2000, 2006), "GoodFriday"))
# r2py:entity:holiday_1
print(holiday(np.arange(2000, 2006), GoodFriday))

# Good Friday and Easter
# r2py:entity:holiday_2
print(holiday(np.arange(2000, 2006), ["GoodFriday", "Easter"]))
# r2py:entity:holiday_3
print(holiday(np.arange(2000, 2006), [GoodFriday, Easter]))

# Easter
# r2py:entity:Easter
print(Easter(np.arange(2000, 2006)))

# GoodFriday
# r2py:entity:GoodFriday
print(GoodFriday(np.arange(2000, 2006)))
# r2py:entity:Easter_1
print(Easter(np.arange(2000, 2006), -2))

# Named holidays
# r2py:entity:holiday_4
print(holiday(2025, Holiday="Easter", names=True))
# r2py:entity:holiday_5
print(holiday(2025, Holiday=Easter, names=True))

# Corrected range from 2024:2006 to 2024:2025
# r2py:entity:holiday_6
print(holiday(np.arange(2024, 2026), Holiday="Easter", names=True))
# r2py:entity:holiday_7
print(holiday(np.arange(2024, 2026), Holiday=Easter, names=True))

# r2py:entity:holiday_8
print(holiday(np.arange(2024, 2026), Holiday=["Easter", "ChristmasDay"], names=True))
# r2py:entity:holiday_9
print(holiday(np.arange(2024, 2026), Holiday=[Easter, ChristmasDay], names=True))

# r2py:entity:ho1
ho1 = "Easter"
# r2py:entity:holiday_10
print(holiday(2025, Holiday=ho1, names=True))

# r2py:entity:ho1a
ho1a = Easter
# r2py:entity:ho3
ho3 = [Easter, GBEarlyMayBankHoliday]
# r2py:entity:holiday_11
print(holiday(2025, Holiday=ho1a, names=True))

# r2py:entity:ho1b
ho1b = "Easter"
# r2py:entity:ho3b
ho3b = ["Easter", "GBEarlyMayBankHoliday"]
# r2py:entity:holiday_12
print(holiday(2025, Holiday=ho1b, names=True))
# r2py:entity:holiday_13
print(holiday(2025, Holiday=ho3b, names=True))
# r2py:entity:holiday_14
print(holiday(np.arange(2024, 2026), Holiday=ho3b, names=True))

# r2py:entity:ho2
ho2 = ["Easter", "GBEarlyMayBankHoliday"]
# r2py:entity:holiday_15
print(holiday(2025, Holiday=ho2, names=True))
# r2py:entity:holiday_16
print(holiday(Holiday=[Easter, GBEarlyMayBankHoliday], names=True))
# r2py:entity:holiday_17
print(holiday(np.arange(2024, 2026), Holiday=ho2, names=True))
# r2py:entity:holiday_18
print(holiday(np.arange(2024, 2026), Holiday=ho1a, names=True))
# r2py:entity:holiday_19
print(holiday(np.arange(2024, 2026), Holiday=ho1, names=True))

# r2py:entity:holiday_20
print(holiday(np.arange(2024, 2026), Holiday=["Easter"], names=True))
# r2py:entity:holiday_21
print(holiday(np.arange(2024, 2026), Holiday=[Easter], names=True))