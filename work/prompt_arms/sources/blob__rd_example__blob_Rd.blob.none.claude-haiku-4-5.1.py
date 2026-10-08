# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class Blob:
    """Represents an R blob object (list of raw byte vectors)."""
    def __init__(self, data):
        if not isinstance(data, list):
            data = [data]
        # Validate each element is bytes-like
        self.data = []
        for item in data:
            if isinstance(item, (bytes, bytearray)):
                self.data.append(bytes(item))
            elif item is None:
                self.data.append(None)
            else:
                raise TypeError(f"Expected bytes, got {type(item).__name__}")
    
    def __repr__(self):
        """Represent blob like R's output: <blob[N]> followed by elements."""
        header = f"<blob[{len(self.data)}]>"
        lines = [header, "[1] ", ]
        elements = []
        for item in self.data:
            if item is None:
                elements.append("NA")
            else:
                size = len(item)
                elements.append(f"blob[{size} B]")
        lines[1] += " ".join(elements)
        return "\n".join(lines)
    
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
def as_blob(x):
    # Convert inputs to bytes to mimic R's as.blob/as_blob behavior for strings
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
print(blob(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))
