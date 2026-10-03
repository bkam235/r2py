# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np
import matplotlib.colors as mcolors
import pandas as pd

# Helper function to approximate farver::decode_colour
# r2py:entity:decode_colour
def decode_colour(colour_val, alpha=False, to='rgb', white='D65', na_value=None):
    if isinstance(colour_val, str):
        colour_val = [colour_val]
    
    results = []
    
    for c in colour_val:
        try:
            # 1. Decode to RGB [0, 1]
            if isinstance(c, str) and c.startswith('#'):
                hex_val = c[1:]
                if len(hex_val) == 8:
                    r = int(hex_val[0:2], 16) / 255.0
                    g = int(hex_val[2:4], 16) / 255.0
                    b = int(hex_val[4:6], 16) / 255.0
                    a = int(hex_val[6:8], 16) / 255.0
                elif len(hex_val) == 6:
                    r = int(hex_val[0:2], 16) / 255.0
                    g = int(hex_val[2:4], 16) / 255.0
                    b = int(hex_val[4:6], 16) / 255.0
                    a = 1.0
                else:
                    raise ValueError("Invalid hex length")
            elif isinstance(c, str):
                rgba = mcolors.to_rgba(c)
                r, g, b, a = rgba
            else:
                raise ValueError("Unsupported color format")

            # 2. Convert based on 'to'
            if to.lower() == 'rgb':
                # farver returns RGB as 0-255 integers (as floats in matrix)
                row = [float(round(r * 255)), float(round(g * 255)), float(round(b * 255))]
                if alpha:
                    row.append(float(a))
                results.append(row)
            elif to.lower() == 'lch':
                # Precise sRGB -> XYZ -> Lab -> LCH conversion
                def rgb_to_lab(r, g, b):
                    def pivot(x):
                        return ((x + 0.055) / 1.055)**2.4 if x > 0.04045 else x / 12.92
                    
                    r, g, b = pivot(r), pivot(g), pivot(b)
                    
                    # sRGB to XYZ (D65) - standard matrices
                    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804384
                    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
                    z = r * 0.0193339 + g * 0.1183895 + b * 0.9503041
                    
                    # XYZ to Lab (D65)
                    def f(t):
                        return t**(1/3) if t > 0.00885645167 else (7.787 * t) + (16/116)
                    
                    # Reference white D65 (standard CIE)
                    Xn, Yn, Zn = 0.95047, 1.00000, 1.08883
                    L = 116 * f(y / Yn) - 16
                    a_val = 500 * (f(x / Xn) - f(y / Yn))
                    b_val = 200 * (f(y / Yn) - f(z / Zn))
                    return L, a_val, b_val

                L, a_val, b_val = rgb_to_lab(r, g, b)
                C = np.sqrt(a_val**2 + b_val**2)
                h = np.degrees(np.arctan2(b_val, a_val))
                if h < 0: h += 360
                
                row = [float(L), float(C), float(h)]
                if alpha:
                    row.append(float(a))
                results.append(row)
            else:
                results.append([np.nan] * (4 if alpha else 3))
                
        except Exception:
            results.append([np.nan] * (4 if alpha else 3))
            
    # Return as DataFrame to mimic R's matrix with column names
    cols = ['r', 'g', 'b'] if to.lower() == 'rgb' else ['l', 'c', 'h']
    if alpha:
        cols.append('alpha')
    
    return pd.DataFrame(results, columns=cols)

# Main logic
colors_list = ['#43e1f6', 'steelblue', '#67ce9fe4']

# r2py:entity:decode_colour
res1 = decode_colour(colors_list)
# Format to match R matrix output closer (no decimals for RGB)
print(res1.astype(int).to_string(index=False, header=True))

# r2py:entity:decode_colour_1
res2 = decode_colour(colors_list, alpha=True)
# Split RGB to int and alpha to float for printing
rgb_part = res2[['r', 'g', 'b']].astype(int)
alpha_part = res2[['alpha']]
res2_formatted = pd.concat([rgb_part, alpha_part], axis=1)
print(res2_formatted.to_string(index=False, header=True))

# r2py:entity:decode_colour_2
res3 = decode_colour(colors_list, to='lch')
print(res3.to_string(index=False, header=True))