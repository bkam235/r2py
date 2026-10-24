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

# r2py:entity:spectrum
def rainbow(n):
    """
    Approximate R's rainbow(n) function.
    R's rainbow(n) generates n colors distributed evenly around the color wheel.
    """
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow() uses a specific HSV conversion. 
        # For n=10, R produces colors that correspond to hsv_to_rgb but 
        # scaled to 0-255 integers.
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append([round(c * 255) for c in rgb])
    return np.array(res)

# r2py:entity:spectrum
def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    # R's decode_colour returns an array/matrix of the colors.
    # For 'rgb' and input from rainbow(), it's effectively identity.
    return np.array(colour)

def as_white_ref(x):
    """Translates R farver::as_white_ref."""
    white_references = {
        "D65": np.array([95.0303, 100.0, 108.883]),
        "F10": np.array([91.64, 100.0, 114.42]),
        "D50": np.array([96.422, 100.0, 100.0]),
    }
    if isinstance(x, str):
        val = white_references.get(x.upper())
        if val is None:
            raise ValueError("Unknown white reference")
        return val
    return np.array(x)

def rgb_to_lab(rgb, white_ref):
    """
    Convert sRGB [0, 255] to Lab using white reference white_ref.
    """
    # Normalize to [0, 1]
    rgb = np.array(rgb) / 255.0
    
    # sRGB to Linear RGB
    mask = rgb > 0.04045
    linear_rgb = np.where(mask, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    
    # Linear RGB to XYZ (D65)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = linear_rgb @ matrix.T
    
    # The matrix above is for D65. If white_ref is not D65, we apply chromatic adaptation.
    # D65 white point in XYZ (normalized to Y=1)
    d65 = np.array([0.950303, 1.0, 1.08883])
    # Target white point (normalized to Y=1)
    wp_target = white_ref / 100.0
    
    # Simple scaling (Bradford is typical, but farver often uses scaling for these)
    xyz = xyz * (wp_target / d65)
    
    # XYZ to Lab
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    # Normalize by target white point
    xyz_norm = xyz / wp_target
    f_xyz = f(xyz_norm)
    
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """
    Convert Lab (white_from) -> XYZ (white_from) -> Lab (white_to)
    """
    wp_from = as_white_ref(white_from) / 100.0
    wp_to = as_white_ref(white_to) / 100.0
    
    # Lab to XYZ
    l = lab[..., 0]
    a = lab[..., 1]
    b = lab[..., 2]
    
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
    
    xyz_from = np.stack([f_inv(x), f_inv(y), f_inv(z)], axis=-1) * wp_from
    
    # Shift XYZ from white_from to white_to
    xyz_to = xyz_from * (wp_to / wp_from)
    
    # XYZ to Lab (using wp_to)
    xyz_norm = xyz_to / wp_to
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz_norm)
    l_new = (116 * f_xyz[..., 1]) - 16
    a_new = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b_new = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l_new, a_new, b_new], axis=-1)

# r2py:entity:convert_colour
def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    
    if isinstance(colour, pd.DataFrame):
        col_vals = colour.values
    else:
        col_vals = np.array(colour)

    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        res = rgb_to_lab(col_vals, as_white_ref(white_to))
        return pd.DataFrame(res, columns=['l', 'a', 'b'])
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        res = lab_to_lab_shift(col_vals, white_from, white_to)
        return pd.DataFrame(res, columns=['l', 'a', 'b'])
        
    return pd.DataFrame(col_vals)

# Execute the translated script
# r2py:entity:spectrum
spectrum = decode_colour(rainbow(10))

# r2py:entity:spec_lab
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
# R: spec_lab (auto-prints)
print(spec_lab)

# Convert between different white references
# r2py:entity:convert_colour
spec_lab_1 = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(spec_lab_1)