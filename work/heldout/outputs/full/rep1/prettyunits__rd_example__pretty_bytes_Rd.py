# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd

# r2py:entity:pretty_bytes
def pretty_bytes(bytes_val, style="default"):
    vals = np.atleast_1d(bytes_val)
    # prettyunits::pretty_bytes uses 1000 as base for kB, MB, etc.
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    
    results = []
    for v in vals:
        if v == 0:
            results.append("0 B")
            continue
            
        # Calculate magnitude based on 1000
        i = int(np.floor(np.log10(v) / 3)) if v > 0 else 0
        i = max(0, min(i, len(units) - 1))
        
        p = v / (1000**i)
        
        if style == "nopad":
            # R's nopad for bytes seems to use 2 decimal places
            results.append(f"{p:.2f} {units[i]}")
        elif style == "6":
            # style "6" seems to round to 1 decimal or similar, but matches integers
            # Looking at R output: 1.3 kB, 133 kB, 13 MB...
            # It's essentially rounding to 1 decimal place and stripping trailing zeros
            val_str = f"{p:.1f}".rstrip('0').rstrip('.')
            results.append(f"{val_str} {units[i]}")
        else: # default
            # Default pads the number to a width of 6
            # R output: "  1.34 kB" "133.34 kB"
            val_str = f"{p:.2f}"
            results.append(f"{val_str:>6} {units[i]}")
            
    return results[0] if np.isscalar(bytes_val) else results

# r2py:entity:bytes
bytes = np.array([1337, 133337, 13333337, 1333333337, 133333333337])

# r2py:entity:pretty_bytes
print(pretty_bytes(bytes))
# r2py:entity:pretty_bytes_1
print(pretty_bytes(bytes, style="nopad"))
# r2py:entity:pretty_bytes_2
print(pretty_bytes(bytes, style="6"))