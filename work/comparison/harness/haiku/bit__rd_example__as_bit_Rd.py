import numpy as np
from typing import Optional, Union

class BitArray:
    """Bit array class mimicking R's bit package"""
    def __init__(self, data: np.ndarray):
        self.data = np.asarray(data, dtype=bool)
        self.length = len(self.data)
    
    def __repr__(self):
        # Format: "bit length=N occupying only 1 int32\n<indices>\n<values>"
        indices = "    " + "".join(f"{i+1:>6}" for i in range(self.length))
        values = " ".join(f"{'TRUE' if v else 'FALSE':>5}" for v in self.data)
        return f"bit length={self.length} occupying only 1 int32\n{indices} \n{values} "

# r2py:entity:as.bit_2
def as_bit(x: Optional[Union[list, np.ndarray]]) -> BitArray:
    """Convert input to bit array"""
    if x is None:
        return BitArray(np.array([], dtype=bool))
    
    x_array = np.asarray(x)
    result = np.zeros(len(x_array), dtype=bool)
    
    # Handle different input types uniformly: 0 → False, non-0 → True, NA → False
    for i, val in enumerate(x_array):
        # Check for NA/None/NaN
        if val is None:
            result[i] = False
        elif isinstance(val, float) and np.isnan(val):
            result[i] = False
        else:
            # Non-zero is True, zero is False
            result[i] = bool(val != 0)
    
    return BitArray(result)

# r2py:entity:as.bit
print(as_bit([0, 1, 2, -2, None]))
# r2py:entity:as.bit_1
print(as_bit([0.0, 1.0, 2.0, -2.0, np.nan]))
# r2py:entity:as.bit_2
print(as_bit([False, None, True]))