# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import base64
import numpy as np

# base64encode(1:100)
# r2py:entity:base64encode
d = np.arange(1, 101, dtype=np.int8).tobytes()
print(base64.b64encode(d).decode('utf-8'))

# base64encode(1:100, 70)
# Python's base64.b64encode does not take a width parameter; 
# we simulate wrapping manually for a width of 70
# r2py:entity:base64encode_1
encoded = base64.b64encode(d).decode('utf-8')
wrapped = '\n'.join([encoded[i:i+70] for i in range(0, len(encoded), 70)])
print(wrapped)

# base64encode(1:100, 70, "\n")
# Similar to above, the line ending is explicitly \n
# r2py:entity:base64encode_2
print(wrapped)

# x <- charToRaw("the decoded content, otherwise the number of bytes")
# r2py:entity:x
x = "the decoded content, otherwise the number of bytes".encode('utf-8')

# y <- base64decode(base64encode(x))
# r2py:entity:y
y = base64.b64decode(base64.b64encode(x))

# stopifnot(identical(x, y))
# r2py:entity:stopifnot
assert x == y