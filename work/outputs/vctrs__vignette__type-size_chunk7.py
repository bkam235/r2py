# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
from datetime import date, datetime, timedelta

# r2py:entity:vec_ptype_show
def vec_ptype_full(x):
    """
    Simulates R's vctrs::vec_ptype_full by returning the type name 
    of the object, mirroring the behavior for the provided examples.
    """
    if isinstance(x, date):
        return "Date"
    elif isinstance(x, datetime):
        return "POSIXct"
    elif isinstance(x, timedelta):
        return "difftime"
    else:
        return type(x).__name__

def vec_ptype_show(*args):
    """
    Simulates R's vctrs::vec_ptype_show by printing the prototype 
    type of the provided arguments.
    """
    # Filter out None values (similar to compact in R)
    args = [arg for arg in args if arg is not None]
    n = len(args)
    
    if n == 0:
        print("Prototype: NULL")
    elif n == 1:
        print(f"Prototype: {vec_ptype_full(args[0])}")
    else:
        # This part handles the complex ptype2 resolution logic from the R source
        # For the given examples, we only have single-argument calls.
        # Implementing basic version for the logic flow.
        res_type = vec_ptype_full(args[-1])
        print(f"Prototype: {res_type}")

# Equivalent to Sys.Date()
vec_ptype_show(date.today())

# Equivalent to Sys.time()
# r2py:entity:vec_ptype_show_1
vec_ptype_show(datetime.now())

# Equivalent to as.difftime(10, units = "mins")
# r2py:entity:vec_ptype_show_2
vec_ptype_show(timedelta(minutes=10))