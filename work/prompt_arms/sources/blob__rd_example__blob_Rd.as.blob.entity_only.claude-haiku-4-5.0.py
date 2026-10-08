# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class Blob:
    """A blob object representing a list of raw (bytes) vectors."""
    def __init__(self, data):
        if not isinstance(data, list):
            data = [data]
        self.data = data
    
    def __repr__(self):
        """Format blob for printing like R does."""
        n = len(self.data)
        header = f"<blob[{n}]>"
        items = []
        for item in self.data:
            if isinstance(item, (bytes, bytearray)):
                size = len(item)
                items.append(f"blob[{size} B]")
            else:
                items.append(f"blob[? B]")
        items_str = " ".join(items)
        return f"{header}\n[1] {items_str}"
    
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
    return Blob(x)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
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
res_new_blob = new_blob([x1, x2])
print(res_new_blob)
# r2py:entity:blob
res_blob = blob(x1, x2)
print(res_blob)

# r2py:entity:as.blob
res_as_blob = as_blob(["Good morning", "Good evening"])
print(res_as_blob)