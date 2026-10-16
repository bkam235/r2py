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
    # R's rainbow() uses a specific hue sequence from 0 to 1.
    # For n=10, hues are 0, 0.1, 0.2, ..., 0.9 (approx)
    # But it's essentially hsv(h=seq(0, 1, length.out=n), s=1, v=1)
    # However, the exact RGB values in R's rainbow() are based on sRGB.
    # The R output provided: [255, 0, 0], [255, 153, 0], [204, 255, 0]...
    # This suggests a linear interpolation in hue.
    res = []
    for i in range(n):
        h = i / n # R's rainbow() doesn't wrap the end point unless specified
        # Using colorsys.hsv_to_rgb
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        # Convert to 0-255 and round
        res.append([int(round(c * 255)) for c in rgb])
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([0.950303, 1.000000, 1.088840]),
        "F10": np.array([0.916400, 1.000000, 1.144200]),
        "D50": np.array([0.964212, 1.000000, 0.825188]),
    }
    if isinstance(white, str):
        return white_refs.get(white.upper(), white_refs["D65"])
    return np.array(white)

def rgb_to_lab(rgb, white_ref):
    """Helper to convert RGB [0-255] to Lab."""
    rgb = np.array(rgb) / 255.0
    
    # sRGB to Linear RGB
    mask = rgb > 0.04045
    rgb_lin = np.where(mask, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    
    # Linear RGB to XYZ (D65)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = rgb_lin @ matrix.T
    
    # Normalize by D65 and scale by target white_ref
    d65 = np.array([0.950303, 1.000000, 1.088840])
    xyz = (xyz / d65) * white_ref
    
    # XYZ to Lab
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz)
    f_white = f(white_ref)
    
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """Helper to shift Lab values between white references."""
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Lab -> XYZ(wp_from)
    y = (lab[:, 1] + 16) / 116 # This is actually L
    # Wait, indices for lab are [L, a, b]
    l_val = lab[:, 0]
    a_val = lab[:, 1]
    b_val = lab[:, 2]
    
    y_val = (l_val + 16) / 116
    x_val = a_val / 500 + y_val
    z_val = y_val - b_val / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
    
    xyz = np.stack([f_inv(x_val), f_inv(y_val), f_inv(z_val)], axis=-1) * wp_from
    
    # XYZ(wp_from) -> Lab(wp_to)
    xyz_norm = xyz / wp_to
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz_norm)
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    
    wp_to = as_white_ref(white_to)
    
    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        return rgb_to_lab(colour, wp_to)
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
        return lab_to_lab_shift(vals, white_from, white_to)
        
    return np.array(colour)

# Execute
spectrum = decode_colour(rainbow(10))
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
print(spec_lab)

res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(res_white)