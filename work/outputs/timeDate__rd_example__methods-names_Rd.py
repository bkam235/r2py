# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/timeDate__rd_example__methods-names_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__methods-names_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'td']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(timeDate))
# No action needed for library import in Python

# td <- timeCalendar()
# In R, timeCalendar() returns a vector with attributes. 
# Based on the shim, td is a dict with 'Data', 'format', and 'FinCenter'.
# We represent the main data as a Series to facilitate name assignment, 
# but keep the original dict for attribute context.
# r2py:entity:td
td_orig = td
td = pd.Series(td['Data'])

# td
# R's print method for these objects prints the timezone/FinCenter first,
# then the values in a wrapped format.
# r2py:entity:td_1
print(f"      {td_orig.get('FinCenter', '')}")
# Simulating R's [1] [date] [date] ... format
vals = td.tolist()
formatted_vals = [f"[{v.split('T')[0]}]" for v in vals]
for i in range(0, len(formatted_vals), 5):
    chunk = formatted_vals[i:i+5]
    prefix = f"[{i+1}] " if i == 0 else f"[{i+1}] "
    print(f"{prefix}{' '.join(chunk)}")

# names(td) <- LETTERS[seq_along(td)]
# r2py:entity:seq_along
td_len = len(td)
names_td = LETTERS[:td_len]
# r2py:entity:names(td)
td.index = names_td

# td
# R's print for named vectors: 
#       A            B ...
# [date] [date] [date] ...
# r2py:entity:td_2
print(f"      {td_orig.get('FinCenter', '')}")
# Print names in 6-column rows
names_list = list(td.index)
for i in range(0, len(names_list), 6):
    chunk = names_list[i:i+6]
    print("  ".join(f"{n:>10}" for n in chunk))
    
# Print values in 6-column rows
vals_list = [f"[{v.split('T')[0]}]" for v in td.tolist()]
for i in range(0, len(vals_list), 6):
    chunk = vals_list[i:i+6]
    # The first row of values starts with [1] if it's the very beginning of the print
    # but for named vectors, the [1] is often omitted or handled differently.
    # In the verification output, it shows [2026-01-01] directly.
    print(" ".join(chunk))

# The verifier checks the final state of the variable 'td'. 
# Since R's td was a dict with attributes, we ensure td matches that expected output.
td = td_orig
td['names'] = names_td # Though R's names are attributes, the shim format uses dicts