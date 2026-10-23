import numpy as np

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
    Approximate R's rainbow(n) colors.
    R's rainbow(n) uses a specific HSV-to-RGB mapping where Hue goes from 0 to 1.
    """
    import colorsys
    res = []
    for i in range(n):
        # R's rainbow(10) hue sequence: 0, 0.111, 0.222...
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow() typically results in full saturation and value
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append([round(c * 255) for c in rgb])
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    return np.array(colour)

def as_white_ref(white):
    """Translates R farver::as_white_ref."""
    white_refs = {
        "D65": np.array([0.95045895, 1.00000000, 1.08884048]),
        "F10": np.array([0.916402, 1.00000000, 1.144212]),
        "D50": np.array([0.96422, 1.00000000, 0.82491)],
    }
    if isinstance(white, str):
        return white_refs.get(white.upper(), white_refs["D65"])
    return np.array(white)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """Translates R farver::convert_colour."""
    if white_to is None:
        white_to = white_from
    
    # Ensure input is numpy array
    col_arr = np.array(colour)
    
    if from_val == 'rgb' and to_val == 'lab':
        # Normalize RGB 0-255 to 0-1
        rgb = col_arr / 255.0
        
        # sRGB to Linear RGB
        mask = rgb > 0.04045
        rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
        rgb[~mask] = rgb[~mask] / 12.92
        
        # Linear RGB to XYZ (D65)
        # Standard sRGB matrix
        matrix = np.array([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1183895, 0.9503041]
        ])
        xyz = rgb @ matrix.T
        
        # Reference white for the target space
        wp_to = as_white_ref(white_to)
        
        # XYZ to LAB
        # Normalize XYZ by the white point
        xyz_norm = xyz / wp_to
        
        def f(t):
            return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
        
        f_xyz = f(xyz_norm)
        # f(1.0) for the white point normalized to 1.0 is approx 1.000
        # but more precisely it's f(1.0)
        f_w = f(np.array([1.0, 1.0, 1.0]))
        
        l = (116 * f_xyz[..., 1]) - 16
        a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
        b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
        
        return np.stack([l, a, b], axis=-1)
    
    elif from_val == 'lab' and to_val == 'lab':
        # Lab (white_from) -> XYZ (white_from) -> Lab (white_to)
        wp_from = as_white_ref(white_from)
        wp_to = as_white_ref(white_to)
        
        l = col_arr[..., 0]
        a = col_arr[..., 1]
        b = col_arr[..., 2]
        
        fy = (l + 16) / 116
        fx = a / 500 + fy
        fz = fy - b / 200
        
        def f_inv(t):
            return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
        
        xyz_from = np.stack([f_inv(fx), f_inv(fy), f_inv(fz)], axis=-1) * wp_from
        
        # Now convert XYZ (from wp_from) to Lab (with wp_to)
        xyz_norm_to = xyz_from / wp_to
        
        def f(t):
            return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
            
        f_xyz_to = f(xyz_norm_to)
        
        l_new = (116 * f_xyz_to[..., 1]) - 16
        a_new = 500 * (f_xyz_to[..., 0] - f_xyz_to[..., 1])
        b_new = 200 * (f_xyz_to[..., 2] - f_xyz_to[..., 1])
        
        return np.stack([l_new, a_new, b_new], axis=-1)

    return col_arr

# Execute the translated script
spectrum = decode_colour(rainbow(10))
spec_lab = convert_colour(spectrum, 'rgb', 'lab')
# R doesn't print spec_lab here (it's just an assignment)

# Convert between different white references
# This is an expression, so it should be printed
res_white = convert_colour(spec_lab, 'lab', 'lab', white_from='D65', white_to='F10')
print(res_white)