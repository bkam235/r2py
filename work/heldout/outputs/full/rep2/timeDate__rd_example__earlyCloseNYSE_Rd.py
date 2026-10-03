# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas_market_calendars as mcal

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    """
    Returns early closing dates for the NYSE.
    Uses pandas_market_calendars for accurate exchange scheduling.
    """
    if isinstance(year, int):
        years = [year]
    else:
        years = year

    nyse = mcal.get_calendar('NYSE')
    all_early_closes = []
    
    for y in years:
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31)
        schedule = nyse.schedule(start_date=start, end_date=end)
        # In pandas_market_calendars, early close is indicated by the 'market_close' time
        # We filter for days where the market closes earlier than the standard 16:00
        early_closes = schedule[schedule['market_close'].dt.time < pd.to_datetime('16:00').time()]
        all_early_closes.extend(early_closes.index.strftime('%Y-%m-%d').tolist())
    
    return sorted(list(set(all_early_closes)))

# r2py:entity:holidayNYSE
def holidayNYSE(year):
    """
    Returns holiday dates for the NYSE.
    """
    if isinstance(year, int):
        years = [year]
    else:
        years = year

    nyse = mcal.get_calendar('NYSE')
    all_holidays = []
    
    for y in years:
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31)
        # Holidays are days that are NOT in the schedule but fall on weekdays,
        # or specifically marked as holidays.
        # A simpler way: get all business days and subtract from the full calendar,
        # or use the calendar's built-in holiday logic.
        schedule = nyse.schedule(start_date=start, end_date=end)
        # For NYSE, we can identify holidays by finding weekdays not in the schedule
        full_range = pd.date_range(start=start, end=end, freq='B')
        holidays = full_range[~full_range.isin(schedule.index)]
        all_holidays.extend(holidays.strftime('%Y-%m-%d').tolist())
        
    return sorted(list(set(all_holidays)))

# Translation of the main script execution
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# early closings for 2022 to 2024
# r2py:entity:earlyCloseNYSE_1
years_range = list(range(2022, 2025))
early_closes = earlyCloseNYSE(years_range)
print(early_closes)

# holidays for 2022 to 2024
# r2py:entity:holidayNYSE
holidays = holidayNYSE(years_range)
print(holidays)

# early closings & holidays combined
# r2py:entity:c
combined = early_closes + holidays
print(combined)