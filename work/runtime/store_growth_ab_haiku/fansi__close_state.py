import re
import numpy as np

def _r2py_impl_r_close_state(x, warn=None, normalize=None):
    # Handle default options
    if warn is None:
        warn = True
    if normalize is None:
        normalize = False
    
    # Convert input to list if needed
    if isinstance(x, str):
        x = [x]
    elif isinstance(x, np.ndarray):
        x = x.tolist()
    elif hasattr(x, '__iter__') and not isinstance(x, str):
        x = list(x)
    else:
        x = [x]
    
    result = []
    
    for state_str in x:
        # Handle NA/NaN values
        if isinstance(state_str, float) and np.isnan(state_str):
            result.append("")
            continue
        
        # Handle None
        if state_str is None:
            result.append("")
            continue
        
        # Convert to string if needed
        state_str = str(state_str)
        
        # If state_str is empty, return empty
        if not state_str:
            result.append("")
            continue
        
        if not normalize:
            # Check if there's any actual state (not just reset codes)
            # Remove all \033[0m codes and see if anything remains
            temp = state_str.replace("\033[0m", "")
            if not temp or not re.search(r'\033\[[0-9;]+m', temp):
                result.append("")
            else:
                result.append("\033[0m")
        else:
            # Parse the state string to find active attributes
            closing_codes = []
            
            # Find all ANSI SGR codes in the state string
            pattern = r'\033\[([0-9;]+)m'
            matches = re.findall(pattern, state_str)
            
            # Track which attributes are active
            has_foreground = False
            has_background = False
            
            for match in matches:
                codes = match.split(';')
                for code in codes:
                    code_int = int(code)
                    # 0 means reset - if we see it, it clears all attributes
                    if code_int == 0:
                        has_foreground = False
                        has_background = False
                    # 30-37, 90-97: foreground colors
                    elif (30 <= code_int <= 37) or (90 <= code_int <= 97):
                        has_foreground = True
                    # 40-47, 100-107: background colors
                    elif (40 <= code_int <= 47) or (100 <= code_int <= 107):
                        has_background = True
            
            # Generate closing codes in order
            if has_foreground:
                closing_codes.append("\033[39m")
            if has_background:
                closing_codes.append("\033[49m")
            
            result.append("".join(closing_codes))
    
    return result


_R2PY_UNVERIFIED_r_close_state = {'normalize': ['True']}
_R2PY_UNVERIFIED_CLASSES_r_close_state = []


def _r2py_items_r_close_state(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_close_state(*args, **kwargs):
    """r_close_state reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_close_state
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_close_state; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_close_state).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_close_state.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_close_state: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_close_state and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_close_state(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_close_state and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_close_state: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_close_state and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_close_state: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_close_state(*args, **kwargs)
