# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260929_162051/py/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *

# RColorBrewer equivalent logic using matplotlib
# Note: Python does not have a direct 'display.brewer.all' function, 
# so we implement the visualization logic using matplotlib.

# mypalette<-brewer.pal(7,"Greens")
# r2py:entity:mypalette
import matplotlib.colors as mcolors
mypalette = plt.get_cmap('Greens').colors[:7] if hasattr(plt.get_cmap('Greens'), 'colors') else [plt.get_cmap('Greens')(i) for i in np.linspace(0, 1, 7)]

# image(1:7,1,as.matrix(1:7),col=mypalette,...)
# r2py:entity:image
plt.figure(figsize=(6, 2))
plt.imshow([np.arange(1, 8)], aspect='auto', cmap=mcolors.ListedColormap(mypalette))
plt.xlabel("Greens (sequential)")
plt.ylabel("")
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.show()

# Helper to simulate display.brewer.pal
# r2py:entity:display.brewer.pal
def display_brewer_pal(n, palette_name):
    cmap = plt.get_cmap(palette_name)
    colors = [cmap(i) for i in np.linspace(0, 1, n)]
    plt.figure(figsize=(6, 1))
    plt.imshow([colors], aspect='auto')
    plt.axis('off')
    plt.title(palette_name)
    plt.show()

# display.brewer.pal(7,"BrBG")
display_brewer_pal(7, "BrBG")

# display.brewer.pal(7,"Accent")
# r2py:entity:display.brewer.pal_1
display_brewer_pal(7, "Accent")

# Helper to simulate display.brewer.all
# r2py:entity:display.brewer.all
def display_brewer_all(n=None, exact_n=False, type=None, colorblindFriendly=False):
    # Simplified map of RColorBrewer categories to Matplotlib
    palettes = {
        "div": ["RdBu", "Spectral", "BrBG", "PiYG", "PRGn"],
        "seq": ["Greens", "Blues", "Oranges", "Reds", "Purples"],
        "qual": ["Set1", "Set2", "Set3", "Pastel1", "Accent"]
    }
    
    target_list = []
    if type == "div": target_list = palettes["div"]
    elif type == "seq": target_list = palettes["seq"]
    elif type == "qual": target_list = palettes["qual"]
    else: target_list = palettes["div"] + palettes["seq"] + palettes["qual"]

    for p in target_list:
        cmap = plt.get_cmap(p)
        colors = [cmap(i) for i in np.linspace(0, 1, n if n else 10)]
        plt.figure(figsize=(6, 0.5))
        plt.imshow([colors], aspect='auto')
        plt.axis('off')
        plt.title(p)
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
display_brewer_all(type="div")

# display.brewer.all(type="seq")
# r2py:entity:display.brewer.all_4
display_brewer_all(type="seq")

# display.brewer.all(type="qual") 
# r2py:entity:display.brewer.all_5
display_brewer_all(type="qual")

# display.brewer.all(n=5,type="div",exact.n=TRUE)
# r2py:entity:display.brewer.all_6
display_brewer_all(n=5, type="div", exact_n=True)

# display.brewer.all(colorblindFriendly=TRUE)
# r2py:entity:display.brewer.all_7
display_brewer_all(colorblindFriendly=True)

# brewer.pal.info (Simulated as a DataFrame)
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    "Blues": {"maxcolors": 9, "type": "seq"},
    "Greens": {"maxcolors": 9, "type": "seq"},
    "BrBG": {"maxcolors": 11, "type": "div"},
    "Accent": {"maxcolors": 8, "type": "qual"}
}).T

print(brewer_pal_info)

# brewer.pal.info["Blues",]
print(brewer_pal_info.loc["Blues"])

# brewer.pal.info["Blues",]$maxcolors
print(brewer_pal_info.loc["Blues", "maxcolors"])