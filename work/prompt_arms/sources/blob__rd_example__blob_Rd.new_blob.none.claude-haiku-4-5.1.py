# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class Blob:
    """A blob is a list of raw vectors (bytes objects)"""
    def __init__(self, data):
        if not isinstance(data, list):
            data = [data]
        self.data = data
    
    def __repr__(self):
        # Format: <blob[N]>
        # [1] blob[X B] blob[Y B] ...
        header = f"<blob[{len(self.data)}]>"
        sizes = [f"blob[{len(item) if isinstance(item, (bytes, bytearray)) else 0} B]" for item in self.data]
        body = "[1] " + " ".join(sizes)
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

def new_blob(x=None):
    """Create a new blob from a list of raw vectors"""
    if x is None:
        x = []
    if not isinstance(x, list):
        x = [x]
    return Blob(x)

def blob(*args):
    """Create a blob from raw vectors"""
    x = list(args)
    validate_blob(x)
    return new_blob(x)

def as_blob(x):
    """Convert input to blob"""
    if isinstance(x, (list, tuple, np.ndarray)):
        return new_blob([i.encode('utf-8') if isinstance(i, str) else i for i in x])
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# --- Main Script Execution ---

x1 = "Good morning".encode('utf-8')
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

print(new_blob([x1, x2]))
print(blob(x1, x2))

print(as_blob(["Good morning", "Good evening"]))
