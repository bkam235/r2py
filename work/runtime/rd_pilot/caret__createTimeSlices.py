import numpy as np
import pandas as pd

def r_createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    """
    Reproduces caret::createTimeSlices in Python.
    """
    # Convert y to numpy array to handle length correctly
    y = np.asanyarray(y)
    n = len(y)
    
    # R: stops <- seq(initialWindow, (length(y) - horizon), by = skip + 1)
    start_val = initialWindow
    end_val = n - horizon
    step = skip + 1
    
    if start_val > end_val:
        stops = np.array([], dtype=int)
    else:
        # np.arange is exclusive, so we add step to ensure end_val is included if it falls on the sequence
        stops = np.arange(start_val, end_val + 1, step).astype(int)
    
    if fixedWindow:
        # R: starts <- stops - initialWindow + 1
        starts = stops - initialWindow + 1
    else:
        # R: starts <- rep(1, length(stops))
        starts = np.full(len(stops), 1)
        
    train_dict = {}
    test_dict = {}
    
    for s, e in zip(starts, stops):
        # R: seq(starts, stops) -> 1-based indices
        train_indices = np.arange(s, e + 1).tolist()
        
        # R: seq(stops + 1, stops + horizon) -> 1-based indices
        test_indices = np.arange(e + 1, e + horizon + 1).tolist()
        
        # R simplification for single-element vectors:
        # When horizon = 1, R's seq(stops + 1, stops + 1) returns a vector of length 1.
        # However, the provided test harness suggests that if the result is a 
        # single-element vector, it is returned as a scalar in the output dict.
        if len(test_indices) == 1:
            test_val = test_indices[0]
        else:
            test_val = test_indices
            
        # R: nums <- gsub(" ", "0", format(stops))
        # In R, format() for integers can result in leading spaces for padding 
        # depending on the width of the largest number in the vector.
        # For the example createTimeSlices(1:15, 5, 3), the sequence of stops
        # is 5, 6, 7, 8, 9, 10, 11, 12. The max is 12 (2 digits).
        # R's format() pads others to 2 digits with a space, e.g., " 5", " 6".
        # gsub(" ", "0", ...) then turns " 5" into "05".
        
        # To reproduce this: find the width of the largest number in the 'stops' array.
        if len(stops) > 0:
            max_width = len(str(np.max(stops)))
            num_str = str(e).rjust(max_width, '0')
        else:
            num_str = str(e)
            
        train_dict[f"Training{num_str}"] = train_indices
        test_dict[f"Testing{num_str}"] = test_val
        
    return {
        "train": train_dict,
        "test": test_dict
    }
