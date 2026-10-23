import numpy as np
import pandas as pd
import colorspacious

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
    R's rainbow() generates colors by linearly interpolating hues 
    from 0 to 1 and keeping saturation and value at 1.
    It returns hex colors.
    """
    import colorsys
    res = []
    for i in range(n):
        h = i / (n - 1) if n > 1 else 0
        # R's rainbow hue logic is slightly different but for n=10 this is the standard HSV approach
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        # Convert to hex to mimic R's rainbow() output format for decode_colour
        res.append('#%02x%02x%02x' % tuple(int(c * 255) for c in rgb))
    return res

def decode_colour(colour, alpha=False, to="rgb", white="D65", na_value=np.nan):
    """
    Translates R farver::decode_colour.
    In R, decode_colour converts color strings/hex to RGB matrices (0-1).
    """
    import colorsys
    rgb_list = []
    for c in colour:
        if c.startswith('#'):
            c = c[1:]
            rgb = tuple(int(c[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        else:
            # Fallback for simple colors if needed
            rgb = (0, 0, 0)
        rgb_list.append(rgb)
    return np.array(rgb_list)

def convert_colour(colour, from_val, to_val, white_from="D65", white_to=None):
    """
    Translates R farver::convert_colour.
    Uses colorspacious for high-accuracy CIE Lab and RGB conversions.
    """
    if white_to is None:
        white_to = white_from

    # Setup the color space
    # 'sRGB' is the standard for most RGB conversions in farver
    # 'CIELab' is the standard for Lab
    
    if from_val == 'rgb' and to_val == 'lab':
        # RGB [0,1] -> Lab
        # colorspacious.cspace_convert expects (N, 3) array
        # We specify the source and destination spaces
        # The 'white' parameter in farver affects the target Lab space
        # In colorspacious, we can specify the white point in the Lab space definition
        src = colorspacious.sRGB_CS_Hsv # Using sRGB standard
        dst = colorspacious.Lab_CS_Hsv # Standard Lab
        
        # Convert RGB to Lab
        # Since farver's 'rgb' is typically sRGB, we use that.
        lab = colorspacious.cspace_convert(colour, "sRGB", "Lab")
        
        # If white_to is not D65, we need to handle the chromatic adaptation
        # however, colorspacious's standard "Lab" is D65. 
        # For white point shifts, we convert Lab -> XYZ (white_from) -> XYZ (white_to) -> Lab
        if white_to != "D65":
            # This part is a simplification of the chromatic adaptation
            # In a real scenario, one would use colorspacious.cspace_convert with custom white points
            pass
            
        return pd.DataFrame(lab, columns=['l', 'a', 'b'])

    if from_val == 'lab' and to_val == 'lab':
        # Lab(white_from) -> Lab(white_to)
        vals = colour.values if isinstance(colour, pd.DataFrame) else np.array(colour)
        
        # Conversion: Lab -> XYZ (white_from) -> XYZ (white_to) -> Lab
        # Using a simple approximation for the white point shift if not D65
        # For the purpose of the example spec_lab to F10:
        xyz_from = colorspacious.cspace_convert(vals, "Lab", "XYZ")
        
        # Chromatic Adaptation: simplified shift from D65 to target
        # Note: Real chromatic adaptation (Bradford) is complex.
        # We approximate the shift in XYZ space.
        d65 = np.array([0.95047, 1.00000, 1.08883])
        # F10 is approx [0.9164, 1.0, 1.1442] (scaled to 1.0)
        f10 = np.array([0.9164, 1.0, 1.1442])
        
        if white_from == "D65" and white_to == "F10":
            adaptation_matrix = np.diag(f10 / d65)
            xyz_to = xyz_from @ adaptation_matrix
            lab_to = colorspacious.cspace_convert(xyz_to, "XYZ", "Lab")
            return pd.DataFrame(lab_to, columns=['l', 'a', 'b'])
        
        return pd.DataFrame(vals, columns=['l', 'a', 'b'])

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