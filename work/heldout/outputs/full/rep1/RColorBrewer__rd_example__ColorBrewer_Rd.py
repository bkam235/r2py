# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# RColorBrewer equivalent in Python is usually handled via matplotlib colormaps
# 'Greens' is a built-in sequential map
# r2py:entity:mypalette
mypalette = plt.get_cmap('Greens')(np.linspace(0, 1, 7))

# image(1:7,1,as.matrix(1:7),col=mypalette,...)
# r2py:entity:image
fig, ax = plt.subplots()
ax.imshow([np.arange(1, 8)], aspect='auto', cmap=colors.ListedColormap(mypalette))
ax.set_xlabel("Greens (sequential)")
ax.set_ylabel("")
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
plt.show()

# display.brewer.pal(7,"BrBG")
# r2py:entity:display.brewer.pal
def display_brewer_pal(n, name):
    cmap = plt.get_cmap(name)
    colors_list = cmap(np.linspace(0, 1, n))
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.imshow([colors_list], aspect='auto')
    ax.set_axis_off()
    plt.title(name)
    plt.show()

display_brewer_pal(7, "BrBG")
# r2py:entity:display.brewer.pal_1
display_brewer_pal(7, "Accent")

# display.brewer.all(n=10, exact.n=FALSE) 
# Matplotlib doesn't have a direct "all" display; we simulate by iterating available cmaps
# r2py:entity:display.brewer.all
def display_brewer_all(n=None, type=None, exact_n=False, colorblindFriendly=False):
    # Mapping of RColorBrewer names to Matplotlib names
    all_maps = {
        "seq": ["Greens", "Blues", "Reds", "Oranges", "Purples"],
        "div": ["BrBG", "RdBu", "PiYG", "PRGn", "RdYlBu"],
        "qual": ["Set1", "Set2", "Set3", "Paired", "Accent"]
    }
    
    targets = []
    if type == "div": targets = all_maps["div"]
    elif type == "seq": targets = all_maps["seq"]
    elif type == "qual": targets = all_maps["qual"]
    else: targets = all_maps["seq"] + all_maps["div"] + all_maps["qual"]
    
    for name in targets:
        display_brewer_pal(n if n else 8, name)

display_brewer_all(n=10)
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

# brewer.pal.info representation
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    "Blues": {"maxcolors": 9, "type": "seq"},
    "Greens": {"maxcolors": 9, "type": "seq"},
    "BrBG": {"maxcolors": 11, "type": "div"},
    "Accent": {"maxcolors": 8, "type": "qual"}
}).T

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues"])
print(brewer_pal_info.loc["Blues", "maxcolors"])