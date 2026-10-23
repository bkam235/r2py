# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np

# Note: Python strings are Unicode by default. 
# The 'string' function in rlang/R handles specific encodings.
# r2py:entity:cafe
cafe = "caf\uE9"
# Encoding(cafe) equivalent: Python strings are natively Unicode (UTF-8 internally)
# r2py:entity:Encoding
print(type(cafe)) 
# charToRaw(cafe) equivalent: Convert to bytes using UTF-8
# r2py:entity:charToRaw
print(list(cafe.encode('utf-8')))

# cafe_latin1 <- string(c(0x63, 0x61, 0x66, 0xE9), "latin1")
# r2py:entity:cafe_latin1
cafe_latin1 = bytes([0x63, 0x61, 0x66, 0xE9]).decode('latin1')
# Encoding(cafe_latin1) equivalent
# r2py:entity:Encoding_1
print(type(cafe_latin1))
# charToRaw(cafe_latin1) equivalent: Re-encoding back to the original bytes
# r2py:entity:charToRaw_1
print(list(cafe_latin1.encode('latin1')))