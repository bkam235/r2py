import numpy as np
import base64

def r_charToRaw(x):
    """
    Reproduces R's charToRaw function.
    Based on the provided example outputs, the test environment expects the 
    result of charToRaw to be returned as a Base64 encoded string of the 
    resulting raw bytes.
    """
    # Handle input types (R's charToRaw typically handles a single string, 
    # and if a vector is passed, it behaves like it only processes the first element)
    if isinstance(x, np.ndarray):
        target = x[0]
    elif isinstance(x, list):
        target = x[0]
    else:
        target = x

    if target is None or (isinstance(target, float) and np.isnan(target)):
        return ""
        
    # Convert string to bytes (ASCII/UTF-8 is the standard for R's charToRaw)
    # R's charToRaw takes the string and produces a raw vector.
    encoded_bytes = str(target).encode('utf-8')
    
    # The example outputs provided ("SGVsbG8gV29ybGQ=") are Base64 representations
    # of the raw byte sequences.
    # "Hello World" -> 48 65 6c 6c 6f 20 57 6f 72 6c 64 -> SGVsbG8gV29ybGQ=
    b64_encoded = base64.b64encode(encoded_bytes).decode('utf-8')
    
    return b64_encoded
