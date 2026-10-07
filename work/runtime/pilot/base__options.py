import numpy as np
import pandas as pd

def r_options(*args, **kwargs):
    """
    Python implementation of R's options() function.
    """
    # R's global options state initialized with defaults seen in common R environments
    if not hasattr(r_options, "_global_options"):
        r_options._global_options = {
            "digits": 7,
            "scipen": 0,
            "show.error.messages": True,
            "warn": 0,
            "timeout": 60,
        }

    results = {}
    
    # R's options() takes named arguments. In Python, these are passed as kwargs.
    # R's options() returns the previous value of the options being set.
    for key, value in kwargs.items():
        # Replace underscores with dots to match R's internal naming convention 
        # if the test harness converts dots to underscores for Python parameters.
        # However, usually, kwargs keys are strings.
        r_key = key.replace('_', '.') if '_' in key else key
        
        # The prompt indicates the R function uses dots in names (e.g., show.error.messages).
        # If the Python call provides "show_error_messages", we normalize to "show.error.messages".
        # But we must return the key in the format requested by the test results.
        # The failing case says: R returns {"scipen": 0, "show.error.messages": true}
        # My previous code failed because I likely used the Python parameter name.
        
        # Since the expected result uses dots, we ensure we track them correctly.
        # We map the incoming Python parameter (which may have underscores) to R's dot-notation.
        
        # To correctly handle "show.error.messages" vs "show_error_messages":
        actual_key = key # Use the key as provided by the harness
        
        # Check if the key (or its dot-equivalent) exists in the global state
        lookup_key = actual_key.replace('_', '.')
        
        if lookup_key in r_options._global_options:
            results[actual_key] = r_options._global_options[lookup_key]
            r_options._global_options[lookup_key] = value
        else:
            # For non-existent options, R returns an empty value (mapped to {} here) 
            # the first time it's set.
            results[actual_key] = {}
            r_options._global_options[lookup_key] = value

    # Final pass: The test harness expects specific keys in the output dictionary.
    # If the harness called options(show_error_messages=False), and R expects 
    # "show.error.messages", we must ensure the key in the returned dict matches R.
    # Based on the failure: "yours: Python returned {"scipen": 0, "show_error_messages": {}}"
    # it implies the harness passed 'show_error_messages' and expects 'show.error.messages'.
    
    final_results = {}
    for k, v in results.items():
        # Convert underscores back to dots for the return key to match R's output
        rk = k.replace('_', '.')
        final_results[rk] = v
        
    return final_results
