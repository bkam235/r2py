# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ggplot2__rd_example__geom_bin_2d_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__geom_bin_2d_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['diamonds']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from plotnine import ggplot, aes, geom_bin_2d, xlim, ylim
from plotnine.data import diamonds

# r2py:entity:d
d = (
# r2py:entity:ggplot
    ggplot(diamonds, aes(x='x', y='y')) 
# r2py:entity:xlim
    + xlim(4, 10) 
# r2py:entity:ylim
    + ylim(4, 10)
)

# r2py:entity:geom_bin_2d
p1 = d + geom_bin_2d()
print(p1)

# You can control the size of the bins by specifying the number of
# bins in each direction:
# r2py:entity:geom_bin_2d_1
p2 = d + geom_bin_2d(bins=10)
print(p2)

# r2py:entity:geom_bin_2d_2
p3 = d + geom_bin_2d(bins={'x': 30, 'y': 10})
print(p3)

# Or by specifying the width of the bins
# r2py:entity:geom_bin_2d_3
p4 = d + geom_bin_2d(binwidth=[0.1, 0.1])
print(p4)