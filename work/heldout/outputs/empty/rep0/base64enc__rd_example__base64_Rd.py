# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import base64
import numpy as np

# r2py:entity:base64encode
def base64encode(what, linewidth=0, newline=None):
    # Handle linewidth logic matching R source
    if linewidth is None:
        linewidth = 0
    
    if linewidth > 0 and linewidth < 4:
        linewidth = 4
    
    # Convert input to bytes (as.raw in R)
    if isinstance(what, str):
        # In R, base64encode treats strings as filenames if they are characters
        # unless they are raw. But based on the source, if is.character(what),
        # it opens a file. However, for raw data inputs passed as strings in 
        # some contexts, we handle it.
        # Based on R source: if (is.character(what)) { what <- file(what, "rb") ... }
        # For the example 'x', x is already raw (charToRaw).
        # Here we handle basic types.
        data = what.encode('utf-8')
    elif isinstance(what, (list, np.ndarray)):
        data = bytes([int(x) % 256 for x in what])
    elif isinstance(what, bytes):
        data = what
    else:
        data = bytes(what)

    encoded = base64.b64encode(data).decode('ascii')
    
    if linewidth <= 0:
        return encoded
    
    # R's base64encode ensures linewidth is a multiple of 4
    actual_linewidth = linewidth - (linewidth % 4)
    
    # Split string into chunks of linewidth
    chunks = [encoded[i:i + actual_linewidth] for i in range(0, len(encoded), actual_linewidth)]
    
    if newline is None:
        # If linewidth > 0 and newline is NULL, R returns a vector of strings
        return chunks
    else:
        # If newline is provided, R joins them into a single string with the newline
        return newline.join(chunks)

# r2py:entity:y
def base64decode(what, output=None, file=None, strict=False):
    if file is not None and what is not None:
        raise ValueError("'what' and 'file' are mutually exclusive")
    
    if file is not None:
        with open(file, 'r') as f:
            data = f.read()
    else:
        data = what

    decoded = base64.b64decode(data, validate=strict)
    
    if isinstance(output, str):
        with open(output, 'wb') as f:
            f.write(decoded)
        return len(decoded)
    elif output is not None:
        output.write(decoded)
        return len(decoded)
    
    return decoded

# r2py:entity:stopifnot
def stopifnot(*args):
    for arg in args:
        if not arg:
            raise AssertionError("Condition not met")

def r_print(x):
    """Helper to mimic R's printing of vectors/strings, including escaping newlines."""
    if isinstance(x, list):
        res = ""
        for i, val in enumerate(x):
            # R represents newlines as \n in quoted output
            escaped_val = val.replace('\n', '\\n') if isinstance(val, str) else val
            res += f'[{i+1}] "{escaped_val}"\n'
        return res.strip()
    elif isinstance(x, str):
        escaped_val = x.replace('\n', '\\n')
        return f'[1] "{escaped_val}"'
    else:
        return str(x)

# --- Main Script Translation ---

# base64encode(1:100)
# r2py:entity:base64encode
print(r_print(base64encode(np.arange(1, 101))))

# base64encode(1:100, 70)
# r2py:entity:base64encode_1
print(r_print(base64encode(np.arange(1, 101), 70)))

# base64encode(1:100, 70, "\n")
# r2py:entity:base64encode_2
print(r_print(base64encode(np.arange(1, 101), 70, "\n")))

# x <- charToRaw("the decoded content, otherwise the number of bytes")
# r2py:entity:x
x = "the decoded content, otherwise the number of bytes".encode('utf-8')

# y <- base64decode(base64encode(x))
# Note: base64encode(x) returns a string here because linewidth=0
# r2py:entity:y
y = base64decode(base64encode(x))

# stopifnot(identical(x, y))
# r2py:entity:stopifnot
stopifnot(x == y)