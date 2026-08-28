# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

import numpy as np
import pandas as pd

# r2py:entity:as.bit
class BitArray:
    def __init__(self, data):
        # as.bit logic: 0/FALSE/NA -> FALSE, others -> TRUE
        # Based on R output: 
        # c(0L, 1L, 2L, -2L, NA) -> FALSE TRUE TRUE TRUE FALSE
        # c(FALSE, NA, TRUE) -> FALSE FALSE TRUE
        self.length = len(data)
        self.values = []
        for val in data:
            if pd.isna(val) or val == 0 or val is False:
                self.values.append(False)
            else:
                self.values.append(True)
    
    def __str__(self):
        # Mimic R's print output for bit objects
        # Example:
        #       bit length=5 occupying only 1 int32
        # 1     2     3     4     5 
        # FALSE  TRUE  TRUE  TRUE FALSE
        
        # Calculate 'occupying' (simplified)
        # R's .BITS is usually 32 or 64. 1 int32 can hold 32 bits.
        ints_needed = (self.length + 31) // 32 if self.length > 0 else 0
        header = f"      bit length={self.length} occupying only {ints_needed} int32"
        
        indices = " ".join([str(i+1).rjust(5) for i in range(self.length)])
        vals = " ".join([str(v).upper().rjust(5) for v in self.values])
        
        return f"{header}\n{indices}\n{vals}"

def as_bit(data):
    return BitArray(data)

# as.bit(c(0L, 1L, 2L, -2L, NA))
print(as_bit([0, 1, 2, -2, np.nan]))

# as.bit(c(0, 1, 2, -2, NA))
# r2py:entity:as.bit_1
print(as_bit([0, 1, 2, -2, np.nan]))

# as.bit(c(FALSE, NA, TRUE))
# r2py:entity:as.bit_2
print(as_bit([False, np.nan, True]))