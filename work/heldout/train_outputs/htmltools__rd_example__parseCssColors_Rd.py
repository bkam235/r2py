# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from shiny import App, ui
import matplotlib.colors as mcolors

# R's parseCssColors approximates to matplotlib.colors.to_rgba
# which handles hex, rgb, rgba, hsl (via some versions), and named colors.

# r2py:entity:parseCssColors
colors_list = [
    "#0d6efd",
    "#DC35457F",
    "rgb(32,201,151)",
    "  rgba( 23 , 162 , 184 , 0.5 )  ",
    "hsl(261, 51%, 51%)",
    "cornflowerblue"
]

# Note: matplotlib.colors.to_rgba doesn't support hsl natively. 
# To mimic the R behavior of parsing various CSS formats into RGBA:
# r2py:entity:parseCssColors
def parse_css_color(color):
    try:
        # Handle HSL manually since matplotlib doesn't
        if 'hsl' in color:
            import colorsys
            # Extract numbers from hsl(h, s%, l%)
            vals = [float(x.strip('%')) for x in color.replace('hsl(', '').replace(')', '').split(',')]
            r, g, b = colorsys.hls_to_rgb(vals[0]/360.0, vals[2]/100.0, vals[1]/100.0)
            return (r, g, b, 1.0)
        
        # Handle rgb/rgba/hex/named
        return mcolors.to_rgba(color.strip())
    except:
        return None

# r2py:entity:parseCssColors
result = [parse_css_color(c) for c in colors_list]
print(result)