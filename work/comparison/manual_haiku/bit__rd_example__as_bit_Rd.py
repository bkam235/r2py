# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: as.bit.Rd
# Translated from R to Python

# Note: The 'bit' package is a specialized R package for bit-level operations.
# Python doesn't have a direct equivalent, but bitwise operations and numpy can be used.

import numpy as np

# Convert integers to binary representation
values_int = [0, 1, 2, -2, None]
values_float = [0.0, 1.0, 2.0, -2.0, None]
values_bool = [False, None, True]

# Convert to binary strings (simulating as.bit behavior)
def as_bit(values):
    """Convert values to bit representation"""
    result = []
    for v in values:
        if v is None:
            result.append(None)
        elif isinstance(v, bool):
            result.append(1 if v else 0)
        else:
            result.append(1 if int(v) else 0)
    return result

print(as_bit(values_int))
print(as_bit(values_float))
print(as_bit(values_bool))
