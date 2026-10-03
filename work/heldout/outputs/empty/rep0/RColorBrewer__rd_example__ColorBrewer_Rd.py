# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/RColorBrewer__rd_example__ColorBrewer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'RColorBrewer__rd_example__ColorBrewer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['brewer.pal.info']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *

# RColorBrewer equivalent in Python is often handled by matplotlib's colormaps
# 'Greens' is a standard sequential map
# r2py:entity:mypalette
mypalette = plt.get_cmap('Greens')(np.linspace(0, 1, 7))

# image(1:7, 1, as.matrix(1:7), col=mypalette...)
# r2py:entity:image
plt.figure(figsize=(6, 2))
plt.imshow([np.arange(7)], aspect='auto', cmap=plt.get_cmap('Greens'), 
           extent=[1, 7, 1, 1])
plt.xlabel("Greens (sequential)")
plt.ylabel("")
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.show()

# display.brewer.pal(7, "BrBG")
# r2py:entity:display.brewer.pal
plt.figure(figsize=(6, 2))
plt.imshow([np.linspace(0, 1, 7)], aspect='auto', cmap=plt.get_cmap('BrBG'))
plt.axis('off')
plt.show()

# display.brewer.pal(7, "Accent")
# r2py:entity:display.brewer.pal_1
plt.figure(figsize=(6, 2))
# 'Accent' is a qualitative map. Using 'Set3' or 'tab10' as approximation
plt.imshow([np.arange(7)], aspect='auto', cmap=plt.get_cmap('Set3'))
plt.axis('off')
plt.show()

# Mocking display.brewer.all() functionality as Python does not have a direct equivalent
# We use a list of common Brewer-like colormaps categorized by type
# r2py:entity:display.brewer.all
div_pals = ['RdBu', 'PiYG', 'PRGn', 'BrBG', 'RdYlBu', 'RdYlGn', 'Spectral']
seq_pals = ['Blues', 'Greens', 'Greys', 'Oranges', 'Purples', 'Reds', 'YlGnBu']
qual_pals = ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired']

def plot_all_palettes(pals, n=10):
    fig, axes = plt.subplots(len(pals), 1, figsize=(8, len(pals)*0.5))
    if len(pals) == 1: axes = [axes]
    for ax, pal in zip(axes, pals):
        ax.imshow([np.linspace(0, 1, n)], aspect='auto', cmap=plt.get_cmap(pal))
        ax.set_title(pal, loc='left', fontsize=10)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# display.brewer.all(n=10, exact.n=FALSE)
plot_all_palettes(div_pals + seq_pals + qual_pals, n=10)

# r2py:entity:display.brewer.all_1
# display.brewer.all(n=10)
plot_all_palettes(div_pals + seq_pals + qual_pals, n=10)

# r2py:entity:display.brewer.all_2
# display.brewer.all()
plot_all_palettes(div_pals + seq_pals + qual_pals, n=12)

# r2py:entity:display.brewer.all_3
# display.brewer.all(type="div")
plot_all_palettes(div_pals)

# r2py:entity:display.brewer.all_4
# display.brewer.all(type="seq")
plot_all_palettes(seq_pals)

# r2py:entity:display.brewer.all_5
# display.brewer.all(type="qual")
plot_all_palettes(qual_pals)

# r2py:entity:display.brewer.all_6
# display.brewer.all(n=5, type="div", exact.n=TRUE)
plot_all_palettes(div_pals, n=5)

# r2py:entity:display.brewer.all_7
# display.brewer.all(colorblindFriendly=TRUE)
# Approximation: Subset of common color-blind friendly maps
plot_all_palettes(['viridis', 'magma', 'plasma'], n=10)

# brewer.pal.info emulation
# r2py:entity:brewer.pal.info
brewer_pal_info = pd.DataFrame({
    'type': ['div']*len(div_pals) + ['seq']*len(seq_pals) + ['qual']*len(qual_pals),
    'maxcolors': [11]*len(div_pals) + [9]*len(seq_pals) + [12]*len(qual_pals)
}, index=div_pals + seq_pals + qual_pals)

print(brewer_pal_info)
print(brewer_pal_info.loc["Blues", :])
print(brewer_pal_info.loc["Blues", "maxcolors"])