import numpy as np
import pandas as pd
import re

def r_close_state(x, warn=True, normalize=False):
    """
    Python reproduction of fansi::close_state.
    
    The function generates the ANSI escape sequences required to reset the 
    terminal state back to default, based on the provided state strings.
    """
    # Ensure x is treated as a sequence
    is_scalar = False
    if isinstance(x, str):
        x = [x]
        is_scalar = True
    elif isinstance(x, (np.ndarray, pd.Series)):
        x_list = x.tolist()
    elif isinstance(x, list):
        x_list = x
    else:
        # Handle single non-string values
        x = [x]
        is_scalar = True
        x_list = x
    
    if not isinstance(x, list) and not hasattr(x, '__iter__'):
        x_list = [x]
    elif hasattr(x, '__iter__'):
        x_list = list(x)
    else:
        x_list = [x]

    results = []
    
    for state in x_list:
        # Handling NA: R's fansi::close_state returns "" for NA state inputs
        if state is None or (isinstance(state, float) and np.isnan(state)):
            results.append("")
            continue
            
        if not isinstance(state, str):
            state = str(state)
            
        # Identify active styles
        has_fg = False
        has_bg = False
        has_bold = False # 1 -> 22
        has_under = False # 4 -> 24
        has_others = False
        
        sequences = re.findall(r'\x1b\[([0-9;]*)m', state)
        
        for seq in sequences:
            params = seq.split(';')
            for p in params:
                if not p: continue
                val = int(p)
                if val == 0:
                    has_fg = has_bg = has_bold = has_under = has_others = False
                elif 30 <= val <= 37 or 38 == val or 90 <= val <= 97 or 100 == val:
                    has_fg = True
                elif 40 <= val <= 47 or 48 == val or 100 <= val <= 107 or 108 == val:
                    has_bg = True
                elif val == 1:
                    has_bold = True
                elif val == 4:
                    has_under = True
                else:
                    has_others = True
        
        if normalize:
            res = ""
            # Normalized close sequences for specific attributes
            if has_bold:
                res += "\x1b[22m"
            if has_under:
                res += "\x1b[24m"
            if has_fg:
                res += "\x1b[39m"
            if has_bg:
                res += "\x1b[49m"
            
            # If we have other styles but not bold/under/fg/bg, 
            # normalization usually falls back to 0m or remains empty
            if not res and (has_others or has_bold or has_under or has_fg or has_bg):
                res = "\x1b[0m"
                
            results.append(res)
        else:
            # Non-normalized: if any state is active, use the global reset
            if has_fg or has_bg or has_bold or has_under or has_others:
                results.append("\x1b[0m")
            else:
                results.append("")

    # Return numpy array for vectors, scalar for scalar input
    final_res = np.array(results, dtype=object)
    
    if is_scalar:
        return final_res[0]
    return final_res
