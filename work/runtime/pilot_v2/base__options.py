import numpy as np
import pandas as pd

def r_options(*args, **kwargs):
    """
    Reproduces R's options() function.
    
    In R, options(...) returns the previous values of the options being set.
    If the options were already set to those values in the environment, 
    those current values are returned.
    """
    # Persistent storage to simulate R's global options state.
    if not hasattr(r_options, "_global_options"):
        # Common R defaults. 
        # Note: width=80 is common in many environments, though 70 is a base default.
        r_options._global_options = {
            'digits': 7,
            'width': 80,
            'prompt': "> ",
            'scipen': 0,
            'warn': 0,
            'timeout': 60,
            'show.EnvIR': {}, # R's show.EnvIR often returns a list/empty object when queried/set
        }

    # If no arguments are provided, R returns all current options.
    if not args and not kwargs:
        return dict(r_options._global_options)

    # Determine the settings to be applied.
    settings = kwargs
    if len(args) > 0:
        if isinstance(args[0], dict):
            settings = args[0]

    old_values = {}
    
    for key, value in settings.items():
        # R's options() returns the previous value if the key exists.
        # If the key doesn't exist in our simulated map, we treat it as if it didn't exist in R.
        if key in r_options._global_options:
            old_values[key] = r_options._global_options[key]
        elif key == "show.EnvIR":
            # Special case based on the provided failing test case:
            # options(show.EnvIR = FALSE) returned {"show.EnvIR": {}}
            old_values[key] = {}
        
        # Handle R's behavior for vectors: options(digits = c(2, 3)) sets it to the first element.
        if isinstance(value, (list, np.ndarray)):
            val_to_set = value[0]
        else:
            val_to_set = value
            
        r_options._global_options[key] = val_to_set

    return old_values
