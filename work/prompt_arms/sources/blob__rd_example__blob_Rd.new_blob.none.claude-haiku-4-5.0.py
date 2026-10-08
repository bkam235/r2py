# Translated from <R script> by r2py v0.3.0
# blob package example

import numpy as np

class blob:
    """A blob object representing a list of raw byte vectors."""
    def __init__(self, data=None):
        if data is None:
            self.data = []
        elif isinstance(data, list):
            self.data = list(data)
        else:
            self.data = [data]
    
    def __repr__(self):
        # Format: <blob[n]>
        # [1] blob[size1 B] blob[size2 B] ...
        n = len(self.data)
        header = f"<blob[{n}]>"
        items = []
        for item in self.data:
            if isinstance(item, (bytes, bytearray)):
                size = len(item)
                items.append(f"blob[{size} B]")
            else:
                items.append(f"blob[0 B]")
        body = "[1] " + " ".join(items)
        return header + "\n" + body
    
    def __str__(self):
        return self.__repr__()

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
    return blob(x)

# r2py:entity:blob
def blob_fn(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    # Convert inputs to bytes to mimic R's as.blob behavior for strings
    if isinstance(x, (list, tuple, np.ndarray)):
        result = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return new_blob(result)
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
print(blob_fn(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))
