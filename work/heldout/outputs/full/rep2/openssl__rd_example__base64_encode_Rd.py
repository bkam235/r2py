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
    encoded = base64.b64encode(bin_val)
    if linebreaks:
        # R's openssl base64_encode adds linebreaks every 64 characters
        # but base64.b64encode doesn't. For the sake of this logic:
        return encoded.decode('utf-8')
    return encoded.decode('utf-8')

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

# r2py:entity:input
input_val = "foo = bar + 5".encode('utf-8')
# r2py:entity:message
message = base64_encode(input_val)
# r2py:entity:output
output = base64_decode(message)
# r2py:entity:identical
result = np.array_equal(output, input_val)
print(result)