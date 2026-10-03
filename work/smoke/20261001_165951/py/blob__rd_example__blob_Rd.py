# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np

# R's blob package handles raw binary data. In Python, this is equivalent to 'bytes'.
# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
# new_blob(list(x1, x2))
# Represents a collection of binary objects
new_blob_result = [x1, x2]
print(f"<blob[{len(new_blob_result)}]>")
for b in new_blob_result:
    print(f"blob[{len(b)} B]", end=" ")
print()

# r2py:entity:blob
# blob(x1, x2)
blob_result = [x1, x2]
print(f"<blob[{len(blob_result)}]>")
print("[1]", end=" ")
for b in blob_result:
    print(f"blob[{len(b)} B]", end=" ")
print()

# r2py:entity:as.blob
# as.blob(c("Good morning", "Good evening"))
# Converting a character vector to a list of binary objects
as_blob = [s.encode('utf-8') for s in ["Good morning", "Good evening"]]
print(as_blob)