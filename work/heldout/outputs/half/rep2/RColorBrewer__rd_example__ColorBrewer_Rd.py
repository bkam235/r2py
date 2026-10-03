# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# RColorBrewer equivalents in Python are typically handled by matplotlib.cm or specialized libraries.
# However, the specific Brewer palettes are available via matplotlib.colors or can be mapped.
# To maintain the RColorBrewer behavior, we can use the 'brewer' palettes from matplotlib.

# r2py:entity:mypalette
def brewer_pal(n, name):
    """
    Equivalent to R's brewer.pal. 
    Uses matplotlib's built-in colormaps which include ColorBrewer sets.
    """
    # Matplotlib colormap names are slightly different from RColorBrewer
    # R 'Greens' -> matplotlib 'Greens'
    # R 'BrBG' -> matplotlib 'BrBG'
    # R 'Accent' -> matplotlib 'Accent'
    try:
        cmap = plt.get_cmap(name)
    except ValueError:
        raise ValueError(f"{name} is not a valid palette name for brewer_pal")
    
    # R's brewer.pal often returns a specific subset. 
    # In Python, we sample the colormap.
    colors = cmap(np.linspace(0, 1, n))
    return [mcolors.to_hex(c) for c in colors]

# r2py:entity:display.brewer.pal
def display_brewer_pal(n, name):
    """Equivalent to R's display.brewer.pal"""
    colors = brewer_pal(n, name)
    
    fig, ax = plt.subplots(figsize=(6, 2))
    # Create a horizontal bar of colors
    for i in range(n):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=colors[i]))
    
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
    """Equivalent to R's display.brewer.all"""
    # This is a complex function. In Python, we simulate the display of multiple palettes.
    # Simplified implementation showing the available colormaps in the requested category.
    import matplotlib
    all_cmaps = matplotlib.colormaps
    
    # Categorize colormaps (simplified mapping)
    div_list = ["RdBu", "RdYlBu", "Spectral", "BrBG", "PiYG", "PRGn"]
    seq_list = ["Blues", "Greens", "Reds", "Purples", "YlGnBu", "YlOrRd"]
    qual_list = ["Accent", "Set1", "Set2", "Set3", "Paired"]
    
    if type_val == "div":
        current_list = div_list
    elif type_val == "qual":
        current_list = qual_list
    elif type_val == "seq":
        current_list = seq_list
    else:
        current_list = div_list + qual_list + seq_list

    if select:
        current_list = [name for name in current_list if name in select]

    if colorblind_friendly:
        # Simplified: only keep some
        current_list = [name for name in current_list if name in ["Set2", "Paired"]]

    num_cols = n if n is not None else 10
    
    fig, axes = plt.subplots(len(current_list), 1, figsize=(8, len(current_list)*0.5))
    if len(current_list) == 1:
        axes = [axes]
        
    for ax, name in zip(axes, current_list):
        colors = brewer_pal(num_cols, name)
        for i in range(num_cols):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=colors[i]))
        ax.set_xlim(0, num_cols)
        ax.set_ylim(0, 1)
        ax.set_ylabel(name, rotation=0, ha='right', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        
    plt.tight_layout()
    plt.show()

# r2py:entity:devAskNewPage
def dev_ask_new_page(ask=True):
    """Equivalent to R's devAskNewPage - Python's plt.show() usually blocks or creates new windows."""
    if ask:
        plt.pause(0.1)

# Start of translated script logic
# r2py:entity:mypalette
mypalette = brewer_pal(7, "Greens")

# image(1:7,1,as.matrix(1:7),col=mypalette,...)
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

# brewer.pal.info mapping
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    "name": ["Blues", "Greens", "Reds"],
    "maxcolors": [9, 9, 9],
    "type": ["seq", "seq", "seq"]
}).set_index("name")

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues"])
print(brewer_pal_info.loc["Blues", "maxcolors"])