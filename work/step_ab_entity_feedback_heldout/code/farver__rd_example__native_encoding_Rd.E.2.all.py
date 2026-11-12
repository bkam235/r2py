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
    For common R colors, the representation is often a signed 32-bit integer.
    """
    if not isinstance(colour, (list, np.ndarray, tuple)):
        colour = [colour]
    
    # Map R-specific color names to hex/matplotlib colors
    # 'navyblue' in R is #000080
    mapping = {
        'navyblue': '#000080'
    }
    
    native_vals = []
    for col in colour:
        hex_col = mapping.get(col.lower(), col) if isinstance(col, str) else col
        rgba = mcolors.to_rgba(hex_col)
        
        r = int(round(rgba[0] * 255))
        g = int(round(rgba[1] * 255))
        b = int(round(rgba[2] * 255))
        
        # R's native encoding logic for these colors: 
        # The value -8388608 is 0xFF000080 in 2's complement
        # 0xFF000080 corresponds to (255 << 24) | (0 << 16) | (0 << 8) | 128
        val = (255 << 24) | (r << 16) | (g << 8) | b
        
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

# Print for stdout verification
print(f"[1] {native_col[0]} {native_col[1]}")

# Convert back
# r2py:entity:decode_native
decode_native = decode_native(native_col)
print(f'[1] "{decode_native[0]}" "{decode_native[1]}"')