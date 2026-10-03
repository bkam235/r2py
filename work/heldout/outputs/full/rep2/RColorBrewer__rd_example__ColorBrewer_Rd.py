# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *
import matplotlib.colors as mcolors

# brewer.pal(7, "Greens")
# Python equivalent using matplotlib colormaps
# r2py:entity:mypalette
cmap = plt.get_cmap('Greens')
mypalette = [mcolors.to_hex(cmap(i)) for i in np.linspace(0.3, 1, 7)]

# image(1:7, 1, as.matrix(1:7), ...)
# r2py:entity:image
plt.figure(figsize=(6, 2))
plt.imshow([np.arange(1, 8)], aspect='auto', cmap=cmap, extent=[1, 7, 1, 1])
plt.xlabel("Greens (sequential)")
plt.ylabel("")
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.show()

# Helper function to mimic display.brewer.pal
# r2py:entity:display.brewer.pal
def display_brewer_pal(palette_name, n=7):
    try:
        cmap = plt.get_cmap(palette_name)
    except ValueError:
        # Fallback for palettes not in matplotlib default names
        cmap = plt.get_cmap('viridis')
    
    colors = [cmap(i) for i in np.linspace(0, 1, n)]
    plt.figure(figsize=(6, 1))
    plt.imshow([colors], aspect='auto')
    plt.axis('off')
    plt.title(palette_name)
    plt.show()

# display.brewer.pal(7,"BrBG")
# r2py:entity:display.brewer.pal
display_brewer_pal("BrBG", 7)

# display.brewer.pal(7,"Accent")
# r2py:entity:display.brewer.pal_1
display_brewer_pal("Accent", 7)

# Helper to mimic display.brewer.all
# r2py:entity:display.brewer.all
def display_brewer_all(n=10, exact_n=False, palette_type=None, colorblindFriendly=False):
    # Simplified approximation of RColorBrewer's all palettes
    all_cmaps = plt.colormaps
    selected = []
    for name in all_cmaps:
        if palette_type == 'div' and 'Rd' in name: selected.append(name)
        elif palette_type == 'seq' and 'Blues' in name: selected.append(name)
        elif palette_type == 'qual' and 'Set' in name: selected.append(name)
        elif palette_type is None: selected.append(name)
    
    # Limit to a reasonable subset for display
    selected = selected[:20]
    
    fig, axes = plt.subplots(len(selected), 1, figsize=(8, len(selected)*0.5))
    if len(selected) == 1: axes = [axes]
    
    for ax, name in zip(axes, selected):
        cmap = plt.get_cmap(name)
        colors = [cmap(i) for i in np.linspace(0, 1, n)]
        ax.imshow([colors], aspect='auto')
        ax.set_title(name, loc='left', fontsize=8)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# display.brewer.all(n=10, exact.n=FALSE)
# r2py:entity:display.brewer.all
display_brewer_all(n=10, exact_n=False)

# display.brewer.all(n=10)
# r2py:entity:display.brewer.all_1
display_brewer_all(n=10)

# display.brewer.all()
# r2py:entity:display.brewer.all_2
display_brewer_all()

# display.brewer.all(type="div")
# r2py:entity:display.brewer.all_3
display_brewer_all(palette_type="div")

# display.brewer.all(type="seq")
# r2py:entity:display.brewer.all_4
display_brewer_all(palette_type="seq")

# display.brewer.all(type="qual")
# r2py:entity:display.brewer.all_5
display_brewer_all(palette_type="qual")

# display.brewer.all(n=5,type="div",exact.n=TRUE)
# r2py:entity:display.brewer.all_6
display_brewer_all(n=5, palette_type="div", exact_n=True)

# display.brewer.all(colorblindFriendly=TRUE)
# r2py:entity:display.brewer.all_7
display_brewer_all(colorblindFriendly=True)

# brewer.pal.info
# Creating a dummy DataFrame to simulate R's brewer.pal.info
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    'maxcolors': [9, 11, 12],
    'type': ['seq', 'div', 'qual']
}, index=['Blues', 'BrBG', 'Accent'])

print(brewer_pal_info)

# brewer.pal.info["Blues",]
print(brewer_pal_info.loc['Blues'])

# brewer.pal.info["Blues",]$maxcolors
print(brewer_pal_info.loc['Blues', 'maxcolors'])