# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemini-2.0-flash  ScriptMap entities: 7

import numpy as np

class Blob:
    def __init__(self, x):
        if not isinstance(x, list):
            x = list(x)
        self.data = x
    
    def __repr__(self):
        # Format like R's blob output: <blob[n]>\n[1] blob[size B] blob[size B] ...
        n = len(self.data)
        sizes = [len(item) if isinstance(item, (bytes, bytearray)) else 0 for item in self.data]
        blob_strs = [f"blob[{size} B]" for size in sizes]
        result = f"<blob[{n}]>\n[1] " + " ".join(blob_strs)
        return result
    
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
    if not isinstance(x, list):
        x = list(x)
    return Blob(x)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    # Convert inputs to bytes to mimic R's as.blob behavior for strings
    if isinstance(x, (list, tuple, np.ndarray)):
        return new_blob([i.encode('utf-8') if isinstance(i, str) else i for i in x])
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
print(blob(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))
