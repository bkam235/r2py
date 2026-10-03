# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import base64
import numpy as np

# r2py:entity:message
def base64_encode(bin_val, linebreaks=False):
    if isinstance(bin_val, str):
        bin_val = bin_val.encode('utf-8')
    if not isinstance(bin_val, (bytes, bytearray)):
        raise TypeError("bin must be raw bytes")
    
    encoded = base64.b64encode(bin_val).decode('utf-8')
    if linebreaks:
        # R's base64_encode with linebreaks typically inserts them every 76 chars
        # but for the basic logic:
        return encoded # Simplified for standard Python base64
    return encoded

# r2py:entity:output
def base64_decode(text):
    if isinstance(text, (bytes, bytearray)):
        text = text.decode('utf-8')
    if not isinstance(text, str):
        raise TypeError("text must be a character string")
    if text is None:
        return bytes()
    
    text = text.replace('\r', '').replace('\n', '')
    return base64.b64decode(text)

# r2py:entity:identical
def identical(x, y, num_eq=True, single_na=True, attrib_as_set=True, 
               ignore_bytecode=True, ignore_environment=False, 
               ignore_srcref=True, extptr_as_ref=False):
    return np.array_equal(x, y)

# r2py:entity:input
input = "foo = bar + 5".encode('utf-8')
# r2py:entity:message
message = base64_encode(input)
# r2py:entity:output
output = base64_decode(message)
# r2py:entity:identical
result = identical(output, input)
print(result)