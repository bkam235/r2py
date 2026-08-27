# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__rd_example__year-week-day-narrow_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__year-week-day-narrow_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from datetime import date

# r2py:entity:x
def year_week_day(year, week, day):
    """
    Mimics clock::year_week_day by creating a date object from ISO year, week, and day of week.
    """
    # date.fromisocalendar is available in Python 3.8+
    return date.fromisocalendar(year, week, day)

# r2py:entity:calendar_narrow
def calendar_narrow(x, precision):
    """
    Mimics clock::calendar_narrow by formatting the date to the requested precision.
    """
    if precision == "week":
        # %G is ISO year, %V is ISO week
        return x.strftime("%G-W%V")
    return x

# Day precision
# x <- year_week_day(2019, 1, 5)
# r2py:entity:x
x = year_week_day(2019, 1, 5)

# Mimicking R's output for x
# r2py:entity:x_1
print("<year_week_day<Sunday><day>[1]>")
print(f'[1] "{x.strftime("%G-W%V-%u")}"')

# Narrowed to week precision
# calendar_narrow(x, "week")
# r2py:entity:calendar_narrow
res_narrow = calendar_narrow(x, "week")
print("<year_week_day<Sunday><week>[1]>")
print(f'[1] "{res_narrow}"')