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

# r2py:entity:date
def timeDate(charvec):
    # R's timeDate object is represented as a list/dict with these specific components
    return {
        'Data': f"{charvec}T00:00:00",
        'format': '%Y-%m-%d',
        'FinCenter': None
    }

def finCenter(date_obj):
    # This is a helper to provide the reference to the object for the assignment shim
    return date_obj

# Since R uses finCenter(date) <- "GMT", and Python doesn't support overloading 
# assignment to function calls, we implement the assignment logic directly.
def set_finCenter(date_obj, value):
    date_obj['FinCenter'] = value

# r2py:entity:format
def format(x):
    # In the context of timeDate, format(date) returns the date string based on the internal format
    # Since Data is ISO 8601, we just take the first 10 chars for %Y-%m-%d
    return x['Data'][:10]

# R: date <- timeDate("2008-01-01")
# r2py:entity:date
date = timeDate("2008-01-01")

# R: finCenter(date) <- "GMT"
# r2py:entity:finCenter(date)
set_finCenter(date, "GMT")

# R: date
# r2py:entity:date_1
# For the print output to match R's console representation
print(f"      {date['FinCenter']}")
print(f"[1] [{date['Data'][:10]}]")

# R: format(date)
# r2py:entity:format
print(f'[1] "{format(date)}"')

# R: finCenter(date) <- "Zurich"
# r2py:entity:finCenter(date)_1
set_finCenter(date, "Zurich")

# R: date
# r2py:entity:date_2
print(f"      {date['FinCenter']}")
print(f"[1] [{date['Data'][:10]}]")

# R: format(date)
# r2py:entity:format_1
print(f'[1] "{format(date)}"')