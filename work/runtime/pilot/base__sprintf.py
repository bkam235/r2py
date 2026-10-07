import numpy as np
import pandas as pd

def r_sprintf(fmt=None, *args, **kwargs):
    """
    Reproduces R's sprintf function.
    R's sprintf handles vectorization of arguments by recycling them.
    NA in R's sprintf is converted to the string "NA".
    """
    # Python's function signature (fmt=None, *args) causes a TypeError 
    # if the user passes both a positional argument (which goes to fmt) 
    # and a keyword argument for fmt. However, R's sprintf allows 
    # calling it as sprintf("fmt", arg) or sprintf(fmt="fmt", arg).
    # To avoid "multiple values for argument 'fmt'", we handle 
    # positional vs keyword separately.
    
    # Because of the way Python handles arguments, if the user calls 
    # r_sprintf("Hello %s", "World"), "Hello %s" is fmt and "World" is in args.
    # If the user calls r_sprintf(fmt="Hello %s", "World"), this is a SyntaxError 
    # in Python (positional args cannot follow keyword args).
    # If they call r_sprintf(fmt="Hello %s", width=10), "Hello %s" is fmt and 
    # width=10 is in kwargs.
    
    # The error "multiple values for argument 'fmt'" happens if the test 
    # harness is calling the function in a way that conflicts with the signature.
    # Let's use a more flexible signature.
    pass

def r_sprintf(*args, **kwargs):
    # Map the first argument to fmt, whether it was positional or keyword
    if 'fmt' in kwargs:
        fmt = kwargs.pop('fmt')
        # Positionals are the ... part
        pos_args = list(args)
    else:
        if not args:
            return ""
        fmt = args[0]
        pos_args = list(args[1:])

    # R's ... collects all positional arguments and then any named ones
    # based on the example: sprintf("%s %s", letters[1:2], width = 10)
    # 'width' becomes an argument in the ... sequence.
    all_args = pos_args + list(kwargs.values())

    if not all_args:
        return fmt

    # Convert args to numpy arrays for easy handling of lengths and NAs
    processed_args = []
    for arg in all_args:
        if isinstance(arg, (list, np.ndarray, pd.Series)):
            arr = np.array(arg, dtype=object)
        else:
            arr = np.array([arg], dtype=object)
        
        def is_na(x):
            try:
                return x is None or (isinstance(x, (float, np.floating)) and np.isnan(x))
            except:
                return False
        
        mask = np.array([is_na(x) for x in arr])
        arr[mask] = "NA"
        processed_args.append(arr)

    # Determine the length of the output vector (R recycling)
    max_len = max(len(a) for a in processed_args)
    
    final_args = []
    for a in processed_args:
        repeated = np.resize(a, max_len)
        final_args.append(repeated)

    zipped_args = zip(*final_args)
    
    results = []
    for args_tuple in zipped_args:
        try:
            # Python's % operator
            res = fmt % args_tuple
            results.append(res)
        except TypeError:
            # Handle cases where types don't match % specifier (e.g. %d with string)
            # R is more lenient or handles internal casting.
            results.append(fmt % tuple(str(x) for x in args_tuple))

    if len(results) == 1:
        return results[0]
    else:
        return results
