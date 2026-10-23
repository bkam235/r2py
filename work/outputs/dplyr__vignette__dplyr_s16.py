# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__vignette__dplyr_s16.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__vignette__dplyr_s16.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(dplyr))
# In Python, pandas is the equivalent for dplyr.

# load data from shim
df = pd.DataFrame(starwars)

# mutate(height_m = height / 100, BMI = mass / (height_m^2))
# r2py:entity:mutate
df['height_m'] = df['height'] / 100
df['BMI'] = df['mass'] / (df['height_m']**2)

# select(BMI, everything())
# r2py:entity:select
cols = ['BMI'] + [col for col in df.columns if col != 'BMI']
df = df[cols]

print(df)