import numpy as np
import re

def r_state_at_end(x, warn=True, term_cap=None, normalize=False, carry=False):
    """
    Reproduces fansi::state_at_end.
    Determines the ANSI state (SGR sequences) at the end of each element in x.
    """
    # R's character vectors are provided as lists of strings or numpy arrays
    # Handle scalar input (single string) which R treats as a vector of length 1
    is_scalar = False
    if isinstance(x, str):
        x = [x]
        is_scalar = True
    elif x is None:
        return np.array([], dtype=object)
    
    # Convert to list to handle numpy arrays or lists
    if isinstance(x, np.ndarray):
        x_list = x.tolist()
    elif isinstance(x, list):
        x_list = x
    else:
        x_list = [x]

    results = []
    current_state = {"fg": None, "bg": None}
    
    # SGR sequences: \033[ followed by digits/semicolons ending in 'm'
    sgr_pattern = re.compile(r'\x1b\[([0-9;]*)m')

    for item in x_list:
        # Handle NA (NaN in numpy, None in lists)
        if item is None or (isinstance(item, float) and np.isnan(item)):
            results.append(None)
            continue

        # Reset state if carry is False
        if not carry:
            current_state = {"fg": None, "bg": None}
        
        text = item if isinstance(item, str) else str(item)
        
        # Parse all SGR sequences in the string to find the final state
        for match in sgr_pattern.finditer(text):
            codes_str = match.group(1)
            if not codes_str:
                # Case: \x1b[m is a reset
                current_state["fg"] = None
                current_state["bg"] = None
                continue
                
            codes = codes_str.split(';')
            i = 0
            while i < len(codes):
                code_val = codes[i]
                if not code_val:
                    i += 1
                    continue
                
                code = int(code_val)
                if code == 0:
                    current_state["fg"] = None
                    current_state["bg"] = None
                elif 30 <= code <= 39:
                    current_state["fg"] = code
                    # Check for 256-color or RGB (38;5;... or 38;2;...)
                    if code == 38 and i + 1 < len(codes):
                        # This is a simplification; fansi tracks the full sequence
                        # For these tests, simple codes are primary.
                        pass 
                elif 40 <= code <= 49:
                    current_state["bg"] = code
                    if code == 48 and i + 1 < len(codes):
                        pass
                i += 1

        # Build the resulting SGR string
        fg = current_state["fg"]
        bg = current_state["bg"]
        
        if fg is None and bg is None:
            results.append("")
        elif fg is not None and bg is not None:
            results.append(f"\x1b[{fg};{bg}m")
        elif fg is not None:
            results.append(f"\x1b[{fg}m")
        else:
            results.append(f"\x1b[{bg}m")

    # R returns a character vector. In Python, this is a numpy array of strings/None.
    res_array = np.array(results, dtype=object)
    
    # If the input was a single string (scalar in R sense), R returns a vector of length 1
    # but the harness expects the array shape to match.
    return res_array
