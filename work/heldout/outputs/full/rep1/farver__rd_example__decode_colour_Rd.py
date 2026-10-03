# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=np.nan):
    """
    Equivalent to farver::decode_colour. 
    Translates color strings (hex, named) to specified color spaces.
    """
    if isinstance(colour, str):
        colour = [colour]
    
    # White references (Tristimulus)
    white_refs = {
        'D65': np.array([95.047, 100.000, 108.883]),
        'D50': np.array([96.422, 100.000, 82.518]),
    }
    
    white_val = white_refs.get(white.upper(), np.array([95.047, 100.000, 108.883]))
    
    results = []
    cols = []
    
    for c in colour:
        try:
            # mcolors.to_rgba handles hex and named colors
            rgba = mcolors.to_rgba(c)
            rgb = np.array(rgba[:3])
            
            if to.lower() == 'rgb':
                # farver returns RGB in [0, 255]
                res = np.round(rgb * 255).astype(float)
                if alpha:
                    res = np.append(res, rgba[3])
                results.append(res)
                cols = ['r', 'g', 'b'] + (['alpha'] if alpha else [])
            
            elif to.lower() == 'lch':
                # sRGB to linear RGB
                mask = rgb > 0.04045
                lin_rgb = np.where(mask, ((rgb + 0.055) / 1.055)**2.4, rgb / 12.92)
                
                # Linear RGB to XYZ (D65)
                matrix = np.array([
                    [0.4124564, 0.3575761, 0.1804233],
                    [0.2126729, 0.7151523, 0.0721750],
                    [0.0193339, 0.1183895, 0.9503041]
                ])
                xyz = matrix @ lin_rgb
                # scale to 100 for consistency with white_val
                xyz = xyz * 100
                
                # XYZ to Lab
                # Normalize by white point
                xyz_norm = xyz / white_val
                
                def f(t):
                    return t**(1/3) if t > 0.00885645167 else (7.787 * t + 16/116)
                
                f_xyz = np.array([f(x) for x in xyz_norm])
                L = 116 * f_xyz[1] - 16
                a = 500 * (f_xyz[0] - f_xyz[1])
                b = 200 * (f_xyz[2] - f_xyz[1])
                
                # Lab to LCH
                C = np.sqrt(a**2 + b**2)
                h = np.degrees(np.arctan2(b, a))
                if h < 0: h += 360
                
                res = np.array([L, C, h])
                if alpha:
                    res = np.append(res, rgba[3])
                results.append(res)
                cols = ['l', 'c', 'h'] + (['alpha'] if alpha else [])
            else:
                raise ValueError(f"Color space {to} not supported")
        except:
            dim = 3 + (1 if alpha else 0)
            results.append([na_value] * dim)
            if not cols: cols = ['r', 'g', 'b'] + (['alpha'] if alpha else [])
            
    df = pd.DataFrame(results, columns=cols)
    return df

def print_as_r_matrix(df):
    """Helper to mimic R matrix print output"""
    output = []
    # Header
    header = " ".join(f"{col:>8}" for col in df.columns)
    output.append(f"    {header}")
    # Rows
    for i, row in enumerate(df.values):
        row_str = " ".join(f"{val:8.5g}" if isinstance(val, float) else f"{val:8g}" for val in row)
        output.append(f"[{i+1},] {row_str}")
    return "\n".join(output)

# Main execution
colors_list = ['#43e1f6', 'steelblue', '#67ce9fe4']

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))
# r2py:entity:decode_colour
decode_colour_res = decode_colour(colors_list)
print(print_as_r_matrix(decode_colour_res))

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), alpha = TRUE)
# r2py:entity:decode_colour_1
decode_colour_res_1 = decode_colour(colors_list, alpha=True)
print(print_as_r_matrix(decode_colour_res_1))

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), to = 'lch')
# r2py:entity:decode_colour_2
decode_colour_res_2 = decode_colour(colors_list, to='lch')
print(print_as_r_matrix(decode_colour_res_2))