# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import numpy as np

# r2py:entity:deg_min_color
def deg_min_color(x, direction):
    pm = ["N", "S"] if direction == "lat" else ["E", "W"]
    
    sign_val = np.sign(x)
    abs_x = abs(x)
    deg = int(abs_x)
    rem = abs_x - deg
    rad = int(round(rem * 60))
    
    # Note: pillar::style_subtle is for console formatting; 
    # standard strings are used here for general Python compatibility.
    suffix = pm[0] if sign_val >= 0 else pm[1]
    
    ret = f"{deg}°{rad:02d}'{suffix}"
    
    return ret.rjust()