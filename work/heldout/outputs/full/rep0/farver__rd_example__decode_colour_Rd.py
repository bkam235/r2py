# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    """
    Decodes colors into a specified color space.
    """
    results = []
    cols = []
    
    for col in colour:
        # Convert named colors or hex to rgba (0-1 range)
        rgba = mcolors.to_rgba(col)
        
        if to.lower() == 'rgb':
            # farver RGB uses 0-255 integers
            rgb = [int(round(x * 255)) for x in rgba[:3]]
            if alpha:
                rgb.append(rgba[3])
            results.append(rgb)
            cols = ['r', 'g', 'b'] + (['alpha'] if alpha else [])
            
        elif to.lower() == 'lch':
            # sRGB to XYZ (D65)
            r, g, b = rgba[:3]
            def pivot(c): 
                return ((c + 0.055) / 1.055)**2.4 if c > 0.04045 else c / 12.92
            
            r_lin, g_lin, b_lin = map(pivot, [r, g, b])
            
            # Standard sRGB D65 matrix
            x = r_lin * 0.4124564 + g_lin * 0.3575761 + b_lin * 0.1804375
            y = r_lin * 0.2126729 + g_lin * 0.7151522 + b_lin * 0.0721750
            z = r_lin * 0.0193339 + g_lin * 0.1183895 + b_lin * 0.9504906
            
            # XYZ to Lab (D65)
            # Reference white D65
            Xn, Yn, Zn = 0.95047, 1.00000, 1.08883
            
            def f(t): 
                return t**(1/3) if t > 0.008856 else (7.787 * t) + (16/116)
            
            L = 116 * f(y / Yn) - 16
            a_lab = 500 * (f(x / Xn) - f(y / Yn))
            b_lab = 200 * (f(y / Yn) - f(z / Zn))
            
            # Lab to LCH
            C = np.sqrt(a_lab**2 + b_lab**2)
            H = np.degrees(np.arctan2(b_lab, a_lab)) % 360
            
            val = [L, C, H]
            if alpha:
                val.append(rgba[3])
            results.append(val)
            cols = ['l', 'c', 'h'] + (['alpha'] if alpha else [])
            
    return pd.DataFrame(results, columns=cols)

# Test cases
# r2py:entity:decode_colour
print(decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4']))
# r2py:entity:decode_colour_1
print(decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], alpha=True))
# r2py:entity:decode_colour_2
print(decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], to='lch'))