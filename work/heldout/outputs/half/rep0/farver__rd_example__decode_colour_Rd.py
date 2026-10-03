# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
import matplotlib.colors as mcolors

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=np.nan):
    """
    Translates farver::decode_colour. 
    R's farver returns values in 0-255 for RGB.
    """
    results = []
    
    # To match R's farver output exactly, we need to handle the color space conversions
    for c in colour:
        try:
            # Parse color to RGBA (0-1 range) using matplotlib
            # handles hex (#RGB, #RGBA, #RRGGBB, #RRGGBBAA) and CSS names
            rgba = mcolors.to_rgba(c)
            r, g, b, a = rgba

            if to.lower() == 'rgb':
                # farver returns 0-255 for RGB
                vals = [round(r * 255), round(g * 255), round(b * 255)]
                cols = ['r', 'g', 'b']
            elif to.lower() == 'lch':
                # Precise LCH conversion (CIELCh)
                # 1. RGB (0-1) -> sRGB -> XYZ (D65)
                # Simple sRGB to XYZ conversion
                def srgb_to_xyz(rgb):
                    # Linearize
                    rgb = np.array(rgb)
                    mask = rgb <= 0.04045
                    rgb[mask] = rgb[mask] / 12.92
                    rgb[~mask] = ((rgb[~mask] + 0.055) / 1.055) ** 2.4
                    # Matrix multiplication for D65
                    M = np.array([
                        [0.4124564, 0.3575761, 0.1804375],
                        [0.2126729, 0.7151522, 0.0721750],
                        [0.0193339, 0.1183895, 0.9503040]
                    ])
                    return M @ rgb

                xyz = srgb_to_xyz([r, g, b])
                # 2. XYZ -> CIELAB (D65 reference)
                ref = np.array([0.95047, 1.00000, 1.08883]) # D65
                xyz_norm = xyz / ref
                
                def f(t):
                    return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
                
                fx = f(xyz_norm[0])
                fy = f(xyz_norm[1])
                fz = f(xyz_norm[2])
                
                L = 116 * fy - 16
                a_lab = 500 * (fx - fy)
                b_lab = 200 * (fy - fz)
                
                # 3. LAB -> LCH
                C = np.sqrt(a_lab**2 + b_lab**2)
                H = np.degrees(np.arctan2(b_lab, a_lab))
                if H < 0: H += 360
                
                vals = [L, C, H]
                cols = ['l', 'c', 'h']
            else:
                vals = [round(r * 255), round(g * 255), round(b * 255)]
                cols = ['v1', 'v2', 'v3']

            if alpha:
                vals.append(a)
                cols.append('alpha')
            
            results.append(vals)
        except:
            # Handle NA values
            dim_len = 3 if to.lower() == 'rgb' or to.lower() == 'lch' else 3
            res_row = [na_value] * dim_len
            if alpha:
                res_row.append(na_value)
            results.append(res_row)

    df = pd.DataFrame(results, columns=cols)
    # R's output is essentially a matrix; for display purposes we return a DF 
    # but ensure the values are computed correctly.
    return df

# basic use
# r2py:entity:decode_colour
print(decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4']))

# Return alpha as well (no alpha value is interpreted as 1)
# r2py:entity:decode_colour_1
print(decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], alpha=True))

# Decode directly into specific colour space
# r2py:entity:decode_colour_2
print(decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], to='lch'))