import numpy as np

# r2py:entity:pretty_num
def get_si_prefix(val):
    """Helper to determine SI prefix and scaled value."""
    if val == 0:
        return 0, ""
    
    # SI Prefixes
    prefixes = [
        (1e12, 'T'), (1e9, 'G'), (1e6, 'M'), (1e3, 'k'),
        (1, ''), 
        (1e-3, 'm'), (1e-6, 'u'), (1e-9, 'n'), (1e-12, 'p')
    ]
    
    abs_val = abs(val)
    for limit, prefix in prefixes:
        if abs_val >= limit:
            return val / limit, prefix
    # For extremely small numbers
    return val / 1e-12, 'p'

def format_pretty(val, style):
    scaled, prefix = get_si_prefix(val)
    
    if style == "6":
        # 6 significant digits, but the output shows different behaviors 
        # based on the magnitude (e.g., "133 G" vs "1.33 G")
        # R's pretty_num(style="6") essentially uses 6 sig figs total.
        fmt = "{:.6g}"
        s = fmt.format(scaled)
    elif style == "nopad":
        # Default precision (usually 3 or 4), no leading spaces
        fmt = "{:.2f}" if prefix else "{:.0f}"
        # If it's an integer-like float, remove trailing zeros
        s = f"{scaled:g}"
        if '.' in s:
            # R's default for these examples seems to be 2 decimal places
            s = f"{scaled:.2f}".rstrip('0').rstrip('.') if scaled % 1 != 0 else f"{scaled:.0f}"
            # Correction based on R output: "1.34 k", "13.33 u"
            s = f"{scaled:.2f}"
    else: # "default"
        # Padded to a certain width, 2 decimal places
        s = f"{scaled:.2f}"
    
    # Handle the specific R output cases seen in verification
    # "1.34 k", "13.33 u", "13.33 M", "1.33 G", "133.33 G"
    # It looks like it's actually using 3 significant figures for the numeric part.
    
    # Re-evaluating based on R output: 
    # 1337 -> "1.34 k" (3 sig figs)
    # 1.3333e-5 -> "13.33 u" (4 sig figs? No, 1.3333e-5 is 13.3333u)
    # 13333337 -> "13.33 M"
    # 1333333337 -> "1.33 G"
    # 133333333337 -> "133.33 G"
    
    # Let's try a more robust 3-4 sig fig approach
    if style == "6":
        s = f"{scaled:.3g}"
    else:
        s = f"{scaled:.2f}"
    
    # Clean up trailing zeros for "nopad" vs "default"
    if style == "nopad":
        # Remove trailing zeros if they are redundant, but R output shows "1.34 k"
        # Actually, "nopad" just removes the leading spaces.
        res = f"{s} {prefix}".strip()
    elif style == "6":
        res = f"{s} {prefix}".strip()
    else:
        # Default: Right aligned, width approx 7
        res = f"{s} {prefix}".strip()
        res = res.rjust(7)
    
    return res

def pretty_num_default(number):
    return [format_pretty(x, "default") for x in np.atleast_1d(number)]

def pretty_num_nopad(number):
    return [format_pretty(x, "nopad") for x in np.atleast_1d(number)]

def pretty_num_6(number):
    return [format_pretty(x, "6") for x in np.atleast_1d(number)]

def pretty_num(number, style="default"):
    if style == "default":
        func = pretty_num_default
    elif style == "nopad":
        func = pretty_num_nopad
    elif style == "6":
        func = pretty_num_6
    else:
        raise ValueError("style must be one of 'default', 'nopad', '6'")
    
    res = func(number)
    return res if np.atleast_1d(number).size > 1 else res[0]

# r2py:entity:numbers
numbers = np.array([1337, 1.3333e-5, 13333337, 1333333337, 133333333337])

# r2py:entity:pretty_num
print(pretty_num(numbers))
# r2py:entity:pretty_num_1
print(pretty_num(numbers, style="nopad"))
# r2py:entity:pretty_num_2
print(pretty_num(numbers, style="6"))