# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from matplotlib import colors

# r2py:entity:decode_colour
def rgb_to_xyz(rgb):
    """
    Convert sRGB [0, 255] to CIE XYZ (D65).
    farver uses the sRGB standard.
    """
    # Normalize to [0, 1]
    rgb = np.array(rgb) / 255.0
    
    # Inverse gamma correction (sRGB)
    mask = rgb > 0.04045
    rgb[mask] = ((rgb[mask] + 0.055) / 1.055)**2.4
    rgb[~mask] = rgb[~mask] / 12.92
    
    # Matrix for sRGB to XYZ (D65)
    # These coefficients are standard for sRGB
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804233],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503040]
    ])
    
    if rgb.ndim == 1:
        return np.dot(matrix, rgb)
    else:
        return np.dot(rgb, matrix.T)

def xyz_to_lab(xyz):
    """Convert CIE XYZ to CIE L*a*b* (D65)."""
    # D65 Reference White
    white = np.array([0.95047, 1.00000, 1.08883])
    
    xyz = np.array(xyz)
    if xyz.ndim == 1:
        xyz = xyz.reshape(1, -1)
        is_single = True
    else:
        is_single = False
        
    xyz_norm = xyz / white
    
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    fx = f(xyz_norm[:, 0])
    fy = f(xyz_norm[:, 1])
    fz = f(xyz_norm[:, 2])
    
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    
    res = np.stack([L, a, b], axis=-1)
    return res[0] if is_single else res

def lab_to_lch(lab):
    """Convert CIE L*a*b* to CIE L*C*h*."""
    lab = np.array(lab)
    if lab.ndim == 1:
        L = lab[0]
        a = lab[1]
        b = lab[2]
        C = np.sqrt(a**2 + b**2)
        h = np.degrees(np.arctan2(b, a))
        if h < 0: h += 360
        return np.array([L, C, h])
    else:
        L = lab[:, 0]
        a = lab[:, 1]
        b = lab[:, 2]
        C = np.sqrt(a**2 + b**2)
        h = np.degrees(np.arctan2(b, a))
        h = np.where(h < 0, h + 360, h)
        return np.stack([L, C, h], axis=-1)

# Equivalent to farver::decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=np.nan):
    colours_input = np.atleast_1d(colour)
    results = []
    
    for c in colours_input:
        # Convert name or hex to RGBA (0-1 range)
        rgba = colors.to_rgba(c)
        rgb_255 = np.array(rgba[:3]) * 255
        
        if to.lower() == 'rgb':
            val = rgb_255
            if alpha:
                val = np.append(val, rgba[3])
        elif to.lower() == 'lch':
            xyz = rgb_to_xyz(rgb_255)
            lab = xyz_to_lab(xyz)
            val = lab_to_lch(lab)
            if alpha:
                val = np.append(val, rgba[3])
        else:
            # Fallback to RGB
            val = rgb_255
            if alpha:
                val = np.append(val, rgba[3])
        
        results.append(val)
    
    # Define column names
    dims = {'rgb': ['r', 'g', 'b'], 'lch': ['l', 'c', 'h']}
    cols = dims.get(to.lower(), ['v1', 'v2', 'v3'])
    if alpha:
        cols = cols + ['alpha']
        
    df = pd.DataFrame(results, columns=cols)
    # To match R's integer output for RGB
    if to.lower() == 'rgb' and not alpha:
        df = df.astype(int)
        
    return df

# Input data
colours_list = ['#43e1f6', 'steelblue', '#67ce9fe4']

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))
# r2py:entity:decode_colour
print(decode_colour(colours_list))

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), alpha = TRUE)
# r2py:entity:decode_colour_1
print(decode_colour(colours_list, alpha=True))

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), to = 'lch')
# r2py:entity:decode_colour_2
print(decode_colour(colours_list, to='lch'))