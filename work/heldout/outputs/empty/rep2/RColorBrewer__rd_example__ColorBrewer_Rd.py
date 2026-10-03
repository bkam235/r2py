# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Note: Python doesn't have a direct 1:1 clone of RColorBrewer's display functions.
# We use matplotlib.colormaps to approximate the palettes.

# mypalette <- brewer.pal(7, "Greens")
# r2py:entity:mypalette
cmap_greens = plt.get_cmap('Greens')
mypalette = [cmap_greens(i) for i in np.linspace(0, 1, 7)]

# image(1:7, 1, as.matrix(1:7), col=mypalette, ...)
# r2py:entity:image
fig, ax = plt.subplots(figsize=(6, 2))
ax.imshow([np.arange(1, 8)], aspect='auto', cmap=cmap_greens, extent=[1, 7, 1, 1])
ax.set_xlabel("Greens (sequential)")
ax.set_ylabel("")
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
plt.show()

# display.brewer.pal(7, "BrBG")
# r2py:entity:display.brewer.pal
def display_brewer_pal(n, name):
    cmap = plt.get_cmap(name)
    colors = [cmap(i) for i in np.linspace(0, 1, n)]
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.imshow([colors], aspect='auto')
    ax.axis('off')
    plt.show()

display_brewer_pal(7, "BrBG")
# r2py:entity:display.brewer.pal_1
display_brewer_pal(7, "Accent")

# display.brewer.all(n=10, exact.n=FALSE)
# r2py:entity:display.brewer.all
def display_brewer_all(n=None, type=None, exact_n=False, colorblindFriendly=False):
    # Mapping RColorBrewer names to Matplotlib cmaps
    all_cmaps = plt.colormaps()
    # Simplified filter for sequential, diverging, qualitative
    # In a real scenario, one would map specific R names to MPL names
    div = ['RdBu', 'PiYG', 'PRGn', 'BrBG', 'Spectral']
    seq = ['Blues', 'Greens', 'Reds', 'Purples', 'Greys']
    qual = ['Set1', 'Set2', 'Set3', 'Paired', 'Accent']
    
    target_list = all_cmaps if type is None else (div if type == 'div' else (seq if type == 'seq' else qual))
    
    for name in target_list:
        if type is None or name in target_list:
            display_brewer_pal(n if n else 10, name)

display_brewer_all(n=10, exact_n=False)
# r2py:entity:display.brewer.all_1
display_brewer_all(n=10)
# r2py:entity:display.brewer.all_2
display_brewer_all()
# r2py:entity:display.brewer.all_3
display_brewer_all(type="div")
# r2py:entity:display.brewer.all_4
display_brewer_all(type="seq")
# r2py:entity:display.brewer.all_5
display_brewer_all(type="qual")
# r2py:entity:display.brewer.all_6
display_brewer_all(n=5, type="div", exact_n=True)
# r2py:entity:display.brewer.all_7
display_brewer_all(colorblindFriendly=True)

# brewer.pal.info
# Creating a dummy dataframe to mimic the info structure
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    'maxcolors': [9, 9, 12, 8],
    'type': ['seq', 'seq', 'div', 'qual']
}, index=['Blues', 'Greens', 'BrBG', 'Accent'])

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues", :])
print(brewer_pal_info.loc["Blues", "maxcolors"])