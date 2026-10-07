import numpy as np

def r_createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    """
    Python reproduction of caret::createTimeSlices
    """
    # y is provided as a numpy array.
    n = len(y)
    
    # R's seq(from, to, by)
    # stops <- seq(initialWindow, (length(y) - horizon), by = skip + 1)
    # In R, seq handles limits such that if to < from, it returns an empty sequence.
    start_val = initialWindow
    end_val = n - horizon
    step = skip + 1
    
    if start_val > end_val:
        stops = np.array([], dtype=int)
    else:
        # Calculate number of elements: floor((to - from)/by) + 1
        num = int((end_val - start_val) // step) + 1
        stops = np.arange(start_val, start_val + num * step, step)

    if fixedWindow:
        # starts <- stops - initialWindow + 1
        starts = stops - initialWindow + 1
    else:
        # starts <- rep(1, length(stops))
        starts = np.full(len(stops), 1)

    train_dict = {}
    test_dict = {}
    
    for i in range(len(stops)):
        s_start = int(starts[i])
        s_stop = int(stops[i])
        
        # R: seq(starts, stops) -> 1-based inclusive
        # Python: range(s_start, s_stop + 1)
        train_indices = list(range(s_start, s_stop + 1))
        
        # R: seq(stops + 1, stops + horizon)
        test_start = s_stop + 1
        test_stop = s_stop + horizon
        test_indices = list(range(test_start, test_stop + 1))
        
        # Formatting logic for names
        # nums <- gsub(" ", "0", format(stops))
        # In R, format() on a number usually results in a string. 
        # For simple integers, it's just the string representation.
        num_str = str(s_stop)
        
        train_key = f"Training{num_str}"
        test_key = f"Testing{num_str}"
        
        train_dict[train_key] = train_indices
        
        # If horizon is 1, R returns a single value instead of a sequence for the test set
        # based on the example output provided in the prompt.
        if horizon == 1:
            test_dict[test_key] = test_indices[0]
        else:
            test_dict[test_key] = test_indices

    return {"train": train_dict, "test": test_dict}
