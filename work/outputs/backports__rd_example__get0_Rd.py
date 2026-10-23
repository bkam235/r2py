# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np

# r2py:entity:bp_get0
def get0(name, ifnotfound=None):
    """
    Substitute for R's get0: retrieves the value of a variable by its name
    from the global scope.
    """
    return globals().get(name, ifnotfound)

# bp_get0("a")
# r2py:entity:bp_get0_1
print(get0("a"))

# bp_get0("a", ifnotfound = 0)
# r2py:entity:bp_get0_2
print(get0("a", ifnotfound=0))

# r2py:entity:foo
foo = 12
# bp_get0("foo")
# r2py:entity:bp_get0_3
print(get0("foo"))