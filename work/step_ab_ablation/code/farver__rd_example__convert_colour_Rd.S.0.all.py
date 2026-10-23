import numpy as np
import pandas as pd

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
    R's rainbow(n) generates a sequence of colors.
    It corresponds to HSV with S=1, V=1 and H from 0 to 1.
    Returns a matrix of RGB values in [0, 1].
    """
    import colorsys
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append(rgb)
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """
    Translates R farver::decode_colour.
    In this context, rainbow(10) already returns RGB, so decode_colour 
    essentially returns it as a numpy array.
    """
    return np.array(colour)

def as_white_ref(white):
    """Common white references X, Y, Z."""
    white_refs = {
        "D65": np.array([0.950303, 1.000000, 0.825214]), # Standard D65
        "F10": np.array([0.916400, 1.000000, 1.144200]), # Approximation for F10
        "D50": np.array([0.964220, 1.000000, 0.825070]),
    }
    if isinstance(white, str):
        return white_refs.get(white.upper(), white_refs["D65"])
    return np.array(white)

def rgb_to_lab(rgb, white_ref):
    """
    Standard sRGB to CIELAB conversion.
    rgb: array of shape (n, 3) in range [0, 1]
    """
    # sRGB to linear RGB
    rgb = np.array(rgb)
    mask = rgb > 0.04045
    linear_rgb = np.where(mask, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    
    # Linear RGB to XYZ (D65)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = linear_rgb @ matrix.T
    
    # Normalize by white reference
    # The matrix above is for D65. We divide by D65 then multiply by target white_ref.
    d65 = np.array([0.950303, 1.000000, 0.825214])
    xyz = (xyz / d65) * white_ref
    
    # XYZ to Lab
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    xyz_f = f(xyz)
    white_f = f(white_ref)
    
    l = (116 * xyz_f[..., 1]) - 16
    a = 500 * (xyz_f[..., 0] - xyz_f[..., 1])
    b = 200 * (xyz_f[..., 2] - xyz_f[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """
    Converts Lab from one white reference to another.
    Lab(from) -> XYZ(from) -> Lab(to)
    """
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Lab to XYZ
    y = (lab[..., 1] + 16) / 116 # This is incorrect, L is index 0
    # Correcting indices:
    l_val = lab[..., 0]
    a_val = lab[..., 1]
    b_val = lab[..., 2]
    
    f_y = (l_val + 16) / 116
    f_x = a_val / 500 + f_y
    f_z = f_y - b_val / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
    
    xyz = np.stack([f_inv(f_x), f_inv(f_y), f_inv(f_z)], axis=-1) * wp_from
    
    # XYZ to Lab (with wp_to)
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    xyz_norm = xyz / wp_to
    xyz_f = f(xyz_norm)
    white_f = f(np.ones(3)) # since normalized
    
    l = (116 * xyz_f[..., 1]) - 16
    a = 500 * (xyz_f[..., 0] - xyz_f[..., 1])
    b = 200 * (xyz_f[..., 2] - xyz_f[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    
    wp_to = as_white_ref(white_to)
    
    if from_val == 'rgb' and to_val == 'lab':
        res = rgb_to_lab(colour, wp_to)
        return res # Return numpy array to mimic R matrix
    
    if from_val == 'lab' and to_val == 'lab':
        vals = np.array(colour)
        res = lab_to_lab_shift(vals, white_from, white_to)
        return res
        
    return colour

# Execute the translated script
# r2py:entity:spectrum
spectrum = decode_colour(rainbow(10))
# r2py:entity:spec_lab
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
print(spec_lab)

# Convert between different white references
# r2py:entity:spec_lab_1
spec_lab_1 = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(spec_lab_1)