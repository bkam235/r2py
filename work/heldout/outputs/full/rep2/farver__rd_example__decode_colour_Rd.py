import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=np.nan):
    # Handle input as list/array
    if isinstance(colour, str):
        colour = [colour]
    
    # Convert colors to RGBA using matplotlib
    # matplotlib.colors.to_rgba handles hex, named colors (like 'steelblue'), and RGBA
    rgba_list = [mcolors.to_rgba(c) for c in colour]
    rgba_array = np.array(rgba_list) # Shape (N, 4), values 0-1
    
    if to.lower() == 'rgb':
        # R's farver returns RGB as 0-255 integers (or floats)
        rgb_255 = (rgba_array[:, :3] * 255).round().astype(int)
        cols = ['r', 'g', 'b']
        if alpha:
            # R returns alpha as 0-1 float
            res = np.column_stack([rgb_255, rgba_array[:, 3]])
            cols.append('alpha')
        else:
            res = rgb_255
        return pd.DataFrame(res, columns=cols)

    elif to.lower() == 'lch':
        # Manual conversion to LCH via Lab (Standard D65)
        # 1. sRGB to XYZ
        # Simplified sRGB to XYZ (D65)
        def srgb_to_xyz(rgb):
            # Linearize
            rgb = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055)**2.4)
            # Matrix multiplication for D65
            M = np.array([
                [0.4124564, 0.3575761, 0.1804375],
                [0.2126729, 0.7151522, 0.0721750],
                [0.0193339, 0.1183895, 0.9503041]
            ])
            return rgb @ M.T

        xyz = srgb_to_xyz(rgba_array[:, :3])
        
        # 2. XYZ to Lab
        # Reference white D65
        white_ref = np.array([0.95047, 1.00000, 1.08883])
        xyz_norm = xyz / white_ref
        
        def f(t):
            return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t + 16/116))
        
        fx = f(xyz_norm[:, 0])
        fy = f(xyz_norm[:, 1])
        fz = f(xyz_norm[:, 2])
        
        L = (116 * fy) - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)
        
        # 3. Lab to LCH
        C = np.sqrt(a**2 + b**2)
        # h in degrees
        h = np.degrees(np.arctan2(b, a))
        h = np.where(h < 0, h + 360, h)
        
        res = np.column_stack([L, C, h])
        return pd.DataFrame(res, columns=['l', 'c', 'h'])

    else:
        raise ValueError("Unsupported colour space")

# R: decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))
# r2py:entity:decode_colour
res1 = decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'])
print(res1)

# R: decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), alpha = TRUE)
# r2py:entity:decode_colour_1
res2 = decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], alpha=True)
print(res2)

# R: decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), to = 'lch')
# r2py:entity:decode_colour_2
res3 = decode_colour(['#43e1f6', 'steelblue', '#67ce9fe4'], to='lch')
print(res3)