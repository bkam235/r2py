import numpy as np

class Blob:
    def __init__(self, data):
        # Data should be a list of byte-like objects
        self.data = data

    def __repr__(self):
        # Mimic R's print output: 
        # <blob[N]>
        # [1] blob[X B] blob[Y B]
        n = len(self.data)
        header = f"<blob[{n}]>"
        elements = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {elements}"

def new_blob(x):
    # x is expected to be a list of raw vectors
    return Blob(x)

def blob(*args):
    # blob() takes multiple raw vectors as arguments
    return Blob(list(args))

def as_blob(x):
    # Convert strings/lists to bytes
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return Blob(converted)
    elif isinstance(x, str):
        return Blob([x.encode('utf-8')])
    else:
        return Blob([x])

# --- Main Script Execution ---

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
print(repr(new_blob([x1, x2])))

# r2py:entity:blob
print(repr(blob(x1, x2)))

# r2py:entity:as.blob
print(repr(as_blob(["Good morning", "Good evening"])))