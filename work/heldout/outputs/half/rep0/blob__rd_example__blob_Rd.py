# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np

# R's blob package handles raw byte arrays. 
# In Python, 'bytes' or 'bytearray' are the equivalents.

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
# new_blob(list(x1, x2))
# In Python, this is represented as a list of byte objects
new_blob_result = [x1, x2]

# r2py:entity:blob
# blob(x1, x2)
# In Python, this is represented as a tuple of byte objects
blob_result = (x1, x2)

# r2py:entity:as.blob
# as.blob(c("Good morning", "Good evening"))
# Translating a vector of strings to a list of bytes
as_blob_result = [s.encode('utf-8') for s in ["Good morning", "Good evening"]]