# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class Blob:
    """Represents a blob (list of raw byte vectors) like in R."""
    def __init__(self, items):
        self.items = list(items) if items else []
    
    def __repr__(self):
        if not self.items:
            return "<blob[0]>\n"
        # Calculate sizes and format like R's blob output
        sizes = [len(item) if isinstance(item, (bytes, bytearray)) else 0 for item in self.items]
        header = f"<blob[{len(self.items)}]>\n"
        items_str = "[1] " + " ".join(f"blob[{size} B]" for size in sizes)
        return header + items_str
    
    def __str__(self):
        return repr(self)

def is_raw_list(x):
    if not isinstance(x, (list, Blob)):
        return False
    items = x.items if isinstance(x, Blob) else x
    for item in items:
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
    # Simplified implementation of as_blob
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