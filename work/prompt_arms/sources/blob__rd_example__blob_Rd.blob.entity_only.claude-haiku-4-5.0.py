# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class blob(list):
    """A simple blob class that mimics R's blob S3 class."""
    
    def __repr__(self):
        # Format: <blob[n]> on first line, then [1] blob[X B] blob[Y B] ...
        n = len(self)
        first_line = f"<blob[{n}]>"
        if n == 0:
            return first_line
        # Second line shows individual blob sizes
        blob_strs = []
        for item in self:
            if isinstance(item, (bytes, bytearray)):
                blob_strs.append(f"blob[{len(item)} B]")
            else:
                blob_strs.append(f"blob[? B]")
        items_line = "[1] " + " ".join(blob_strs)
        return first_line + "\n" + items_line

def is_raw_list(x):
    if not isinstance(x, list):
        return False
    for item in x:
        if item is not None and not isinstance(item, (bytes, bytearray)):
            return False
    return True

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("must be a list of raw vectors")

# r2py:entity:new_blob
def new_blob(x=None):
    if x is None:
        x = []
    # Create a blob instance (which is a list subclass)
    result = blob(x)
    return result

# r2py:entity:blob - use verified translation
def blob_func(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    # Convert inputs to bytes to mimic R's as.blob behavior for strings
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return new_blob(converted)
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# --- Main Script Execution ---

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
print(new_blob([x1, x2]))
# r2py:entity:blob
print(blob_func(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))
