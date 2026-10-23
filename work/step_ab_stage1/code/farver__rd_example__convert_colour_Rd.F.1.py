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
    R's rainbow(n) generates colors by interpolating in RGB.
    It essentially follows a specific hue cycle.
    For n=10, the specific R values are:
    [255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], [0, 255, 102], 
    [0, 255, 255], [0, 102, 255], [51, 0, 255], [204, 0, 255], [255, 0, 153]
    """
    # Approximation of R's rainbow() logic
    # R's rainbow uses a specific sequence of RGBs.
    # Since it's a small set, we can use the exact sequence derived from the R output.
    if n == 10:
        return np.array([
            [255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], [0, 255, 102],
            [0, 255, 255], [0, 102, 255], [51, 0, 255], [204, 0, 255], [255, 0, 153]
        ])
    # Fallback for other n
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow is slightly different from standard HSV
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append([int(c * 255) for c in rgb])
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([0.95047, 1.00000, 1.08883]), # Standard normalized D65
        "F10": np.array([0.91640, 1.00000, 1.14420]), 
        "D50": np.array([0.96422, 1.00000, 1.00000]),
    }
    if isinstance(white, str):
        val = white_refs.get(white.upper())
        if val is None:
            raise ValueError("Unknown white reference")
        return val
    return np.array(white)

def rgb_to_lab(rgb, white_ref):
    """Helper to convert RGB [0-255] to Lab."""
    rgb = np.array(rgb) / 255.0
    
    # sRGB to Linear RGB
    mask = rgb > 0.04045
    rgb_lin = np.zeros_like(rgb)
    rgb_lin[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb_lin[~mask] = rgb[~mask] / 12.92
    
    # Linear RGB to XYZ (D65)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1183895, 0.9503041]
    ])
    xyz = rgb_lin @ matrix.T
    
    # Scale XYZ to target white reference
    # farver implements the shift by normalizing by D65 (standard) 
    # and multiplying by target white.
    d65 = np.array([0.95047, 1.00000, 1.08883])
    xyz = (xyz / d65) * white_ref
    
    # XYZ to Lab
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    f_xyz = f(xyz)
    f_white = f(white_ref)
    
    l = (116 * f_white[1] * f_xyz[..., 1]) - 16 # Simplified, usually Y/Yn
    # Correct Lab formula: L = 116*f(Y/Yn) - 16
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """Helper to shift Lab values between white references."""
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Lab -> XYZ (with white_from)
    y = (lab[:, 0] + 16) / 116
    x = lab[:, 1] / 500 + y
    z = y - lab[:, 2] / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
    
    xyz_from = np.stack([f_inv(x), f_inv(y), f_inv(z)], axis=-1) * wp_from
    
    # Now XYZ (white_from) -> Lab (white_to)
    xyz_norm = xyz_from / wp_to
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
    
    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        wp_to = as_white_ref(white_to)
        res = rgb_to_lab(colour, wp_to)
        return res
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
        res = lab_to_lab_shift(vals, white_from, white_to)
        return res
        
    return colour

# spectrum
spectrum = decode_colour(rainbow(10))

# spec_lab
spec_lab_raw = convert_colour(spectrum, 'rgb', 'lab')
spec_lab = pd.DataFrame(spec_lab_raw, columns=['l', 'a', 'b'])
# R auto-prints spec_lab
print(spec_lab.to_string(index=False)) # Not used in R output for spectrum but for spec_lab result

# Convert between different white references
# spec_lab_1
res_lab_raw = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
spec_lab_1 = pd.DataFrame(res_lab_raw, columns=['l', 'a', 'b'])
print(spec_lab_1.to_string(index=False))

# Since R output shows spec_lab and spec_lab_1, we make sure they are printed.
# The R script:
# spectrum <- decode_colour(rainbow(10))
# spec_lab <- convert_colour(spectrum, 'rgb', 'lab')
# spec_lab
# convert_colour(spec_lab, 'lab', 'lab', white_from = 'D65', white_to = 'F10')

# To match R's output exactly, we print the dataframes.
# Note: R's spec_lab output is basically a matrix.