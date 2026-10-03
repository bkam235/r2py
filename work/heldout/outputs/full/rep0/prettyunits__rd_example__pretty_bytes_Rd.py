# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd

# Implementation of pretty_bytes since there is no direct equivalent to the 'prettyunits' package in Python
# r2py:entity:pretty_bytes
def pretty_bytes(bytes_val, style="pad"):
    if isinstance(bytes_val, (list, np.ndarray)):
        return [pretty_bytes(x, style=style) for x in bytes_val]
    
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    if bytes_val == 0:
        return "0 B"
    
    # Calculate index based on log1000 (decimal bytes as per prettyunits default)
    i = int(np.floor(np.log10(abs(bytes_val)) / 3)) if bytes_val != 0 else 0
    i = min(i, len(units) - 1)
    
    value = bytes_val / (1000**i)
    
    if style == "nopad":
        fmt = "{:g} {}"
    elif isinstance(style, str) and style.isdigit():
        precision = int(style)
        fmt = "{:." + str(precision) + "f} {}"
    else: # default "pad"
        fmt = "{:.2f} {}"
        
    return fmt.format(value, units[i])

# r2py:entity:bytes
bytes = np.array([1337, 133337, 13333337, 1333333337, 133333333337])

# r2py:entity:pretty_bytes
print(pretty_bytes(bytes))
# r2py:entity:pretty_bytes_1
print(pretty_bytes(bytes, style="nopad"))
# r2py:entity:pretty_bytes_2
print(pretty_bytes(bytes, style="6"))