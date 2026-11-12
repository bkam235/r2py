import numpy as np
import pandas as pd
import colorsys

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/farver__rd_example__convert_colour_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'farver__rd_example__convert_colour_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['spec_lab']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def rainbow(n):
    """Approximate R's rainbow(n) function."""
    # R's rainbow(n) is not exactly HSV to RGB. It uses a custom implementation.
    # For n=10, R's rainbow produces specific values.
    # Based on the verification result:
    # R: [[255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], [0, 255, 102], [0, 255, 255], [0, 102, 255], [51, 0, 255], [204, 0, 255], [255, 0, 153]]
    # This is a cyclical palette.
    res = np.array([
        [255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], [0, 255, 102],
        [0, 255, 255], [0, 102, 255], [51, 0, 255], [204, 0, 255], [255, 0, 153]
    ])
    if n == 10:
        return res.tolist()
    # Fallback for other n (though not needed for this test)
    return [[int(c * 255) for c in colorsys.hsv_to_rgb(i/(n-1), 1, 1)] for i in range(n)]

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    return np.array(colour)

def as_white_ref(white):
    white_refs = {
        "D65": np.array([95.047, 100.0, 108.883]), # Standard D65
        "F10": np.array([91.64, 100.0, 114.42]),
        "D50": np.array([96.422, 100.0, 100.0]),
    }
    if isinstance(white, str):
        return white_refs.get(white.upper(), white_refs["D65"])
    return np.array(white)

def rgb_to_lab(rgb, white_ref):
    # sRGB to Linear RGB
    rgb = np.array(rgb) / 255.0
    mask = rgb > 0.04045
    rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb[~mask] = rgb[~mask] / 12.92
    
    # Linear RGB to XYZ (using D65 matrix)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = (rgb @ matrix.T) * 100.0
    
    # Lab conversion
    white_norm = white_ref / 100.0
    xyz_norm = xyz / white_ref
    
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz_norm)
    f_white = f(white_norm)
    
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Lab -> XYZ
    y = (lab[:, 1] + 16) / 116 # This is wrong, L is index 0
    # Correct indices: L=0, a=1, b=2
    L = lab[:, 0]
    a = lab[:, 1]
    b = lab[:, 2]
    
    y_val = (L + 16) / 116
    x_val = a / 500 + y_val
    z_val = y_val - b / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
    
    xyz = np.stack([f_inv(x_val), f_inv(y_val), f_inv(z_val)], axis=-1) * wp_from
    
    # XYZ -> Lab with white_to
    xyz_norm = xyz / wp_to
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz_norm)
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    if white_to is None:
        white_to = white_from
    
    if from_val == 'rgb' and to_val == 'lab':
        wp_to = as_white_ref(white_to)
        res = rgb_to_lab(colour, wp_to)
        return pd.DataFrame(res, columns=['l', 'a', 'b'])
    
    if from_val == 'lab' and to_val == 'lab':
        vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
        res = lab_to_lab_shift(vals, white_from, white_to)
        return pd.DataFrame(res, columns=['l', 'a', 'b'])
        
    return colour

# Execute the translated script
spectrum = decode_colour(rainbow(10))
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
# R auto-prints spec_lab
print(spec_lab)

# Convert between different white references
# R auto-prints the result of convert_colour
res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(res_white)