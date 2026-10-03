# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np

# x1 <- charToRaw("Good morning")
# r2py:entity:x1
x1 = "Good morning".encode('utf-8')

# x2 <- as.raw(c(0x48, 0x65, 0x6c, 0x6c, 0x6f))
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# new_blob(list(x1, x2))
# r2py:entity:new_blob
print(f"<blob[{len([x1, x2])}]>")
print(f"[1] blob[{len(x1)} B] blob[{len(x2)} B]")

# r2py:entity:blob
blob = [x1, x2]
print(f"<blob[{len(blob)}]>")
print(f"[1] blob[{len(x1)} B] blob[{len(x2)} B]")

# r2py:entity:as.blob
as_blob = ["Good morning".encode('utf-8'), "Good evening".encode('utf-8')]
print(as_blob)