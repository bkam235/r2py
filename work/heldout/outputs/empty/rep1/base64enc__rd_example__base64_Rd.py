# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import base64
import numpy as np

# base64encode(1:100)
# In R, 1:100 as raw data is typically treated as a sequence of bytes
# r2py:entity:base64encode
d1 = np.arange(1, 101, dtype=np.uint8).tobytes()
print(base64.b64encode(d1).decode('utf-8'))

# base64encode(1:100, 70)
# R's base64encode with a width argument wraps the output
# r2py:entity:base64encode_1
encoded_70 = base64.b64encode(d1).decode('utf-8')
wrapped_70 = '\n'.join(encoded_70[i:i+70] for i in range(0, len(encoded_70), 70))
print(wrapped_70)

# base64encode(1:100, 70, "\n")
# In the provided R snippet, the third argument is the delimiter. 
# Since we already used \n, this is functionally equivalent to the above.
# r2py:entity:base64encode_2
print(wrapped_70)

# x <- charToRaw("the decoded content, otherwise the number of bytes")
# r2py:entity:x
x = "the decoded content, otherwise the number of bytes".encode('utf-8')

# y <- base64decode(base64encode(x))
# r2py:entity:y
y = base64.b64decode(base64.b64encode(x))

# stopifnot(identical(x, y))
# r2py:entity:stopifnot
assert x == y