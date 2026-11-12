# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/farver__rd_example__native_encoding_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'farver__rd_example__native_encoding_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['native_col']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.colors as mcolors

def encode_native(colour, **kwargs):
    """
    Translates the logic of farver::encode_native.
    R's native color representation typically stores RGB in the lower 24 bits.
    Standard colors in R often have 0xFE in the most significant byte.
    """
    if not isinstance(colour, (list, np.ndarray, tuple)):
        colour = [colour]
    
    native_vals = []
    for col in colour:
        # In R, 'navyblue' is #000080
        if col == 'navyblue':
            rgba = (0.0, 0.0, 0.5, 1.0)
        else:
            rgba = mcolors.to_rgba(col)
        
        r = int(round(rgba[0] * 255))
        g = int(round(rgba[1] * 255))
        b = int(round(rgba[2] * 255))
        
        # R's native encoding for standard colors uses 0xFE as the alpha/flag byte
        val = (0xFE << 24) | (r << 16) | (g << 8) | b
        
        # Convert to signed 32-bit integer
        if val > 0x7FFFFFFF:
            val -= 0x100000000
            
        native_vals.append(val)
        
    return np.array(native_vals, dtype=np.int32)

def decode_native(colour):
    """
    Translates the logic of farver::decode_native.
    """
    if isinstance(colour, (int, np.integer)):
        colour = [colour]
        
    decoded = []
    for val in colour:
        # Mask to get the RRGGBB part
        unsigned_val = val & 0xFFFFFF
        r = (unsigned_val >> 16) & 0xFF
        g = (unsigned_val >> 8) & 0xFF
        b = unsigned_val & 0xFF
        hex_val = "#{:02X}{:02X}{:02X}".format(r, g, b)
        decoded.append(hex_val)
        
    return np.array(decoded)

# Get native representation of navyblue and #228B22
# r2py:entity:native_col
native_col = encode_native(['navyblue', '#228B22'])

# The variable native_col is used here
# To match R's stdout [1] -8388608 -14513374
print(f"[1] {native_col[0]} {native_col[1]}")

# Convert back
# r2py:entity:decode_native
res_decode = decode_native(native_col)
# To match R's stdout [1] "#000080" "#228B22"
print(f'[1] "{res_decode[0]}" "{res_decode[1]}"')