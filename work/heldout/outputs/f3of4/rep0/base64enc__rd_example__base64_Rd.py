# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import base64
import numpy as np

# r2py:entity:base64encode
def base64encode(what, linewidth=0, newline=None):
    # Convert input to bytes (equivalent to as.raw in R)
    if isinstance(what, (list, np.ndarray, range)):
        data = np.array(what, dtype=np.uint8).tobytes()
    elif isinstance(what, str):
        data = what.encode('utf-8')
    elif isinstance(what, bytes):
        data = what
    else:
        data = bytes(what)
    
    # R's base64encode uses a specific wrapping logic
    if linewidth == 0:
        return base64.b64encode(data).decode('ascii')
    
    # R adjusts linewidth to be a multiple of 4
    actual_linewidth = linewidth - (linewidth % 4)
    if actual_linewidth < 4:
        actual_linewidth = 4
        
    encoded = base64.b64encode(data).decode('ascii')
    
    # Wrap the string
    lines = [encoded[i:i+actual_linewidth] for i in range(0, len(encoded), actual_linewidth)]
    
    if newline is None:
        # R's base64encode(x, linewidth) without newline returns a vector of lines
        return lines
    else:
        # R's base64encode(x, linewidth, newline) returns a single string
        return newline.join(lines)

# r2py:entity:y
def base64decode(what, output=None, file=None, strict=False):
    if file is not None and what is not None:
        raise ValueError("'what' and 'file' are mutually exclusive")
    
    if file is not None:
        with open(file, 'r') as f:
            what = f.read()
            
    # Handle case where 'what' might be a list (from base64encode)
    if isinstance(what, list):
        what = "".join(what)
            
    # Decode the base64 string to bytes
    decoded = base64.b64decode(what, validate=strict)
    
    if isinstance(output, str):
        with open(output, 'wb') as f:
            f.write(decoded)
        return len(decoded)
    
    return decoded

# r2py:entity:x
def charToRaw(s):
    return s.encode('utf-8')

def r_print(x):
    """Helper to mimic R's print output for vectors and strings"""
    if isinstance(x, list):
        # R prints vectors as [1] "val1" \n [2] "val2"
        res = []
        for i, val in enumerate(x, 1):
            res.append(f'[{i}] "{val}"')
        return "\n".join(res)
    elif isinstance(x, str):
        # R escapes newlines in printed strings: \n becomes literal \n
        escaped = x.replace('\n', '\\n')
        return f'[1] "{escaped}"'
    return str(x)

# Main execution
# r2py:entity:base64encode
print(r_print(base64encode(list(range(1, 101)))))
# r2py:entity:base64encode_1
print(r_print(base64encode(list(range(1, 101)), 70)))
# r2py:entity:base64encode_2
print(r_print(base64encode(list(range(1, 101)), 70, "\n")))

# r2py:entity:x
x = charToRaw("the decoded content, otherwise the number of bytes")
# r2py:entity:y
y = base64decode(base64encode(x))
# r2py:entity:stopifnot
assert np.array_equal(np.frombuffer(x, dtype=np.uint8), np.frombuffer(y, dtype=np.uint8))