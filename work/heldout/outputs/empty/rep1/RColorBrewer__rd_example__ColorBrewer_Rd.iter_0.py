# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *
import colourbrewer # Requires pip install colour-brewer

# mypalette <- brewer.pal(7, "Greens")
# r2py:entity:mypalette
mypalette = colourbrewer.get_palette("Greens", 7)

# image(1:7, 1, as.matrix(1:7), col=mypalette, xlab="Greens (sequential)", ...)
# r2py:entity:image
fig, ax = plt.subplots()
# Creating a 1x7 matrix to mimic the image() behavior
data = np.arange(1, 8).reshape(1, 7)
# Mapping the 7 colors to the 7 values
from matplotlib.colors import ListedColormap
cmap = ListedColormap(mypalette)
ax.imshow(data, aspect='auto', cmap=cmap)
ax.set_xlabel("Greens (sequential)")
ax.set_ylabel("")
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
plt.show()

# display.brewer.pal(7, "BrBG")
# r2py:entity:display.brewer.pal
def display_brewer_pal(n, palette):
    cols = colourbrewer.get_palette(palette, n)
    plt.figure(figsize=(6, 1))
    plt.imshow([cols], aspect='auto')
    plt.axis('off')
    plt.title(f"{palette} ({n})")
    plt.show()

display_brewer_pal(7, "BrBG")
# devAskNewPage(ask=TRUE) is implicit in plt.show() sequence

# display.brewer.pal(7, "Accent")
# r2py:entity:display.brewer.pal_1
display_brewer_pal(7, "Accent")

# display.brewer.all logic
# r2py:entity:display.brewer.all
def display_brewer_all(n=None, exact_n=False, palette_type=None, colorblindFriendly=False):
    all_palettes = colourbrewer.palettes
    keys = all_palettes.keys()
    
    filtered_palettes = []
    for k in keys:
        p_info = all_palettes[k]
        if palette_type and p_info['type'] != palette_type:
            continue
        if colorblindFriendly and not p_info.get('colorblind', True):
            continue
        
        max_cols = p_info['colors']
        if n:
            if exact_n and max_cols != n:
                continue
            elif not exact_n and max_cols < n:
                continue
        filtered_palettes.append(k)

    # Plotting the collection
    fig, axes = plt.subplots(len(filtered_palettes), 1, figsize=(8, len(filtered_palettes)*0.5))
    if len(filtered_palettes) == 1: axes = [axes]
    for i, k in enumerate(filtered_palettes):
        # If n is provided, take n colors, otherwise take max
        num = n if n else all_palettes[k]['colors']
        cols = colourbrewer.get_palette(k, num)
        axes[i].imshow([cols], aspect='auto')
        axes[i].set_yticks([])
        axes[i].set_xticks([])
        axes[i].set_ylabel(k, rotation=0, ha='right', va='center')
    plt.tight_layout()
    plt.show()

# display.brewer.all(n=10, exact.n=FALSE)
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

# display.brewer.all(n=5, type="div", exact.n=TRUE)
# r2py:entity:display.brewer.all_6
display_brewer_all(n=5, palette_type="div", exact_n=True)

# display.brewer.all(colorblindFriendly=TRUE)
# r2py:entity:display.brewer.all_7
display_brewer_all(colorblindFriendly=True)

# brewer.pal.info
# Convert the dictionary to a pandas DataFrame to mimic the R dataframe structure
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame.from_dict(colourbrewer.palettes, orient='index')

print(brewer_pal_info)

# brewer.pal.info["Blues",]
print(brewer_pal_info.loc["Blues"])

# brewer.pal.info["Blues",]$maxcolors
# In colourbrewer python lib, 'colors' represents the max count
print(brewer_pal_info.loc["Blues", "colors"])