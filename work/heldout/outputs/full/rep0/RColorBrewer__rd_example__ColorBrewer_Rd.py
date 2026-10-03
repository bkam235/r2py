# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# Note: Python's matplotlib provides access to Brewer palettes via 'brewer' 
# but usually requires the 'palettable' library or manual definition.
# Using matplotlib.cm for standard sequential/diverging logic.

# mypalette <- brewer.pal(7,"Greens")
# approximated using matplotlib's Greens colormap
# r2py:entity:mypalette
cmap_greens = plt.get_cmap('Greens')
mypalette = [colors.to_hex(cmap_greens(i)) for i in np.linspace(0.3, 1, 7)]

# image(1:7,1,as.matrix(1:7),col=mypalette,...)
# r2py:entity:image
plt.figure(figsize=(6, 2))
data = np.arange(1, 8).reshape(1, 7)
plt.imshow(data, aspect='auto', cmap=colors.ListedColormap(mypalette))
plt.xlabel("Greens (sequential)")
plt.ylabel("")
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.show()

# display.brewer.pal(7,"BrBG")
# r2py:entity:display.brewer.pal
def display_brewer_pal(n, name):
    try:
        cmap = plt.get_cmap(name)
    except ValueError:
        cmap = plt.get_cmap('RdBu') # fallback
    cols = [colors.to_hex(cmap(i)) for i in np.linspace(0, 1, n)]
    plt.figure(figsize=(6, 1))
    plt.imshow([np.arange(n)], aspect='auto', cmap=colors.ListedColormap(cols))
    plt.axis('off')
    plt.title(name)
    plt.show()

display_brewer_pal(7, "BrBG")
# r2py:entity:display.brewer.pal_1
display_brewer_pal(7, "Accent")

# display.brewer.all variants
# Python does not have a direct equivalent to display.brewer.all().
# We simulate the behavior by iterating through common matplotlib colormaps.

# r2py:entity:display.brewer.all
def display_brewer_all(n=10, palette_type=None, exact_n=False, colorblind=False):
    # Subset of common matplotlib cmaps that mirror Brewer types
    all_cmaps = {
        'div': ['RdBu', 'RdYlBu', 'Spectral', 'coolwarm'],
        'seq': ['Greens', 'Blues', 'Reds', 'Purples', 'YlGnBu'],
        'qual': ['Set1', 'Set2', 'Set3', 'Paired', 'tab10']
    }
    
    target_list = []
    if palette_type:
        target_list = all_cmaps.get(palette_type, [])
    else:
        for v in all_cmaps.values(): target_list.extend(v)

    for name in target_list:
        display_brewer_pal(n, name)

display_brewer_all(n=10)
# r2py:entity:display.brewer.all_1
display_brewer_all()
# r2py:entity:display.brewer.all_2
display_brewer_all(palette_type="div")
# r2py:entity:display.brewer.all_3
display_brewer_all(palette_type="seq")
# r2py:entity:display.brewer.all_4
display_brewer_all(palette_type="qual")
# r2py:entity:display.brewer.all_5
display_brewer_all(n=5, palette_type="div", exact_n=True)
# r2py:entity:display.brewer.all_6
display_brewer_all(colorblind=True)

# brewer.pal.info simulation
# Since this is a data frame in R, we create a pandas DataFrame
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    'name': ['Blues', 'Greens', 'Reds'],
    'maxcolors': [9, 9, 9],
    'type': ['seq', 'seq', 'seq']
}).set_index('name')

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues"])
print(brewer_pal_info.loc["Blues", "maxcolors"])