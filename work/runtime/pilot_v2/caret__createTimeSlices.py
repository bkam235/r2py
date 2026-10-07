import numpy as np

def r_createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    """
    Reproduces caret::createTimeSlices in Python.
    """
    # length(y) in R
    n = len(y)
    
    # stops <- seq(initialWindow, (length(y) - horizon), by = skip + 1)
    start_val = initialWindow
    end_val = n - horizon
    step = skip + 1
    
    if start_val > end_val:
        stops = []
    else:
        # Calculate number of elements to match R's seq behavior
        num_elements = int((end_val - start_val) // step) + 1
        stops = [start_val + i * step for i in range(num_elements)]
    
    if fixedWindow:
        # starts <- stops - initialWindow + 1
        starts = [s - initialWindow + 1 for s in stops]
    else:
        # starts <- rep(1, length(stops))
        starts = [1] * len(stops)
    
    # train <- mapply(seq, starts, stops, SIMPLIFY = FALSE)
    train_list = {}
    # test <- mapply(seq, stops + 1, stops + horizon, SIMPLIFY = FALSE)
    test_list = {}
    
    for i in range(len(stops)):
        s_start = starts[i]
        s_stop = stops[i]
        
        # Training: sequence from s_start to s_stop inclusive
        train_indices = list(range(s_start, s_stop + 1))
        
        # Testing: sequence from s_stop + 1 to s_stop + horizon inclusive
        t_start = s_stop + 1
        t_stop = s_stop + horizon
        test_indices = list(range(t_start, t_stop + 1))
        
        # R's seq(a, b) returns a scalar if a == b. 
        # Based on the failure case: "test": {"Testing5": 6...} instead of [6]
        # we must handle the scalar return for single-element sequences.
        if len(test_indices) == 1:
            test_val = test_indices[0]
        else:
            test_val = test_indices
            
        if len(train_indices) == 1:
            train_val = train_indices[0]
        else:
            train_val = train_indices

        # nums <- gsub(" ", "0", format(stops))
        num_str = str(s_stop).replace(" ", "0")
        
        train_list[f"Training{num_str}"] = train_val
        test_list[f"Testing{num_str}"] = test_val
        
    return {
        "train": train_list,
        "test": test_list
    }
