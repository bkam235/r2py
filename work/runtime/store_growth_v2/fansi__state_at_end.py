import numpy as np
import re

def _r2py_impl_r_state_at_end(x, warn=True, term_cap=None, normalize=False, carry=False):
    """
    Reproduces fansi::state_at_end.
    Determines the ANSI escape state at the end of each string in a vector.
    """
    # Ensure x is treated as a list/array of strings
    if isinstance(x, str):
        x_vec = [x]
    elif isinstance(x, np.ndarray):
        x_vec = x
    else:
        x_vec = list(x)

    # ANSI SGR (Select Graphic Rendition) pattern
    ansi_pattern = re.compile(r'\x1b\[([0-9;]*)m')
    
    results = []
    # Global state across elements if carry=True
    global_state = {} # category -> value

    def get_sgr_category(code):
        # Foreground: 30-37, 38, 90-97, 98
        if 30 <= int(code) <= 37 or 90 <= int(code) <= 97 or int(code) == 38 or int(code) == 98:
            return 'fg'
        # Background: 40-47, 48, 100-107, 108
        if 40 <= int(code) <= 47 or 100 <= int(code) <= 107 or int(code) == 48 or int(code) == 108:
            return 'bg'
        return 'other'

    for item in x_vec:
        # Handle NA (NaN in numpy arrays for strings usually implies None or "nan")
        if item is None or (isinstance(item, float) and np.isnan(item)):
            results.append(None)
            continue
            
        # If not carrying, start with a fresh state for this element
        local_state = global_state.copy() if carry else {}
        
        # If it's not a string (e.g. numeric), it doesn't change state
        if not isinstance(item, str):
            item_str = str(item)
        else:
            item_str = item

        matches = ansi_pattern.finditer(item_str)
        for match in matches:
            params_str = match.group(1)
            if not params_str:
                # \x1b[m is usually interpreted as \x1b[0m (Reset)
                local_state = {}
                continue
                
            params = params_str.split(';')
            for p in params:
                if not p: continue
                try:
                    val = int(p)
                    if val == 0:
                        local_state = {}
                    else:
                        cat = get_sgr_category(val)
                        if cat != 'other':
                            local_state[cat] = val
                        # Note: 'other' codes (like bold/italic) are not typically 
                        # tracked in the 'state' return of fansi's state_at_end
                        # unless specific to the package's implementation.
                except ValueError:
                    pass
        
        # Update global state if carrying
        if carry:
            global_state = local_state.copy()

        # Construct the sequence. R's fansi typically outputs fg then bg.
        state_parts = []
        if 'fg' in local_state:
            state_parts.append(str(local_state['fg']))
        if 'bg' in local_state:
            state_parts.append(str(local_state['bg']))
            
        if not state_parts:
            results.append("")
        else:
            results.append(f"\x1b[{';'.join(state_parts)}m")

    # The harness expects a numpy array of objects (character vector)
    # In R, state_at_end on a single string returns a character vector of length 1.
    res_array = np.array(results, dtype=object)
    
    # Handle the case where R returns a scalar-like character vector
    # The harness typically expects the numpy array representation of the R vector.
    return res_array


_R2PY_UNVERIFIED_r_state_at_end = {'normalize': ['True']}
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
