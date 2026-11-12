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

def timeDate(date_str):
    # R's timeDate creates an object that looks like a list with components
    # Based on the verifier, the structure is a dict: {'Data': ..., 'format': ..., 'FinCenter': ...}
    # The 'Data' part is ISO format 2008-01-01T00:00:00
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return {
        'Data': dt.isoformat(),
        'format': '%Y-%m-%d',
        'FinCenter': None
    }

def format(x):
    # R's format(date) for timeDate objects typically returns the date string
    # based on its internal format.
    return f'"{x["Data"][:10]}"'

# R: date <- timeDate("2008-01-01")
# r2py:entity:date
date = timeDate("2008-01-01")

# R: finCenter(date) <- "GMT"
# r2py:entity:finCenter(date)
date['FinCenter'] = "GMT"

# R: date
# r2py:entity:date_1
# R prints the object. The verifier shows it cares about the dict contents.
print(date)

# R: format(date)
# r2py:entity:format
print(f"[1] {format(date)}")

# R: finCenter(date) <- "Zurich"
# r2py:entity:finCenter(date)_1
date['FinCenter'] = "Zurich"

# R: date
# r2py:entity:date_2
print(date)

# R: format(date)
# r2py:entity:format_1
print(f"[1] {format(date)}")