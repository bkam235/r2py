# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd

# r2py:entity:pretty_bytes
def pretty_bytes(bytes_val, style="pad"):
    # Approximation of prettyunits::pretty_bytes
    # Units for bytes
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    
    if isinstance(bytes_val, (list, np.ndarray, pd.Series)):
        results = []
        for b in bytes_val:
            results.append(pretty_bytes(b, style=style))
        return results
    
    if bytes_val == 0:
        return "0 B"
    
    # Calculate magnitude
    i = int(np.floor(np.log10(bytes_val) / 3)) if bytes_val > 0 else 0
    # In R's prettyunits, bytes are typically handled in powers of 1000 or 1024.
    # Standard pretty_bytes typically uses 1000 for SI.
    mag = 1000 ** i
    val = bytes_val / mag
    unit = units[i] if i < len(units) else units[-1]
    
    if style == "nopad":
        return f"{val:.2g} {unit}"
    elif style.isdigit():
        precision = int(style)
        return f"{val:.{precision}f} {unit}"
    else: # Default "pad" behavior
        return f"{val:g} {unit}"

# r2py:entity:bytes
bytes = np.array([1337, 133337, 13333337, 1333333337, 133333333337])

# r2py:entity:pretty_bytes
print(pretty_bytes(bytes))
# r2py:entity:pretty_bytes_1
print(pretty_bytes(bytes, style="nopad"))
# r2py:entity:pretty_bytes_2
print(pretty_bytes(bytes, style="6"))