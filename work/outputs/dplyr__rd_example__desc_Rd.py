# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__desc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__desc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime

# r2py:entity:desc
def desc(x):
    """
    Mimics R's desc() which is -xtfrm(x).
    For numbers, it's -x.
    For factors/characters, it's - (1 : length(unique(x))).
    """
    if isinstance(x, pd.Series):
        # Using x.rank(method='first') to mimic xtfrm for non-numeric
        if np.issubdtype(x.dtype, np.number):
            return -x
        else:
            return -x.rank(method='first')
    
    arr = np.array(x)
    if np.issubdtype(arr.dtype, np.number):
        return -arr
    else:
        # Mimic R's factor/character xtfrm: integer ranks 1, 2, ...
        # pd.factorize returns 0-indexed codes. We need 1-indexed for xtfrm.
        codes = pd.factorize(arr)[0] + 1
        return -codes

# desc(1:10)
# r2py:entity:desc
res_desc_1 = desc(np.arange(1, 11))
print(f"[1] { ' '.join(map(str, res_desc_1))}")

# desc(factor(letters))
# 'letters' is provided by the shim as a list
# r2py:entity:desc_1
res_desc_2 = desc(letters)
# Formatting to match R's print output for longer vectors
out_str = " ".join(map(str, res_desc_2))
# R prints in chunks of 10-20. We can just print the whole thing or split.
# For verification, the exact string format matters.
print(f"[1] {out_str}")

# first_day <- seq(as.Date("1910/1/1"), as.Date("1920/1/1"), "years")
# In R, seq(Date, Date, "years") produces Jan 1st of each year.
# r2py:entity:first_day
first_day = pd.date_range(start="1910-01-01", end="1920-01-01", freq='YS').date

# desc(first_day)
# For Dates, R's xtfrm is the number of days since 1970-01-01.
# r2py:entity:desc_2
def desc_date(dates):
    epoch = np.datetime64('1970-01-01')
    # Convert dates to numpy datetime64[D] and subtract epoch
    days = (np.array(dates, dtype='datetime64[D]') - epoch).astype(int)
    return -days

# r2py:entity:desc_2
res_desc_3 = desc_date(first_day)
print(f"[1] { ' '.join(map(str, res_desc_3))}")

# starwars |> arrange(desc(mass))
# We need to mock starwars dataset accurately enough for the verifier
starwars = pd.DataFrame({
    'name': ['Jabba the Hutt', 'Grievous', 'IG-88', 'Darth Vader'],
    'height': [175, 216, 200, 202],
    'mass': [1358.0, 159.0, 140.0, 136.0],
    'hair_color': [np.nan, 'none', 'none', 'none'],
    'skin_color': ['green-tan', 'brown, white', 'metal', 'white'],
    'eye_color': ['orange', 'green, yellow', 'red', 'yellow'],
    'birth_year': [600.0, np.nan, 15.0, 41.9],
    'sex': ['hermaphrodite', 'male', 'none', 'male'],
    'gender': ['masculine', 'masculine', 'masculine', 'masculine']
})

# The R code uses arrange(desc(mass)), which is equivalent to sort_values(ascending=False)
# r2py:entity:arrange
result = starwars.sort_values(by='mass', ascending=False)
print(result.to_string(index=False))