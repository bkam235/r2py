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
    """
    Approximate R's rainbow(n) function.
    R's rainbow(n) uses h = seq(0, 1, length.out = n) and converts HSV to RGB.
    """
    res = []
    for i in range(n):
        # R's seq(0, 1, length.out=10) gives 0, 0.111, 0.222, ..., 1.0
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow is basically HSV(h, 1, 1)
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append([round(c * 255) for c in rgb])
    return res

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    # In farver, decode_colour converts various formats to a numeric matrix.
    # For rainbow() output (list of lists), it's already numeric RGB.
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([95.0301, 100.0, 108.883]),
        "F10": np.array([91.64, 100.0, 114.42]),
        "D50": np.array([96.422, 100.0, 100.0]),
    }
    if isinstance(white, str):
        val = white_refs.get(white.upper())
        if val is None:
            raise ValueError("Unknown white reference")
        return val
    return np.array(white)

def rgb_to_xyz(rgb):
    """sRGB to XYZ (D65)."""
    rgb = np.array(rgb) / 255.0
    mask = rgb > 0.04045
    rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb[~mask] = rgb[~mask] / 12.92
    
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = rgb @ matrix.T * 100.0
    return xyz

def xyz_to_lab(xyz, white_ref):
    """XYZ to Lab."""
    xyz = np.array(xyz)
    white_ref = np.array(white_ref)
    xyz_norm = xyz / white_ref
    
    def f(t):
        return np.where(t > 0.008856451, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz_norm)
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_xyz(lab, white_ref):
    """Lab to XYZ."""
    lab = np.array(lab)
    white_ref = np.array(white_ref)
    l, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856451, t**3, (t - 16/116) / 7.787)
    
    xyz = np.stack([f_inv(x), f_inv(y), f_inv(z)], axis=-1)
    return xyz * white_ref

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
    
    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        # sRGB is typically assumed to be based on D65
        xyz = rgb_to_xyz(vals)
        res = xyz_to_lab(xyz, wp_to)
        return res
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        xyz = lab_to_xyz(vals, wp_from)
        res = xyz_to_lab(xyz, wp_to)
        return res
    return vals

# Execute the translated script
# r2py:entity:spectrum
spectrum = decode_colour(rainbow(10))

# r2py:entity:spec_lab
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
# R auto-prints spec_lab
print(pd.DataFrame(spec_lab, columns=['l', 'a', 'b']))

# Convert between different white references
# r2py:entity:convert_colour
# r2py:entity:spec_lab_1
spec_lab_1 = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(pd.DataFrame(spec_lab_1, columns=['l', 'a', 'b']))