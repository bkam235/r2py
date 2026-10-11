import numpy as np
import re

def r_state_at_end(x, warn=True, term_cap=None, normalize=False, carry=False):
    """
    Reproduces the fansi::state_at_end R function.
    The function extracts the ANSI escape sequences that determine the 
    visual state (SGR - Select Graphic Rendition) at the end of each string.
    """
    # Handle input types to match R's vector behavior
    if x is None:
        return np.array([], dtype=object)
    
    # If x is a single string, R treats it as a vector of length 1
    if isinstance(x, str):
        x_vec = [x]
    elif isinstance(x, (list, np.ndarray)):
        x_vec = x
    else:
        x_vec = [x]
    
    results = []
    # State stores current active SGR codes
    # Use a dictionary to track categories
    current_state = {"fg": None, "bg": None, "others": set()}
    
    for text in x_vec:
        # Handle NA (NaN in numpy array)
        if text is None or (isinstance(text, float) and np.isnan(text)):
            # R's fansi::state_at_end typically returns NA for NA input
            results.append(np.nan)
            continue
            
        # Ensure text is a string
        text = str(text)
        
        # If carry is False, we reset state for every element in the vector
        if not carry:
            current_state = {"fg": None, "bg": None, "others": set()}

        # Find all SGR sequences: \x1b[...m
        matches = re.finditer(r'\x1b\[([0-9;]*)m', text)
        
        for match in matches:
            params_str = match.group(1)
            if not params_str:
                # \x1b[m is a reset all
                current_state = {"fg": None, "bg": None, "others": set()}
            else:
                params = params_str.split(';')
                for p in params:
                    if not p: continue
                    try:
                        val = int(p)
                    except ValueError:
                        continue
                    
                    if val == 0:
                        current_state = {"fg": None, "bg": None, "others": set()}
                    elif 30 <= val <= 37 or 90 <= val <= 97:
                        current_state["fg"] = val
                    elif 40 <= val <= 47 or 100 <= val <= 107:
                        current_state["bg"] = val
                    else:
                        # Toggle logic for other SGR codes (like Bold 1, Underline 4)
                        if val in current_state["others"]:
                            current_state["others"].remove(val)
                        else:
                            current_state["others"].add(val)
        
        # Reconstruct the state string
        # Order usually: others (sorted), then fg, then bg
        final_codes = []
        for v in sorted(list(current_state["others"])):
            final_codes.append(str(v))
        if current_state["fg"] is not None:
            final_codes.append(str(current_state["fg"]))
        if current_state["bg"] is not None:
            final_codes.append(str(current_state["bg"]))
            
        if not final_codes:
            results.append("")
        else:
            results.append(f"\x1b[{';'.join(final_codes)}m")

    # Return as numpy array of objects to allow mixed strings and NaNs
    res_array = np.array(results, dtype=object)
    
    # If the input was a single string (scalar-like in R), 
    # R returns a character vector. In Python, we maintain the array 
    # unless the harness expects a specific scalar.
    return res_array
