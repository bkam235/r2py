# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:pretty_bytes
def pretty_bytes_format(b, pad=True, style="default"):
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    if b == 0:
        return "0 B"
    
    # prettyunits::pretty_bytes uses 1000 as divisor (SI units)
    i = int(np.floor(np.log10(b) / 3)) if b > 0 else 0
    if i >= len(units):
        i = len(units) - 1
    if i < 0:
        i = 0
        
    p = b / (1000**i)
    
    if style == "6":
        # Style "6" in R prettyunits seems to produce 1 significant figure/minimal decimals
        # Based on R output: 1.3 kB, 133 kB, 13 MB...
        # This looks like rounding to a specific precision or removing trailing zeros.
        val = f"{p:.1g}"
        # The R output for "6" shows " 13 MB", implying some padding
        return f"{val:>5} {units[i]}"
    
    # Default and nopad use 2 decimal places
    fmt_val = f"{p:.2f}"
    if pad:
        # R default style pads to 6 characters for the number part
        return f"{fmt_val:>6} {units[i]}"
    else:
        return f"{fmt_val} {units[i]}"

def pretty_bytes_default(bytes_val):
    return [pretty_bytes_format(b, pad=True, style="default") for b in bytes_val]

def pretty_bytes_nopad(bytes_val):
    return [pretty_bytes_format(b, pad=False, style="default") for b in bytes_val]

def pretty_bytes_6(bytes_val):
    return [pretty_bytes_format(b, pad=True, style="6") for b in bytes_val]

def pretty_bytes(bytes_val, style="default"):
    styles = {
        "default": pretty_bytes_default,
        "nopad": pretty_bytes_nopad,
        "6": pretty_bytes_6
    }
    func = styles.get(style, pretty_bytes_default)
    return func(bytes_val)

# r2py:entity:bytes
bytes = np.array([1337, 133337, 13333337, 1333333337, 133333333337])
# r2py:entity:pretty_bytes
print(pretty_bytes(bytes))
# r2py:entity:pretty_bytes_1
print(pretty_bytes(bytes, style="nopad"))
# r2py:entity:pretty_bytes_2
print(pretty_bytes(bytes, style="6"))