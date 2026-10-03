# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/diagram__rd_example__textmulti_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__textmulti_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# Setting up the canvas to mimic openplotmat
# r2py:entity:openplotmat
plt.figure(figsize=(6, 6))
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
plt.title("textmulti")
plt.axis('off')

# R's LETTERS[1:10]

# Loop to simulate textmulti logic
# r2py:entity:textmulti
for i in range(1, 11):
    # mid = runif(2)
    mid = np.random.uniform(0, 1, 2)
    
    # nr = trunc(i/1.5)+3
    nr = int(i / 1.5) + 3
    
    # Approximate textmulti: 
    # Since textmulti draws a circle of labels around a center point,
    # we calculate coordinates for nr labels distributed around the point mid.
    # radx = 0.1, rady = 0.1
    radx = 0.1
    rady = 0.1
    
    angles = np.linspace(0, 2 * np.pi, nr, endpoint=False)
    for j in range(nr):
        x = mid[0] + radx * np.cos(angles[j])
        y = mid[1] + rady * np.sin(angles[j])
        
        # col = i, lab = LETTERS[i], cex = 2
        plt.text(x, y, LETTERS[i-1], 
                 color=plt.cm.tab10(i-1), 
                 fontsize=20, 
                 ha='center', va='center')

plt.show()