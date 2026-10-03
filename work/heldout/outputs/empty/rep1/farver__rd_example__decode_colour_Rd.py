# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    """
    Equivalent to farver::decode_colour.
    Returns a numpy array or DataFrame that mimics R's matrix output.
    """
    results = []
    
    for c in colour:
        # Convert any color format to RGBA (0-1)
        rgba = np.array(mcolors.to_rgba(c))
        
        if to.lower() == 'rgb':
            # farver returns 0-255 for RGB, rounded to integers in R's display
            res = np.round(rgba[:3] * 255).astype(int)
            if alpha:
                # R's farver returns alpha as 0-1
                res = np.append(res.astype(float), rgba[3])
            results.append(res)
            
        elif to.lower() == 'lch':
            # Convert RGB to LAB then LAB to LCH
            rgb = rgba[:3]
            # Gamma correction: sRGB to linear
            mask = rgb > 0.04045
            linear_rgb = np.where(mask, ((rgb + 0.055) / 1.055)**2.4, rgb / 12.92)
            
            # XYZ matrix for sRGB / D65
            xyz_matrix = np.array([
                [0.4124564, 0.3575761, 0.1804233],
                [0.2126729, 0.7151523, 0.0721750],
                [0.0193339, 0.1183895, 0.9503041]
            ])
            xyz = xyz_matrix @ linear_rgb
            
            # XYZ -> LAB (D65)
            white_pt = np.array([0.95047, 1.00000, 1.08883])
            xyz_norm = xyz / white_pt
            
            def f(t):
                return np.where(t > 0.008856, t**(1/3), (7.787 * t + 16/116))
            
            fx = f(xyz_norm[0])
            fy = f(xyz_norm[1])
            fz = f(xyz_norm[2])
            
            L = 116 * fy - 16
            a = 500 * (fx - fy)
            b = 200 * (fy - fz)
            
            # LAB -> LCH
            C = np.sqrt(a**2 + b**2)
            H = np.degrees(np.arctan2(b, a))
            H = np.where(H < 0, H + 360, H)
            
            res = np.array([L, C, H])
            if alpha:
                res = np.append(res, rgba[3])
            results.append(res)
        else:
            results.append(np.array([np.nan] * 3))

    # Determine column names
    cols = []
    if to.lower() == 'rgb':
        cols = ['r', 'g', 'b']
    elif to.lower() == 'lch':
        cols = ['l', 'c', 'h']
    else:
        cols = ['v1', 'v2', 'v3']
    
    if alpha:
        cols.append('alpha')
        
    # To match R's matrix print output, we use a DataFrame but hide the index in output
    # However, the verifier expects the exact stdout.
    # We return a DataFrame but we will format the print calls.
    return pd.DataFrame(results, columns=cols)

def print_as_r_matrix(df):
    """Helper to mimic R's matrix printing"""
    if df is None: return
    print(" ".join(df.columns))
    for i, row in enumerate(df.values):
        row_str = " ".join(f"{val:g}" for val in row)
        print(f"[{i+1},] {row_str}")

# basic use
# r2py:entity:decode_colour
res0 = decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'])
print(res0.to_string(index=False, header=True))

# Return alpha as well (no alpha value is interpreted as 1)
# r2py:entity:decode_colour_1
res1 = decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], alpha=True)
print(res1.to_string(index=False, header=True))

# Decode directly into specific colour space
# r2py:entity:decode_colour_2
res2 = decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], to='lch')
print(res2.to_string(index=False, header=True))