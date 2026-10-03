# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from matplotlib import colors

# r2py:entity:decode_colour
def rgb_to_lab(rgb):
    """Convert RGB [0, 255] to Lab."""
    # Normalize to [0, 1]
    rgb = np.array(rgb) / 255.0
    # Linearize RGB
    mask = rgb > 0.04045
    rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb[~mask] = rgb[~mask] / 12.92
    
    # RGB to XYZ (D65)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804233],
        [0.2126729, 0.7151523, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = rgb @ matrix.T
    
    # XYZ to Lab (D65)
    ref = np.array([0.95047, 1.00000, 1.08883])
    xyz = xyz / ref
    
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t + 16/116))
    
    fx = f(xyz[:, 0])
    fy = f(xyz[:, 1])
    fz = f(xyz[:, 2])
    
    l = (116 * fy) - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return np.stack([l, a, b], axis=1)

def lab_to_lch(lab):
    """Convert Lab to LCH."""
    l = lab[:, 0]
    a = lab[:, 1]
    b = lab[:, 2]
    
    c = np.sqrt(a**2 + b**2)
    h = np.degrees(np.arctan2(b, a))
    h = np.where(h < 0, h + 360, h)
    
    return np.stack([l, c, h], axis=1)

def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=np.nan):
    # Map input colors to RGBA (0-1)
    rgba_list = [colors.to_rgba(c) for c in colour]
    rgba = np.array(rgba_list)
    
    if to.lower() == 'rgb':
        res = (rgba[:, :3] * 255).round().astype(int)
        cols = ['r', 'g', 'b']
        if alpha:
            res = np.column_stack([res, rgba[:, 3]])
            cols.append('alpha')
        df = pd.DataFrame(res, columns=cols)
        return df

    elif to.lower() == 'lch':
        # Convert to LCH using the pipeline
        rgb_255 = rgba[:, :3] * 255
        lab = rgb_to_lab(rgb_255)
        lch = lab_to_lch(lab)
        cols = ['l', 'c', 'h']
        if alpha:
            lch = np.column_stack([lch, rgba[:, 3]])
            cols.append('alpha')
        df = pd.DataFrame(lch, columns=cols)
        return df
    
    else:
        raise ValueError("Unknown colour space")

# Input data
cols_list = ['#43e1f6', 'steelblue', '#67ce9fe4']

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))
print(decode_colour(cols_list))

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), alpha = TRUE)
# r2py:entity:decode_colour_1
print(decode_colour(cols_list, alpha=True))

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), to = 'lch')
# r2py:entity:decode_colour_2
print(decode_colour(cols_list, to='lch'))