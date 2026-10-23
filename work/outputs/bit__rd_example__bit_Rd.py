# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np

# r2py:entity:bit
# bit(12) - In R, bit() creates a bit-vector. 
# 12 in binary is 1100.
d = np.array([int(x) for x in bin(12)[2:].zfill(4)], dtype=bool)
print(d)

# r2py:entity:bit_1
# !bit(12) - Logical NOT
m = ~d
print(m)

# r2py:entity:str
# str(bit(128)) - Structure/Summary of the bit vector.
# 128 in binary is 10000000.
g = np.array([int(x) for x in bin(128)[2:].zfill(8)], dtype=bool)
print(f"Type: {type(g)}")
print(f"Shape: {g.shape}")
print(f"Values: {g}")