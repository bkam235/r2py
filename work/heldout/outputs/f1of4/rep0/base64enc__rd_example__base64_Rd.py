import base64
import numpy as np

# r2py:entity:base64encode
def base64encode(what, linewidth=0, newline=None):
    # Convert input to bytes
    if isinstance(what, str):
        # If it's a string, R treats it as a filename to be read in 'rb' mode
        with open(what, 'rb') as f:
            data = f.read()
    elif hasattr(what, 'read'): # Connection-like
        data = what.read()
    else:
        # Treat as raw vector (numeric sequence in R)
        data = bytes([int(x) for x in what])

    # Perform base64 encoding
    encoded_bytes = base64.b64encode(data)
    encoded_str = encoded_bytes.decode('ascii')

    if linewidth <= 0:
        return encoded_str

    # R's base64encode logic: linewidth must be multiple of 4
    if linewidth < 4:
        linewidth = 4
    
    if linewidth % 4 != 0:
        linewidth = linewidth - (linewidth % 4)
    
    # Split the string into chunks of 'linewidth'
    chunks = [encoded_str[i:i + linewidth] for i in range(0, len(encoded_str), linewidth)]
    
    if newline is None:
        # When newline is NULL and linewidth > 0, R returns a character vector (list in Py)
        return chunks
    else:
        # When newline is provided, R returns a single string with the separator
        return newline.join(chunks)

# r2py:entity:y
def base64decode(what, output=None, file=None, strict=False):
    if file is not None and what is not None:
        raise ValueError("'what' and 'file' are mutually exclusive")
    
    if file is not None:
        with open(file, 'r') as f:
            input_data = f.read()
    elif hasattr(what, 'read'):
        input_data = what.read()
    else:
        input_data = what

    decoded_data = base64.b64decode(input_data)

    if isinstance(output, str):
        with open(output, 'wb') as f:
            f.write(decoded_data)
        return len(decoded_data)
    elif hasattr(output, 'write'):
        output.write(decoded_data)
        return len(decoded_data)
    else:
        return decoded_data

# r2py:entity:stopifnot
def identical(x, y):
    if isinstance(x, bytes) and isinstance(y, bytes):
        return x == y
    return np.array_equal(x, y)

def stopifnot(*args):
    for arg in args:
        if not arg:
            raise AssertionError("Condition not met")

def r_print(val):
    """Helper to mimic R's character vector printing. 
    R prints strings with quotes and escapes special characters like \n.
    """
    if isinstance(val, list):
        res = ""
        for i, item in enumerate(val):
            res += f' [{i+1}] "{repr(item)[1:-1]}"\n'
        return res.strip()
    elif isinstance(val, str):
        # repr(val)[1:-1] removes the outer quotes of Python's repr and keeps internal escapes
        return f'[1] "{repr(val)[1:-1]}"'
    return str(val)

# Main execution
# r2py:entity:base64encode
print(r_print(base64encode(list(range(1, 101)))))
# r2py:entity:base64encode_1
print(r_print(base64encode(list(range(1, 101)), 70)))
# r2py:entity:base64encode_2
print(r_print(base64encode(list(range(1, 101)), 70, "\n")))

# r2py:entity:x
x = "the decoded content, otherwise the number of bytes".encode('utf-8')
# r2py:entity:y
y = base64decode(base64encode(x))
# r2py:entity:stopifnot
stopifnot(identical(x, y))