import numpy as np
import re

def _r2py_impl_r_substr_ctl(x, start, stop, warn=True, term_cap="truecolor", ctl="all", 
                 normalize=False, carry=False, terminate=True):
    """
    Substring extraction that respects ANSI control sequences.
    
    This function extracts substrings while preserving ANSI escape sequences
    that affect the appearance of the visible characters.
    """
    
    if isinstance(x, list):
        # Handle character vector
        return [_r2py_impl_r_substr_ctl(xi, start, stop, warn, term_cap, ctl, normalize, carry, terminate) 
                for xi in x]
    
    # Convert start and stop to 0-based Python indexing
    # R uses 1-based indexing
    start_idx = int(start) - 1
    stop_idx = int(stop)
    
    # Pattern to match ANSI escape sequences
    ansi_pattern = r'\x1b\[[0-9;]*[a-zA-Z]'
    
    # Find all ANSI sequences and their positions in the original string
    ansi_matches = list(re.finditer(ansi_pattern, x))
    
    # Build a map of visible character positions to string positions
    visible_pos = 0
    pos_map = []  # (visible_pos, string_pos, char_type) where char_type: 'char' or 'ansi'
    string_pos = 0
    
    while string_pos < len(x):
        # Check if there's an ANSI sequence at current position
        found_ansi = False
        for match in ansi_matches:
            if match.start() == string_pos:
                # Add ANSI sequence to map
                pos_map.append((visible_pos, string_pos, 'ansi', match.end() - string_pos))
                string_pos = match.end()
                found_ansi = True
                break
        
        if not found_ansi:
            # Regular character
            pos_map.append((visible_pos, string_pos, 'char', 1))
            visible_pos += 1
            string_pos += 1
    
    # Extract the substring based on visible character positions
    result = []
    ansi_codes = []
    
    for vis_pos, str_pos, char_type, length in pos_map:
        if char_type == 'ansi':
            ansi_codes.append(x[str_pos:str_pos + length])
            result.append(x[str_pos:str_pos + length])
        elif start_idx <= vis_pos < stop_idx:
            result.append(x[str_pos:str_pos + length])
    
    # Reconstruct the result with proper ANSI sequences
    output = ''.join(result)
    
    # If terminate is True and there are SGR codes, add reset at the end
    if terminate and any('\x1b[' in code for code in ansi_codes):
        # Check if there's already a reset code
        if '\x1b[0m' not in output and '\x1b[m' not in output:
            output += '\x1b[0m'
    
    return output


_R2PY_UNVERIFIED_r_substr_ctl = {'carry': ['True'], 'ctl': ['sgr'], 'normalize': ['True'], 'terminate': ['False'], 'warn': ['False']}
_R2PY_UNVERIFIED_CLASSES_r_substr_ctl = ['vector input']


def _r2py_items_r_substr_ctl(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_substr_ctl(*args, **kwargs):
    """r_substr_ctl reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_substr_ctl
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_substr_ctl; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_substr_ctl).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_substr_ctl.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_substr_ctl: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_substr_ctl and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_substr_ctl(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_substr_ctl and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_substr_ctl: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_substr_ctl and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_substr_ctl: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_substr_ctl(*args, **kwargs)
