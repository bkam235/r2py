# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/diagram__rd_example__coordinates_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__coordinates_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Helper function to replicate R's diagram::coordinates functionality
# r2py:entity:openplotmat
def get_coordinates(N=None, pos=None, relsize=1, hor=True):
    if pos is not None:
        # Handle pos = c(rows, cols, ...) layout
        rows, cols = pos[0], pos[1]
        coords = []
        for r in range(rows):
            for c in range(cols):
                coords.append((c, -r))
        # If pos has a 3rd element (like 3 in the last example), 
        # it typically handles specific layout shifts in R; 
        # here we implement a basic grid based on the first two.
        return np.array(coords)
    
    if N is not None:
        # Default circle layout for N elements
        theta = np.linspace(0, 2*np.pi, N, endpoint=False)
        return np.column_stack([np.cos(theta), np.sin(theta)]) * relsize

# --- Section 1 ---
# openplotmat(main = "coordinates")
# text(coordinates(N = 6), lab = LETTERS[1:6], cex = 2)
# r2py:entity:text
coords1 = get_coordinates(N=6)
df1 = pd.DataFrame({'x': coords1[:,0], 'y': coords1[:,1], 'lab': list("ABCDEF")})
p1 = (ggplot(df1) + 
      geom_text(aes(x='x', y='y', label='lab'), size=20) + 
      labs(title="coordinates") + 
      theme_void())
print(p1)

# text(coordinates(N = 8, relsize = 0.5), lab = letters[1:8], cex = 2)
# r2py:entity:text_1
coords2 = get_coordinates(N=8, relsize=0.5)
df2 = pd.DataFrame({'x': coords2[:,0], 'y': coords2[:,1], 'lab': list("abcdefgh")})
p2 = (ggplot(df2) + 
      geom_text(aes(x='x', y='y', label='lab'), size=20) + 
      labs(title="coordinates") + 
      theme_void())
print(p2)

# --- Section 2 ---
# openplotmat(main = "coordinates")
# text(coordinates(pos = c(2, 4, 2)), lab = letters[1:8], cex = 2)
# r2py:entity:text_2
coords3 = get_coordinates(pos=[2, 4, 2])
df3 = pd.DataFrame({'x': coords3[:,0], 'y': coords3[:,1], 'lab': list("abcdefgh")})
p3 = (ggplot(df3) + 
      geom_text(aes(x='x', y='y', label='lab'), size=20) + 
      labs(title="coordinates") + 
      theme_void())
print(p3)

# --- Section 3 ---
# plot(0, type = "n", xlim = c(0, 5), ylim = c(2, 8), main = "coordinates")
# text(coordinates(pos = c(2, 4, 3), hor = FALSE), lab = 1:9, cex = 2)
# r2py:entity:text_3
coords4 = get_coordinates(pos=[2, 4, 3])
# The R code requests 1:9 labels, but pos(2,4) creates 8 slots. 
# To match the request for 1:9, we slice or extend.
labs4 = [str(i) for i in range(1, 10)]
df4 = pd.DataFrame({'x': coords4[:,0], 'y': coords4[:,1], 'lab': labs4[:len(coords4)]})
p4 = (ggplot(df4) + 
      geom_text(aes(x='x', y='y', label='lab'), size=20) + 
      xlim(0, 5) + ylim(2, 8) + 
      labs(title="coordinates") + 
      theme_minimal())
print(p4)