import re
import numpy as np

def _r2py_impl_r_substr_ctl(x, start, stop, warn=True, term_cap=None, ctl="all", 
                 normalize=False, carry=False, terminate=True):
    """
    Python reproduction of fansi::substr_ctl.
    """
    # Handle vector input: R returns a vector if x is a vector
    is_vector = isinstance(x, (list, np.ndarray))
    inputs = x if is_vector else [x]
    
    # ANSI escape sequence regex - captures SGR and others
    # SGR sequences usually end with 'm'
    ansi_pattern = re.compile(r'(\x1b\[[0-9;]*[mK])')
    
    results = []
    for item in inputs:
        if item is None:
            results.append(None)
            continue
            
        text = str(item)
        parts = ansi_pattern.split(text)
        
        current_logical_pos = 1
        res_parts = []
        # track if the current sliced-out text is "inside" a style
        active_style = False
        
        # We need to identify if the string contains a style that is not closed
        # before the 'stop' position.
        
        for part in parts:
            if not part:
                continue
            
            if ansi_pattern.match(part):
                # Control sequence
                if current_logical_pos <= stop:
                    # Keep if it's before start and carry/ctl is enabled, or if it's within the window
                    if current_logical_pos >= start:
                        res_parts.append(part)
                        # Update style state
                        if part.endswith('m'):
                            # Reset sequence: [0m or just [m
                            if '0' in part[part.find('[')+1:] or part == "\x1b[m":
                                active_style = False
                            else:
                                active_style = True
                    else:
                        # Before start: carry or ctl "all"/"sgr" logic
                        ctl_list = [ctl] if isinstance(ctl, str) else ctl
                        if carry or "all" in ctl_list or "sgr" in ctl_list:
                            res_parts.append(part)
                            if part.endswith('m'):
                                if '0' in part[part.find('[')+1:] or part == "\x1b[m":
                                    active_style = False
                                else:
                                    active_style = True
                else:
                    # We are past the stop position. 
                    # However, R's substr_ctl might need to see if a reset was skipped.
                    pass
            else:
                # Plain text block
                block_len = len(part)
                block_start = current_logical_pos
                block_end = current_logical_pos + block_len - 1
                
                overlap_start = max(start, block_start)
                overlap_stop = min(stop, block_end)
                
                if overlap_start <= overlap_stop:
                    rel_start = overlap_start - block_start
                    rel_stop = overlap_stop - block_start + 1
                    res_parts.append(part[rel_start:rel_stop])
                
                current_logical_pos += block_len
        
        res_str = "".join(res_parts)
        
        # The critical part for the failing cases:
        # If 'terminate' is True and we ended the slice while a style was active,
        # R adds a reset sequence "\x1b[0m" to prevent style leakage.
        if terminate and active_style:
            # Only append if the result doesn't already end with a reset
            if not res_str.endswith("\x1b[0m") and not res_str.endswith("\x1b[m"):
                res_str += "\x1b[0m"

        results.append(res_str)

    if is_vector:
        return results
    else:
        return results[0]


_R2PY_UNVERIFIED_r_substr_ctl = {'carry': ['True'], 'normalize': ['True']}
_R2PY_UNVERIFIED_CLASSES_r_substr_ctl = ['NA input', 'vector input']


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
