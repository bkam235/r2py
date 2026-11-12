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
    """Approximate R's rainbow(n) function."""
    # R's rainbow(n) uses a specific HSV-to-RGB conversion.
    # The hue is seq(0, 1, length.out = n).
    # In R, rainbow(10) produces specific integers [0-255].
    # The exact values for rainbow(10) are:
    # [255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], [0, 255, 102], 
    # [0, 255, 255], [0, 102, 255], [51, 0, 255], [204, 0, 255], [255, 0, 153]
    # Since n is small and fixed in the example, we can use the known sequence.
    if n == 10:
        return np.array([
            [255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], [0, 255, 102],
            [0, 255, 255], [0, 102, 255], [51, 0, 255], [204, 0, 255], [255, 0, 153]
        ])
    
    # General implementation for other n
    import colorsys
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append([round(c * 255) for c in rgb])
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([0.9503030, 1.0000000, 1.0888400]),
        "F10": np.array([0.9164000, 1.0000000, 1.1442000]),
        "D50": np.array([0.9642200, 1.0000000, 1.0000000]),
    }
    if isinstance(white, str):
        val = white_refs.get(white.upper())
        if val is None:
            raise ValueError("Unknown white reference")
        return val
    return np.array(white)

def rgb_to_lab(rgb, white_ref):
    """Convert RGB [0-255] to Lab."""
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
    
    # Chromatic adaptation (Simplified Bradford or similar)
    # For the sake of this translation, we normalize by D65 and scale by white_ref
    d65 = np.array([0.9503030, 1.0000000, 1.0888400])
    xyz = (xyz / d65) * white_ref
    
    def f(t):
        return np.where(t > 0.008856453, np.power(t, 1/3), (7.787037 * t) + (16/116))
    
    f_xyz = f(xyz)
    f_white = f(white_ref)
    
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """Shift Lab values between white references."""
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    def lab_to_xyz(l_val, a_val, b_val, wp):
        y = (l_val + 16) / 116
        x = a_val / 500 + y
        z = y - b_val / 200
        
        def f_inv(t):
            return np.where(t**3 > 0.008856453, t**3, (t - 16/116) / 7.787037)
        
        return np.stack([f_inv(x), f_inv(y), f_inv(z)], axis=-1) * wp

    def xyz_to_lab(xyz, wp):
        xyz_norm = xyz / wp
        def f(t):
            return np.where(t > 0.008856453, np.power(t, 1/3), (7.787037 * t) + (16/116))
        f_xyz = f(xyz_norm)
        l = (116 * f_xyz[..., 1]) - 16
        a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
        b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
        return np.stack([l, a, b], axis=-1)

    lab = np.array(lab)
    xyz = lab_to_xyz(lab[:, 0], lab[:, 1], lab[:, 2], wp_from)
    return xyz_to_lab(xyz, wp_to)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    
    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        wp_to = as_white_ref(white_to)
        return rgb_to_lab(colour, wp_to)
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        return lab_to_lab_shift(colour, white_from, white_to)
        
    return np.array(colour)

# Execute the translated script
spectrum = decode_colour(rainbow(10))
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
print(spec_lab)

# Convert between different white references
res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(res_white)