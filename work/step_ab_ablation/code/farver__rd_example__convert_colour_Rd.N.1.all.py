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
    Approximate R's rainbow(n). 
    R's rainbow(n) returns a matrix of RGB values in [0, 1].
    """
    import colorsys
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow is essentially HSV with S=1, V=1
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append(list(rgb))
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """
    Translates R farver::decode_colour.
    In this context, it primarily ensures the input is a numpy array of RGB values.
    """
    return np.array(colour)

def as_white_ref(white):
    """
    Returns XYZ white point for given reference.
    Standard values used by farver/colC.
    """
    white_refs = {
        "D65": np.array([0.95030, 1.00000, 1.08883]),
        "F10": np.array([0.91640, 1.00000, 1.14420]),
        "D50": np.array([0.96422, 1.00000, 1.00000]),
    }
    if isinstance(white, str):
        return white_refs.get(white.upper(), white_refs["D65"])
    return np.array(white)

def f_lab(t):
    return np.where(t > 0.00885645167, np.power(t, 1/3), (7.787037 * t) + (16/116))

def f_lab_inv(t):
    return np.where(t**3 > 0.00885645167, t**3, (t - 16/116) / 7.787037)

def rgb_to_lab(rgb, white_ref):
    """
    sRGB [0, 1] -> Lab conversion.
    """
    # Gamma correction
    mask = rgb > 0.04045
    rgb_lin = np.where(mask, ((rgb[mask] + 0.055) / 1.055)**2.4, rgb[~mask] / 12.92)
    
    # RGB to XYZ (D65)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = rgb_lin @ matrix.T
    
    # Convert to Lab using provided white reference
    # Standard farver/colC logic: XYZ/white_ref
    white_ref_norm = white_ref / white_ref[1] # Normalize Y=1
    xyz_norm = xyz / white_ref_norm
    
    f_xyz = f_lab(xyz_norm)
    f_white = f_lab(white_ref_norm / white_ref_norm[1]) # This is always f_lab([1,1,1]) approx
    
    # Re-calculating f_white properly
    f_w = f_lab(np.array([1.0, 1.0, 1.0])) # simplified since we normalized by white_ref
    
    # But wait, the standard formula is L = 116 * f(Y/Yw) - 16
    # Here Y/Yw is xyz_norm[:, 1]
    l = 116 * f_xyz[..., 1] - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_xyz(lab, white_ref):
    """
    Lab -> XYZ conversion.
    """
    l, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200
    
    xyz_norm = np.stack([f_lab_inv(x), f_lab_inv(y), f_lab_inv(z)], axis=-1)
    
    white_ref_norm = white_ref / white_ref[1]
    return xyz_norm * white_ref_norm

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Handle input type
    if isinstance(colour, pd.DataFrame):
        vals = colour.values
    else:
        vals = np.array(colour)

    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        res = rgb_to_lab(vals, wp_to)
        return pd.DataFrame(res, columns=['L', 'a', 'b'])
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        # Convert Lab(from) -> XYZ -> Lab(to)
        xyz = lab_to_xyz(vals, wp_from)
        
        white_ref_to_norm = wp_to / wp_to[1]
        xyz_norm = xyz / white_ref_to_norm
        f_xyz = f_lab(xyz_norm)
        
        l = 116 * f_xyz[..., 1] - 16
        a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
        b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
        res = np.stack([l, a, b], axis=-1)
        return pd.DataFrame(res, columns=['L', 'a', 'b'])
        
    return colour

# Execute the translated script
# r2py:entity:spectrum
spectrum = decode_colour(rainbow(10))
# r2py:entity:spec_lab
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
print(spec_lab)

# Convert between different white references
# r2py:entity:spec_lab_1
res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(res_white)