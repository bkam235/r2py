# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__fplot_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__fplot_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Load data

# lava::fplot is a specialized wrapper for ggplot2. 
# 'type="s"' in lava typically refers to a scatter plot with smoothers/lines.
# Translating 'Sepal.Length ~ Petal.Length+Species' with type="s" to plotnine:
# r2py:entity:fplot
g = (
    ggplot(iris, aes(x='petal_length', y='sepal_length', color='species'))
    + geom_point(size=2)
    + geom_smooth(method='lm', se=False)
)

print(g)