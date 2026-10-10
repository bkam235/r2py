import numpy as np
import re

def _r2py_impl_r_state_at_end(x, warn=True, term_cap="auto", normalize=False, carry=False):
    """
    Determine ANSI SGR state at end of each string in character vector.
    
    Parameters:
    x: string or numpy array of strings (may contain NaN for NA)
    warn: whether to warn about issues
    term_cap: terminal capability
    normalize: whether to normalize SGR sequences
    carry: whether to carry state from one element to the next
    
    Returns:
    numpy array of strings representing SGR codes at end of each input string
    """
    
    # Handle scalar input
    if isinstance(x, str):
        x = np.array([x], dtype=object)
    elif not isinstance(x, np.ndarray):
        x = np.array(x, dtype=object)
    else:
        # Ensure we're working with object dtype
        x = x.astype(object)
    
    result = np.empty(len(x), dtype=object)
    
    # Current state as we process strings
    current_state = set()  # Set of active SGR codes
    
    # Pattern to match ANSI SGR sequences: ESC [ ... m
    sgr_pattern = re.compile(r'\x1b\[([0-9;]*)m')
    
    for i, s in enumerate(x):
        # Handle NaN/None (NA values)
        if s is None or (isinstance(s, float) and np.isnan(s)):
            result[i] = None
            continue
        
        if not isinstance(s, str):
            s = str(s)
        
        # Find all SGR codes in this string
        matches = list(sgr_pattern.finditer(s))
        
        if not matches:
            # No SGR codes, state stays same (or empty if carry=False)
            if carry:
                result[i] = _sgr_from_state(current_state)
            else:
                result[i] = ""
        else:
            if carry:
                # Update state with all codes found in this string
                for match in matches:
                    codes_str = match.group(1)
                    _update_state(current_state, codes_str)
                result[i] = _sgr_from_state(current_state)
            else:
                # Just get the state from all SGR codes in this string
                state = set()
                for match in matches:
                    codes_str = match.group(1)
                    _update_state(state, codes_str)
                result[i] = _sgr_from_state(state)
    
    return result


def _update_state(state, codes_str):
    """Update graphics state with new SGR codes."""
    if not codes_str:
        # Empty codes mean reset
        state.clear()
        return
    
    codes = []
    for c in codes_str.split(';'):
        if c:
            codes.append(int(c))
    
    for code in codes:
        if code == 0:
            # Reset all
            state.clear()
        elif code == 1:
            state.add(1)  # Bold
        elif code == 4:
            state.add(4)  # Underline
        elif code == 7:
            state.add(7)  # Reverse
        elif 30 <= code <= 37:
            # Foreground colors - remove old foreground, add new
            for fg in range(30, 38):
                state.discard(fg)
            state.add(code)
        elif 40 <= code <= 47:
            # Background colors - remove old background, add new
            for bg in range(40, 48):
                state.discard(bg)
            state.add(code)


def _sgr_from_state(state):
    """Convert state set back to SGR escape sequence."""
    if not state:
        return ""
    
    codes = sorted(list(state))
    return f"\x1b[{';'.join(str(c) for c in codes)}m"


_R2PY_UNVERIFIED_r_state_at_end = {'carry': ['True'], 'normalize': ['True'], 'warn': ['False']}
_R2PY_UNVERIFIED_CLASSES_r_state_at_end = []


def _r2py_items_r_state_at_end(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_state_at_end(*args, **kwargs):
    """r_state_at_end reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_state_at_end
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_state_at_end; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_state_at_end).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_state_at_end.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_state_at_end: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_state_at_end and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_state_at_end(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_state_at_end and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_state_at_end: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_state_at_end and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_state_at_end: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_state_at_end(*args, **kwargs)
