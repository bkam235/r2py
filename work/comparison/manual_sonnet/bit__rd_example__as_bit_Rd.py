# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: as.bit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 5

import numpy as np


def as_bit(x):
    """Convert values to boolean bit vector (non-zero -> True, 0 -> False, None/NaN -> None)."""
    result = []
    for v in x:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            result.append(None)
        else:
            result.append(bool(v))
    return result


print(as_bit([0, 1, 2, -2, None]))       # integers
print(as_bit([0.0, 1.0, 2.0, -2.0, None]))  # doubles
print(as_bit([False, None, True]))        # logicals
