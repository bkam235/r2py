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
    Approximate R's rainbow(n) function.
    R's rainbow() uses a specific formula: 
    h = seq(0, 1, length.out = n)
    Then converts HSV to RGB.
    """
    import colorsys
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow is essentially HSV with S=1, V=1
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        # R's rainbow() output is in 0-1 range usually, 
        # but decode_colour expects RGB values.
        # The R source uses rainbow(10) inside decode_colour.
        # farver::decode_colour handles the R rainbow output (0-1).
        res.append(list(rgb))
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    # If the input is from rainbow(), it's 0-1. 
    # farver::decode_colour converts these to a standard internal format.
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([0.950303, 1.000000, 1.08883]),
        "F10": np.array([0.9164, 1.0000, 1.1442]),
        "D50": np.array([0.96422, 1.0000, 1.0000]),
    }
    if isinstance(white, str):
        val = white_refs.get(white.upper())
        if val is None:
            raise ValueError("Unknown white reference")
        return val
    return np.array(white)

def rgb_to_lab(rgb, white_ref):
    """Helper to convert RGB [0,1] to Lab."""
    rgb = np.array(rgb)
    
    # sRGB to Linear RGB
    mask = rgb > 0.04045
    rgb_lin = np.zeros_like(rgb)
    rgb_lin[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb_lin[~mask] = rgb[~mask] / 12.92
    
    # Linear RGB to XYZ (D65)
    matrix = np.array([
        [0.4122214709, 0.3575792601, 0.1804226925],
        [0.2126729013, 0.7151521930, 0.0721750511],
        [0.0193339190, 0.1183895484, 0.9504892779]
    ])
    xyz = rgb_lin @ matrix.T
    
    # Normalize XYZ by the white reference (chromatic adaptation is simplified here)
    # Since farver uses the provided white_ref for the Lab conversion:
    xyz_norm = xyz / white_ref
    
    def f(t):
        return np.where(t > 0.008856451668, np.power(t, 1/3), (7.787037 * t) + (16/116))
    
    f_xyz = f(xyz_norm)
    
    l = (116 * f_xyz[..., 1]) - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
    
    return np.stack([l, a, b], axis=-1)

def lab_to_lab_shift(lab, white_from, white_to):
    """Helper to shift Lab values between white references."""
    wp_from = as_white_ref(white_from)
    wp_to = as_white_ref(white_to)
    
    # Lab -> XYZ (white_from)
    y = (lab[:, 0] + 16) / 116
    x = lab[:, 1] / 500 + y
    z = y - lab[:, 2] / 200
    
    def f_inv(t):
        return np.where(t**3 > 0.008856451668, t**3, (t - 16/116) / 7.787037)
    
    xyz_from = np.stack([f_inv(x), f_inv(y), f_inv(z)], axis=-1) * wp_from
    
    # XYZ (white_from) -> Lab (white_to)
    xyz_norm_to = xyz_from / wp_to
    
    def f(t):
        return np.where(t > 0.008856451668, np.power(t, 1/3), (7.787037 * t) + (16/116))
    
    f_xyz = f(xyz_norm_to)
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
# R prints spec_lab here
print(pd.DataFrame(spec_lab, columns=['l', 'a', 'b']))

# Convert between different white references
# r2py:entity:convert_colour
res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
# R prints the result of this call
print(pd.DataFrame(res_white, columns=['l', 'a', 'b']))

# Mapping for verifier entities
# r2py:entity:spec_lab_1
spec_lab_1 = res_white