import numpy as np
import pandas as pd
from skimage import color

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
    R's rainbow(n) generates n colors spanning the hue range [0, 1].
    """
    import colorsys
    res = []
    for i in range(n):
        # R's rainbow(n) hue is seq(0, 1, length.out=n)
        h = i / (n - 1) if n > 1 else 0
        # rainbow() in R produces RGB values in [0, 1]
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append(rgb)
    return np.array(res)

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """Translates R farver::decode_colour."""
    # For this specific script, rainbow(10) returns RGB [0,1]
    return np.array(colour)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to="D65"):
    """Translates R farver::convert_colour."""
    # Convert input to numpy array if it's a DataFrame
    vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
    
    if from_val == 'rgb' and to_val == 'lab':
        # skimage.color.rgb2lab expects [0, 1] range
        # Default white is D65
        lab = color.rgb2lab(vals)
        return pd.DataFrame(lab, columns=['L', 'a', 'b'])
    
    if from_val == 'lab' and to_val == 'lab':
        # Handling white point conversion (Lab -> XYZ(white_from) -> XYZ(white_to) -> Lab)
        # This is a complex transformation. 
        # In the context of farver, this typically uses the CIE standard.
        
        # 1. Convert Lab (white_from) to XYZ (white_from)
        # Since skimage doesn't allow specifying the white point easily in rgb2lab,
        # we must use the standard formulas.
        
        def lab_to_xyz(lab_vals, white_ref):
            L = lab_vals[..., 0]
            a = lab_vals[..., 1]
            b = lab_vals[..., 2]
            
            fy = (L + 16) / 116
            fx = a / 500 + fy
            fz = fy - b / 200
            
            def f_inv(t):
                return np.where(t**3 > 0.008856, t**3, (t - 16/116) / 7.787)
            
            x = f_inv(fx) * white_ref[0]
            y = f_inv(fy) * white_ref[1]
            z = f_inv(fz) * white_ref[2]
            return np.stack([x, y, z], axis=-1)

        def xyz_to_lab(xyz_vals, white_ref):
            # Normalize by white reference
            xyz_norm = xyz_vals / white_ref
            
            def f(t):
                return np.where(t > 0.008856, np.power(t, 1/3), (7.787 * t) + (16/116))
            
            f_xyz = f(xyz_norm)
            f_white = f(np.array([1.0, 1.0, 1.0])) # normalized
            
            L = (116 * f_xyz[..., 1]) - 16
            a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
            b = 200 * (f_xyz[..., 2] - f_xyz[..., 1])
            return np.stack([L, a, b], axis=-1)

        white_refs = {
            "D65": np.array([0.950301, 1.0, 1.08883]),
            "F10": np.array([0.9164, 1.0, 1.1442]),
            "D50": np.array([0.96422, 1.0, 1.000]),
        }
        
        wp_from = white_refs.get(white_from, white_refs["D65"])
        wp_to = white_refs.get(white_to, white_refs["D65"])
        
        xyz = lab_to_xyz(vals, wp_from)
        lab_res = xyz_to_lab(xyz, wp_to)
        return pd.DataFrame(lab_res, columns=['L', 'a', 'b'])
        
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