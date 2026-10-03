# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# r2py:entity:mypalette
def brewer_pal(n, name):
    """
    Simulates the RColorBrewer::brewer.pal function.
    In Python, we can use matplotlib's colormaps which include the Brewer palettes.
    """
    # Map of RColorBrewer names to Matplotlib cmap names
    # Note: Matplotlib's Brewer colormaps are available via 'brewer' if using palette libraries,
    # but standard matplotlib has equivalents or we can use the specific names.
    # For a precise translation, we use the standard map.
    cmap_map = {
        "Greens": "Greens",
        "BrBG": "BrBG",
        "Accent": "Accent",
        "Blues": "Blues",
        # ... other mappings as needed
    }
    
    cmap_name = cmap_map.get(name, name)
    try:
        cmap = plt.get_cmap(cmap_name)
    except ValueError:
        raise ValueError(f"{name} is not a valid palette name for brewer_pal")
    
    # Handle n constraints (min 3, max depends on palette)
    # In Matplotlib, we can sample any n from the continuous map
    if n < 3:
        print("Warning: minimal value for n is 3, returning requested palette with 3 different levels")
        n = 3
    
    # Return a list of hex colors
    return [colors.to_hex(cmap(i)) for i in np.linspace(0, 1, n)]

# r2py:entity:display.brewer.pal
def display_brewer_pal(n, name):
    pal = brewer_pal(n, name)
    fig, ax = plt.subplots(figsize=(6, 2))
    # Create a horizontal bar as a surrogate for R's image()
    for i in range(n):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=pal[i]))
    
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_xlabel(f"{name}")
    ax.set_ylabel("")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.show()

# r2py:entity:display.brewer.all
def display_brewer_all(n=None, type_val="all", select=None, exact_n=True, colorblind_friendly=False):
    # This is a complex R function that iterates through all Brewer palettes.
    # We simulate the behavior by listing common Brewer palettes in Matplotlib.
    all_pals = {
        "div": ["BrBG", "PiYG", "PRGn", "RdBu", "RdGy", "RdYlBu", "RdYlGn", "Spectral"],
        "seq": ["Blues", "Greens", "Greys", "Oranges", "Purples", "Reds", "YlGnBu", "YlOrBr"],
        "qual": ["Accent", "Paired", "Set1", "Set2", "Set3"]
    }
    
    if type_val == "all":
        target_list = all_pals["div"] + all_pals["qual"] + all_pals["seq"]
    else:
        target_list = all_pals.get(type_val, [])
    
    if select:
        target_list = [p for p in target_list if p in select]
        
    # Plotting the grid
    fig, ax = plt.subplots(figsize=(10, len(target_list)))
    for i, name in enumerate(target_list):
        # use n or a default
        count = n if n is not None else 10
        pal = brewer_pal(count, name)
        for j in range(count):
            ax.add_patch(plt.Rectangle((j, i), 1, 0.8, color=pal[j], ec="lightgrey") )
        ax.text(-0.5, i + 0.4, name, va='center', ha='right')
        
    ax.set_xlim(0, max(n if n else 10, 10))
    ax.set_ylim(0, len(target_list))
    ax.axis('off')
    plt.show()

# r2py:entity:devAskNewPage
def dev_ask_new_page(ask=True):
    # In Python's matplotlib, plt.show() usually blocks or creates new windows.
    # We can use plt.pause or just assume interactive mode.
    if ask:
        plt.pause(0.1)

# Main Script Translation
# r2py:entity:mypalette
mypalette = brewer_pal(7, "Greens")
# image(1:7,1,as.matrix(1:7),col=mypalette,xlab="Greens (sequential)", ylab="",xaxt="n",yaxt="n",bty="n")
# r2py:entity:image
fig, ax = plt.subplots(figsize=(6, 2))
for i in range(7):
    ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=mypalette[i]))
ax.set_xlim(0, 7)
ax.set_ylim(0, 1)
ax.set_xlabel("Greens (sequential)")
ax.set_ylabel("")
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
plt.show()

# r2py:entity:display.brewer.pal
display_brewer_pal(7, "BrBG")
# r2py:entity:devAskNewPage
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.pal_1
display_brewer_pal(7, "Accent")
# r2py:entity:devAskNewPage_1
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all
display_brewer_all(n=10, exact_n=False)
# r2py:entity:devAskNewPage_2
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_1
display_brewer_all(n=10)
# r2py:entity:devAskNewPage_3
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_2
display_brewer_all()
# r2py:entity:devAskNewPage_4
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_3
display_brewer_all(type_val="div")
# r2py:entity:devAskNewPage_5
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_4
display_brewer_all(type_val="seq")
# r2py:entity:devAskNewPage_6
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_5
display_brewer_all(type_val="qual")
# r2py:entity:devAskNewPage_7
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_6
display_brewer_all(n=5, type_val="div", exact_n=True)
# r2py:entity:devAskNewPage_8
dev_ask_new_page(ask=True)

# r2py:entity:display.brewer.all_7
display_brewer_all(colorblind_friendly=True)
# r2py:entity:devAskNewPage_9
dev_ask_new_page(ask=True)

# Simulating brewer.pal.info dataframe
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    "maxcolors": [8, 12, 12, 9, 12],
    "type": ["qual", "seq", "div", "seq", "div"]
}, index=["Accent", "Blues", "BrBG", "Greens", "RdBu"])

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues", :])
print(brewer_pal_info.loc["Blues", "maxcolors"])