# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np

# r2py:entity:vec_size_common
def vec_size_common(*args):
    # In R's vctrs, vec_size_common returns the common size if all 
    # are the same, or 1 if they differ (following R's recycling rules)
    # except if any are length 0, it returns 0.
    sizes = [len(x) if hasattr(x, '__len__') else 1 for x in args]
    
    if any(s == 0 for s in sizes):
        return 0
    
    if all(s == sizes[0] for s in sizes):
        return sizes[0]
    
    return 1

# vec_size_common(1:3, 1:3, 1:3)
# r2py:entity:vec_size_common
print(vec_size_common(list(range(1, 4)), list(range(1, 4)), list(range(1, 4))))

# vec_size_common(1:10, 1)
# r2py:entity:vec_size_common_1
print(vec_size_common(list(range(1, 11)), [1]))

# vec_size_common(integer(), 1)
# r2py:entity:vec_size_common_2
print(vec_size_common([], [1]))