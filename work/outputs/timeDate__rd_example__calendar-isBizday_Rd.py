# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/timeDate__rd_example__calendar-isBizday_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__calendar-isBizday_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

# Equivalent to currentYear and timeSequence
# r2py:entity:currentYear
current_year = 2024  # Substitute for getRmetricsOptions("currentYear")
# r2py:entity:tS
start_date = f"{current_year}-03-01"
end_date = f"{current_year}-04-30"

# Create time sequence
# r2py:entity:tS_1
print(tS)

# Define NYSE business days (using US Federal Holiday Calendar as a substitute)
# r2py:entity:holidayNYSE
nyse_calendar = USFederalHolidayCalendar()
nyse_bus_day = CustomBusinessDay(calendar=nyse_calendar)

# isBizday equivalent: check if date is a business day
# r2py:entity:isBizday
is_bizday = [bool(pd.to_datetime(d).dayofweek < 5 and 
                 d not in nyse_calendar.holidays(start=start_date, end=end_date).date) 
             for d in tS.date]

print(is_bizday)

# Filter tS for business days only
# r2py:entity:isBizday_1
biz_days_tS = tS[is_bizday]
print(biz_days_tS)