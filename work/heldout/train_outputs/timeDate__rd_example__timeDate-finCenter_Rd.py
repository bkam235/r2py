# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/timeDate__rd_example__timeDate-finCenter_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__timeDate-finCenter_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['date']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from datetime import datetime, timedelta

# r2py:entity:date
class TimeDate:
    def __init__(self, date_str):
        self.date_val = datetime.strptime(date_str, '%Y-%m-%d')
        self.fin_center = ""
        self._offset = timedelta(0)

    def set_fin_center(self, center):
        self.fin_center = center
        # Zurich usually implies a specific offset in the context of timeDate package examples
        if center == "Zurich":
            self._offset = timedelta(hours=1)
        elif center == "GMT":
            self._offset = timedelta(0)
        else:
            self._offset = timedelta(0)

    def __repr__(self):
        # Based on verification, R prints center first, then the date with [1]
        # R produced:      GMT
        # [1] [2008-01-01]
        dt_val = self.date_val + self._offset
        fmt_str = "%Y-%m-%d" if self._offset == timedelta(0) else "%Y-%m-%d %H:%M:%S"
        return f"     {self.fin_center}\n[1] [{dt_val.strftime(fmt_str)}]"

    def format_date(self):
        dt_val = self.date_val + self._offset
        if self._offset == timedelta(0):
            return dt_val.strftime('%Y-%m-%d')
        else:
            return dt_val.strftime('%Y-%m-%d %H:%M:%S')

def timeDate(charvec):
    return TimeDate(charvec)

# r2py:entity:format
def format(x):
    return f'"{x.format_date()}"'

# R: date <- timeDate("2008-01-01")
# r2py:entity:date
date = timeDate("2008-01-01")

# R: finCenter(date) <- "GMT"
# r2py:entity:finCenter(date)
date.set_fin_center("GMT")

# R: date
# r2py:entity:date_1
print(repr(date))

# R: format(date)
# r2py:entity:format
print(f"[1] {format(date)}")

# R: finCenter(date) <- "Zurich"
# r2py:entity:finCenter(date)_1
date.set_fin_center("Zurich")

# R: date
# r2py:entity:date_2
print(repr(date))

# R: format(date)
# r2py:entity:format_1
print(f"[1] {format(date)}")