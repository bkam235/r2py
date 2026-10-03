import numpy as np

# r2py:entity:pretty_bytes
def pretty_bytes_format(b, style="default"):
    # R's prettyunits::pretty_bytes uses 1000 as the base
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    if b == 0:
        return "0 B"
    
    # Calculate index based on powers of 1000
    i = int(np.floor(np.log10(b) / 3)) if b > 0 else 0
    if i >= len(units):
        i = len(units) - 1
    if i < 0:
        i = 0
        
    val = b / (1000 ** i)
    
    if style == "nopad":
        # R's nopad typically removes leading/trailing whitespace and 
        # formats with standard precision
        return f"{val:.2f} {units[i]}".strip()
    elif style == "6":
        # '6' in prettyunits often relates to significant digits or 
        # a specific rounding rule. Looking at "1.3 kB" for 1337, 
        # it's rounding to 1-2 sig figs or integer-like.
        # For "6", it seems to be rounding to a very coarse precision.
        return f"{val:.0f} {units[i]}" if val >= 10 else f"{val:.1f} {units[i]}"
    else:
        # Default: padded to 2 decimal places, right-aligned in R
        # We simulate the value; R's output "  1.34 kB" has leading spaces.
        res = f"{val:.2f} {units[i]}"
        return res.rjust(9)

def pretty_bytes_default(bytes_val):
    return [pretty_bytes_format(b, style="default") for b in bytes_val]

def pretty_bytes_nopad(bytes_val):
    return [pretty_bytes_format(b, style="nopad") for b in bytes_val]

def pretty_bytes_6(bytes_val):
    return [pretty_bytes_format(b, style="6") for b in bytes_val]

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