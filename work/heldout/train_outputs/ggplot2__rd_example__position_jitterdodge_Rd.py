# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__position_jitterdodge_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['diamonds', 'dsub']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Convert shim data to pandas DataFrames
diamonds = pd.DataFrame(diamonds)

# Setup seed
# r2py:entity:set.seed
np.random.seed(596)

# R: dsub <- diamonds[sample(nrow(diamonds), 1000), ]
# We use the shim's dsub if it exists to ensure exact match, 
# otherwise we simulate R's sample (which is sampling without replacement).
# r2py:entity:dsub
if 'dsub' in globals() and isinstance(dsub, (dict, pd.DataFrame)):
    dsub = pd.DataFrame(dsub)
else:
# r2py:entity:sample
    # r2py:entity:sample
    # To match R's sample(nrow(diamonds), 1000), we sample indices
    indices = np.random.choice(len(diamonds), 1000, replace=False)
    dsub = diamonds.iloc[indices].reset_index(drop=True)

# Plotting
# r2py:entity:ggplot
p = (
    ggplot(dsub, aes(x='cut', y='carat', fill='clarity'))
# r2py:entity:geom_boxplot
    # r2py:entity:geom_boxplot
    + geom_boxplot(outlier_size=0)
# r2py:entity:geom_point
    # r2py:entity:geom_point
    + geom_point(shape='o', position=position_jitterdodge())
)

# Render plot
print(p)