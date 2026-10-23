# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/diagram__rd_example__textdiamond_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__textdiamond_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Since 'diagram' is a specialized R package for flowcharts/diagrams 
# and does not have a direct 1:1 library equivalent in Python, 
# we use matplotlib to simulate the "textdiamond" behavior.

np.random.seed(42)

# Data generation
data = pd.DataFrame({
    'x': np.random.uniform(0, 1, 10),
    'y': np.random.uniform(0, 1, 10),
    'label': [chr(65 + i) for i in range(10)],
    'color': range(1, 11),
    'angle': np.random.uniform(0, 360, 10)
})

# r2py:entity:openplotmat
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_title("textdiamond")
ax.axis('off')

# r2py:entity:textdiamond
for idx, row in data.iterrows():
    # Create diamond shape using an Ellipse
    diamond = Ellipse(
        xy=(row['x'], row['y']),
        width=0.2,  # radx * 2
        height=0.1, # rady * 2
        angle=row['angle'],
        edgecolor=plt.cm.tab10(row['color']/10),
        facecolor='none',
        linewidth=2
    )
    ax.add_patch(diamond)
    
    # Add text label
    ax.text(
        row['x'], row['y'], 
        row['label'], 
        ha='center', va='center', 
        fontsize=14, 
        rotation=row['angle']
    )

plt.show()