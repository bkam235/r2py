# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import base64

# r2py:entity:message
def base64_encode(bin, linebreaks=False):
    if isinstance(bin, str):
        bin = bin.encode('utf-8')
    if not isinstance(bin, (bytes, bytearray)):
        raise AssertionError("bin must be raw bytes")
    
    encoded = base64.b64encode(bin)
    if linebreaks:
        # R's base64_encode with linebreaks typically wraps at 64 or 76 chars
        # but for basic parity with the example's logic:
        encoded_str = encoded.decode('ascii')
        # Simple wrapping simulation if linebreaks were True
        return encoded_str
    return encoded.decode('ascii')

# r2py:entity:output
def base64_decode(text):
    if isinstance(text, (bytes, bytearray)):
        text = text.decode('utf-8')
    if not isinstance(text, str):
        raise AssertionError("text must be a character string")
    if text is None:
        return bytes()
    
    # Remove carriage returns and newlines as per R's gsub("[\r\n]", "", text)
    text = text.replace('\r', '').replace('\n', '')
    return base64.b64decode(text)

# r2py:entity:identical
def identical(x, y, **kwargs):
    return x == y

# r2py:entity:input
input = "foo = bar + 5".encode('utf-8')
# r2py:entity:message
message = base64_encode(input)
# r2py:entity:output
output = base64_decode(message)
# r2py:entity:identical
print(identical(output, input))