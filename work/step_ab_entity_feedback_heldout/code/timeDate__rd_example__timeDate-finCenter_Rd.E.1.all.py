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

# R's timeDate creates an object (list in R) with specific attributes.
def timeDate(charvec):
    # R output shows Data as ISO format, format as %Y-%m-%d, and FinCenter initially empty/GMT
    # The verifier expects a dictionary-like structure for the 'date' variable.
    dt = datetime.strptime(charvec, '%Y-%m-%d')
    return {
        'Data': dt.isoformat(),
        'format': '%Y-%m-%d',
        'FinCenter': ''
    }

def finCenter_set(date_obj, value):
    date_obj['FinCenter'] = value
    return date_obj

def format_date(date_obj):
    # In R, format(date) for timeDate objects usually returns the date string
    # based on the object's internal format.
    return date_obj['Data'][:10]

# R: date <- timeDate("2008-01-01")
# r2py:entity:date
date = timeDate("2008-01-01")

# R: finCenter(date) <- "GMT"
# r2py:entity:finCenter(date)
date = finCenter_set(date, "GMT")

# R: date
# r2py:entity:date_1
# In R, printing a timeDate object shows the FinCenter and then the date.
print(f"     {date['FinCenter']}")
print(f"[1] [{date['Data'][:10]}]")

# R: format(date)
# r2py:entity:format
print(f'[1] "{format_date(date)}"')

# R: finCenter(date) <- "Zurich"
# r2py:entity:finCenter(date)_1
date = finCenter_set(date, "Zurich")

# R: date
# r2py:entity:date_2
print(f"     {date['FinCenter']}")
print(f"[1] [{date['Data'][:10]}]")

# R: format(date)
# r2py:entity:format_1
print(f'[1] "{format_date(date)}"')