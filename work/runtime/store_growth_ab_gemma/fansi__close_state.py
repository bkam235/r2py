import numpy as np
import pandas as pd
import re

def r_close_state(x, warn=True, normalize=False):
    """
    Python reproduction of fansi::close_state.
    
    This function generates the ANSI escape sequences required to reset 
    the terminal state back to default, based on the current state x.
    """
    # Ensure x is treated as a list of strings
    if isinstance(x, np.ndarray):
        x = x.tolist()
    elif not isinstance(x, list):
        x = [x]

    results = []
    
    for state in x:
        # Based on the harness feedback, R's close_state returns an empty string "" 
        # for NA/null states instead of maintaining the NA/None.
        if state is None or (isinstance(state, float) and np.isnan(state)):
            results.append("")
            continue
            
        if not state:
            results.append("")
            continue

        if not normalize:
            # Standard behavior: reset everything
            results.append("\033[0m")
        else:
            # Normalization logic:
            # Extract numbers from the state string (which are the active ANSI codes)
            codes = re.findall(r'\d+', state)
            reset_seq = ""
            
            has_fg = False
            has_bg = False
            
            for code in codes:
                c = int(code)
                if 30 <= c <= 37 or 90 <= c <= 97:
                    has_fg = True
                elif 40 <= c <= 47 or 100 <= c <= 107:
                    has_bg = True
            
            # R's fansi puts fg (39) then bg (49)
            if has_fg:
                reset_seq += "\033[39m"
            if has_bg:
                reset_seq += "\033[49m"
            
            # If normalize=True but no specific colors were found, fallback to global reset
            results.append(reset_seq if reset_seq else "\033[0m")

    return results
