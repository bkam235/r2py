# Translated from <R script> by r2py v0.3.0

import numpy as np

class Blob:
    """Represents an R blob object - a list of raw byte vectors"""
    def __init__(self, x=None):
        if x is None:
            self.data = []
        elif isinstance(x, list):
            self.data = x
        else:
            self.data = list(x)
    
    def __repr__(self):
        # Format: <blob[n]>
        # [1] blob[12 B] blob[5 B] ...
        n = len(self.data)
        header = f"<blob[{n}]>"
        
        if n == 0:
            return header
        
        # Format each blob element with its size
        items = []
        for item in self.data:
            if isinstance(item, (bytes, bytearray)):
                size = len(item)
                items.append(f"blob[{size} B]")
            else:
                items.append(f"blob[0 B]")
        
        # Join items with proper indexing
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

def new_blob(x=None):
    if x is None:
        x = []
    # Convert to list if it's a tuple or similar
    if not isinstance(x, list):
        x = list(x)
    return Blob(x)

def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

def as_blob(x):
    # Convert inputs to bytes to mimic R's as.blob behavior for strings
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
