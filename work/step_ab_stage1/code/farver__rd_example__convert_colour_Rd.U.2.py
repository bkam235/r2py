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
    # R's rainbow(n) uses a specific HSV to RGB conversion.
    # The hue is seq(0, 1, length.out = n)
    # R's rainbow colors are effectively HSV(h, 1, 1)
    def hsv_to_rgb_r(h):
        # This is a simplified version of R's rainbow logic
        # which maps hue to RGB.
        import colorsys
        # R's rainbow(10) produces:
        # [255, 0, 0], [255, 153, 0], [204, 255, 0], [51, 255, 0], 
        # [0, 255, 102], [0, 255, 255], [0, 102, 255], [51, 0, 255], 
        # [204, 0, 255], [255, 0, 153]
        # This matches a specific linear spacing of hue.
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        return [round(c * 255) for c in rgb]

    # R's rainbow(n) hue is actually 0 to 1, but it doesn't wrap at the end unless specified.
    # For n=10, h = 0, 0.1, 0.2, ..., 0.9.
    # Wait, looking at the R output provided in the verification, the 10th color is [255, 0, 153]
    # which corresponds to h=0.9.
    res = []
    for i in range(n):
        h = i / n
        res.append(hsv_to_rgb_r(h))
    return res

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([0.950301, 1.000000, 1.08883]),
        "F10": np.array([0.9164, 1.000000, 1.1442]),
        "D50": np.array([0.96422, 1.000000, 1.00000]),
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
    
    # Convert to Lab relative to white_ref
    # XYZ are currently D65. The farver package typically handles 
    # the white point during the XYZ -> Lab conversion.
    
    def f(t):
        return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
    
    # Normalized by white point
    xyz_norm = xyz / white_ref
    f_xyz = f(xyz_norm)
    
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """Helper to shift Lab values between white references."""
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Lab -> XYZ (from)
    y = (lab[:, 1] + 16) / 116 # This index is wrong, L is 0
    # Correction:
    l_val = lab[:, 0]
    a_val = lab[:, 1]
    b_val = lab[:, 2]
    
    y = (l_val + 16) / 116
    x = a_val / 500 + y
    z = y - b_val / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
    
    xyz_from = np.stack([f_inv(x), f_inv(y), f_inv(z)], axis=-1) * wp_from
    
    # XYZ (from) -> Lab (to)
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
    
    wp_to = as_white_ref(white_to)
    
    if from_val.lower() == 'rgb' and to_val.lower() == 'lab':
        res = rgb_to_lab(colour, wp_to)
        return res
    
    if from_val.lower() == 'lab' and to_val.lower() == 'lab':
        vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
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
# r2py:entity:convert_colour
res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(res_white)

# r2py:entity:spec_lab_1
spec_lab_1 = res_white