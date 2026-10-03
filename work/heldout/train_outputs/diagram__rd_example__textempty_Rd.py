# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/diagram__rd_example__textempty_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__textempty_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# r2py:entity:openplotmat
# Initialize plotting area (approximating openplotmat)
# plotnine is declarative; we will build a dataframe for the loop
data_list = []
# r2py:entity:textempty
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

for i in range(1, 11):
    # runif(2) generates two random numbers between 0 and 1
    mid_coords = np.random.uniform(0, 1, 2)
    
    # Store parameters to simulate textempty loop
    data_list.append({
        'x': mid_coords[0], 
        'y': mid_coords[1], 
        'lab': letters[i-1], 
        'col': str(i),
        'cex': 2
    })

# r2py:entity:textempty_1
# Final textempty call
data_list.append({
    'x': 0.5, 
    'y': 0.5, 
    'lab': "textempty", 
    'col': "white",
    'cex': 1
})

# r2py:entity:textempty
d = pd.DataFrame(data_list)

# Translate textempty visuals using plotnine.
# Since plotnine doesn't have a native "text box" background like diagram::textempty,
# we use geom_label which provides a background box around the text.
g = (
    ggplot(d, aes(x='x', y='y', label='lab', fill='col')) 
    + geom_label(size=10) 
    + xlim(-0.1, 1.1) 
    + ylim(-0.1, 1.1) 
    + labs(title="textempty") 
    + theme_minimal()
)

print(g)