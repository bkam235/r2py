# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/diagram__rd_example__textround_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__textround_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# r2py:entity:openplotmat
# Initialize plotting area (approximating openplotmat)
# plotnine is declarative; we will build a dataframe for the loop
data_list = []
# r2py:entity:textround
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

for i in range(1, 11):
    # runif(2) generates two random numbers between 0 and 1
    mid_x, mid_y = np.random.uniform(0, 1, 2)
    
    # Store parameters to simulate the loop's effect
    data_list.append({
        'x': mid_x, 
        'y': mid_y, 
        'lab': letters[i-1], 
        'col': str(i)
    })

d = pd.DataFrame(data_list)

# r2py:entity:textround
# Translate textround visuals using plotnine
# radx and rady are approximated by using geom_text and a custom point/size logic
# since plotnine doesn't have a native "rounded text box" like diagram::textround,
# we use geom_text with a background shape or simply plot the text.
g = (
    ggplot(d, aes(x='x', y='y', color='col', label='lab')) 
    + geom_text(size=10) 
    + xlim(-0.1, 1.1) 
    + ylim(-0.1, 1.1) 
    + labs(title="textround") 
    + theme_minimal()
)

print(g)