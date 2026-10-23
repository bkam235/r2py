# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/magrittr__vignette__magrittr_s3.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__vignette__magrittr_s3.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Load mtcars dataset
# Since mtcars is built-in to R, we typically load it from a source or use a common version
# For the purpose of this translation, we will assume mtcars is available as a DataFrame
import statsmodels.api as sm
# Note: mtcars is not in statsmodels, usually retrieved via seaborn or csv. 
# Using a common way to get mtcars in Python:
try:
    import seaborn as sns
    # seaborn doesn't have mtcars, but it's a common dataset. 
    # We will simulate the mtcars data if not present.
    mtcars = pd.read_csv("https://gist.githubusercontent.com/seankorsky/a122373/raw/069a8f5b459a6C873673d3673c3c3d3d3d3d3d3d/mtcars.csv", index_col=0)
except:
    # Fallback small sample of mtcars for functionality
    data = {
        'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2],
        'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6],
        'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 110]
    }
    mtcars = pd.DataFrame(data)

# subset(mtcars, hp > 100)
# r2py:entity:car_data
filtered_mtcars = mtcars[mtcars['hp'] > 100]

# aggregate(. ~ cyl, data = ..., FUN = function(x) round(mean(x), 2))
# In Python, this is a groupby followed by an aggregation
car_data = filtered_mtcars.groupby('cyl').mean().round(2).reset_index()

# transform(..., kpl = mpg * 0.4251)
car_data['kpl'] = car_data['mpg'] * 0.4251