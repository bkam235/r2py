# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd

# Since there is no direct 1:1 equivalent to prettyunits.pretty_bytes, 
# we implement a helper to mimic the R behavior.
# r2py:entity:pretty_bytes
def pretty_bytes(bytes_val, style="pad"):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    if isinstance(bytes_val, (list, np.ndarray)):
        results = []
        for b in bytes_val:
            # Handle scalar conversion logic
            i = int(np.floor(np.log10(b) / 3)) if b > 0 else 0
            i = min(i, len(units) - 1)
            val = b / (10** (3 * i))
            
            if style == "nopad":
                fmt = f"{val:g}{units[i]}"
            elif isinstance(style, str) and style.isdigit():
                precision = int(style)
                fmt = f"{val:.{precision}f}{units[i]}"
            else: # Default "pad" (roughly matches R's default pretty_bytes)
                fmt = f"{val:.2f}{units[i]}"
            results.append(fmt)
        return results
    return ""

# r2py:entity:bytes
bytes = np.array([1337, 133337, 13333337, 1333333337, 133333333337])

# r2py:entity:pretty_bytes
print(pretty_bytes(bytes))
# r2py:entity:pretty_bytes_1
print(pretty_bytes(bytes, style="nopad"))
# r2py:entity:pretty_bytes_2
print(pretty_bytes(bytes, style="6"))