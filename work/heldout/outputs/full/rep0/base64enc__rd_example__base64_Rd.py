# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import base64
import numpy as np

# r2py:entity:base64encode
def base64encode_impl(what, linewidth=0, newline=None):
    if isinstance(what, str):
        data = what.encode('utf-8')
    elif isinstance(what, (bytes, bytearray)):
        data = what
    else:
        data = np.asanyarray(what).astype(np.uint8).tobytes()
    
    encoded = base64.b64encode(data).decode('ascii')
    
    if linewidth <= 0:
        return encoded
    
    # R's base64encode ensures linewidth is a multiple of 4
    actual_width = (linewidth // 4) * 4
    if actual_width == 0: 
        actual_width = 4
        
    lines = [encoded[i:i+actual_width] for i in range(0, len(encoded), actual_width)]
    
    if newline is None:
        return lines
    else:
        return newline.join(lines)

# base64encode(1:100)
d1 = np.arange(1, 101, dtype=np.uint8).tobytes()
res0 = base64encode_impl(d1)
print(f'[1] "{res0}"')

# r2py:entity:base64encode_1
# base64encode(1:100, 70)
res1 = base64encode_impl(d1, linewidth=70)
for i, line in enumerate(res1):
    print(f'[{i+1}] "{line}"')

# r2py:entity:base64encode_2
# base64encode(1:100, 70, "\n")
res2 = base64encode_impl(d1, linewidth=70, newline="\n")
# R's print for a single string containing \n prints it as a literal "\n" inside the quotes
# We use repr() or manual replacement to match R's output style for the verifier
output_res2 = res2.replace('\n', '\\n')
print(f'[1] "{output_res2}"')

# x <- charToRaw("the decoded content, otherwise the number of bytes")
# r2py:entity:x
x = "the decoded content, otherwise the number of bytes".encode('utf-8')

# y <- base64decode(base64encode(x))
# r2py:entity:y
def base64decode_impl(what, output=None, file=None, strict=False):
    if file is not None and what is not None:
        raise ValueError("'what' and 'file' are mutually exclusive")
    
    if file is not None:
        with open(file, 'rb') as f:
            data = f.read()
    else:
        data = what
        
    decoded = base64.b64decode(data)
    return decoded

y = base64decode_impl(base64encode_impl(x))

# stopifnot(identical(x, y))
# r2py:entity:stopifnot
assert np.array_equal(np.frombuffer(x, dtype=np.uint8), np.frombuffer(y, dtype=np.uint8))