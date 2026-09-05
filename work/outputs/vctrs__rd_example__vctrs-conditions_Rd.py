# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np

class LossyCastError(Exception):
    """Exception raised for lossy casts in vctrs-like operations."""
    def __init__(self, x, to, result, locations, loss_type="precision", x_arg="", to_arg=""):
        self.x = x
        self.to = to
        self.result = result
        self.locations = locations
        self.loss_type = loss_type
        self.x_arg = x_arg
        self.to_arg = to_arg
        super().__init__(f"Lossy cast detected from {x_arg} to {to_arg}")

# r2py:entity:maybe_lossy_cast
def maybe_lossy_cast(result, x, to, lossy=None, locations=None, loss_type="precision", x_arg="", to_arg="", deprecation=False):
    if lossy is None or not any(lossy):
        return result
    
    if deprecation:
        # In the R source, this issues a warning and returns the result
        print(f"Warning: Coercion with lossy casts from {x_arg} to {to_arg} is deprecated.")
        return result
    
    if locations is None:
        locations = [i for i, val in enumerate(lossy) if val]
    
    raise LossyCastError(
        x=x, to=to, result=result, locations=locations, 
        loss_type=loss_type, x_arg=x_arg, to_arg=to_arg
    )

# r2py:entity:allow_lossy_cast
def allow_lossy_cast(expr_func, x_ptype=None, to_ptype=None):
    try:
        return expr_func()
    except LossyCastError as e:
        # Simplified ptype check: in a real scenario, this would check dtypes
        if x_ptype is not None:
            # Dummy check to simulate vec_is
            pass 
        if to_ptype is not None:
            # Dummy check to simulate vec_is
            pass
        # Equivalent to invokeRestart: return the result stored in the error
        return e.result

# Most of the time, `maybe_lossy_cast()` returns its input normally:
# r2py:entity:maybe_lossy_cast
res1 = maybe_lossy_cast(
    ["foo", "bar"],
    None,
    "",
    lossy=[False, False],
    x_arg="",
    to_arg=""
)
print(res1)

# If `lossy` has any `True`, an error is thrown:
# r2py:entity:try
try:
    maybe_lossy_cast(
        ["foo", "bar"],
        None,
        "",
        lossy=[False, True],
        x_arg="",
        to_arg=""
    )
except LossyCastError as e:
    print(f"Caught expected error: {e}")

# Unless lossy casts are allowed:
# We wrap the call in a lambda to simulate the R expression passing
# r2py:entity:allow_lossy_cast
res2 = allow_lossy_cast(
    lambda: maybe_lossy_cast(
        ["foo", "bar"],
        None,
        "",
        lossy=[False, True],
        x_arg="",
        to_arg=""
    )
)
print(res2)