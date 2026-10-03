# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/RColorBrewer__rd_example__ColorBrewer_Rd.py'
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

# RColorBrewer equivalents in Python are typically handled via matplotlib.cm or custom palettes
# Using matplotlib's built-in colormaps for Brewer equivalents
# r2py:entity:mypalette
mypalette = plt.get_cmap('Greens')(np.linspace(0, 1, 7))

# image(1:7,1,as.matrix(1:7),col=mypalette,xlab="Greens (sequential)", ...)
# r2py:entity:image
plt.figure(figsize=(6, 2))
plt.imshow([np.arange(1, 8)], aspect='auto', cmap=mcolors.ListedColormap(mypalette))
plt.xlabel("Greens (sequential)")
plt.ylabel("")
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.show()

# Helper function to mimic display.brewer.pal
# r2py:entity:display.brewer.pal
def display_brewer_pal(name, n=7):
    # Mapping Brewer names to Matplotlib names
    mapping = {"BrBG": "BrBG", "Accent": "Accent"} # Accent isn't standard in cm, but we'll use a qualitative map
    cmap_name = mapping.get(name, name)
    try:
        cmap = plt.get_cmap(cmap_name)
    except ValueError:
        cmap = plt.get_cmap('tab10') # Fallback for 'Accent'
    
    colors = cmap(np.linspace(0, 1, n))
    plt.figure(figsize=(6, 1))
    plt.imshow([colors], aspect='auto')
    plt.title(name)
    plt.axis('off')
    plt.show()

display_brewer_pal("BrBG")
# r2py:entity:display.brewer.pal_1
display_brewer_pal("Accent")

# r2py:entity:display.brewer.all
# Helper function to mimic display.brewer.all
def display_brewer_all(n=10, exact_n=False, palette_type=None, colorblind_friendly=False):
    # Simplified simulation of Brewer palette collection
    all_palettes = {
        "div": ["RdBu", "BrBG", "PiYG", "PRGn", "Spectral"],
        "seq": ["Greens", "Blues", "Oranges", "Reds", "Purples"],
        "qual": ["Set1", "Set2", "Set3", "Pastel1", "Pastel2"]
    }
    
    target_list = []
    if palette_type:
        target_list = all_palettes.get(palette_type, [])
    else:
        for v in all_palettes.values():
            target_list.extend(v)
            
    for name in target_list:
        display_brewer_pal(name, n)

display_brewer_all(n=10, exact_n=False)
# r2py:entity:display.brewer.all_1
display_brewer_all(n=10)
# r2py:entity:display.brewer.all_2
display_brewer_all()
# r2py:entity:display.brewer.all_3
display_brewer_all(palette_type="div")
# r2py:entity:display.brewer.all_4
display_brewer_all(palette_type="seq")
# r2py:entity:display.brewer.all_5
display_brewer_all(palette_type="qual")
# r2py:entity:display.brewer.all_6
display_brewer_all(n=5, palette_type="div", exact_n=True)
# r2py:entity:display.brewer.all_7
display_brewer_all(colorblind_friendly=True)

# brewer.pal.info equivalents
# Creating a dummy dataframe to represent the brewer.pal.info structure
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    "maxcolors": [11, 9, 12],
    "type": ["seq", "div", "qual"]
}, index=["Blues", "BrBG", "Set1"])

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues", :])
print(brewer_pal_info.loc["Blues", "maxcolors"])