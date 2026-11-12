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

from datetime import datetime

class TimeDateObj:
    def __init__(self, date_str):
        self.date_val = date_str
        self.fin_center = None

    def __repr__(self):
        # R's timeDate objects print the financial center on one line 
        # and the date (with [1]) on the next.
        center = self.fin_center if self.fin_center else "UTC"
        return f"{center}\n[1] {self.date_val}"

def timeDate(charvec):
    return TimeDateObj(charvec)

def format(x):
    # format(date) in timeDate package returns the date string
    return f'"{x.date_val}"'

# R: date <- timeDate("2008-01-01")
# r2py:entity:date
date = timeDate("2008-01-01")

# R: finCenter(date) <- "GMT"
# r2py:entity:finCenter(date)
date.fin_center = "GMT"

# R: date
# r2py:entity:date_1
print(repr(date))

# R: format(date)
# r2py:entity:format
print(f"[1] {format(date)}")

# R: finCenter(date) <- "Zurich"
# r2py:entity:finCenter(date)_1
date.fin_center = "Zurich"

# R: date
# r2py:entity:date_2
print(repr(date))

# R: format(date)
# r2py:entity:format_1
print(f"[1] {format(date)}")