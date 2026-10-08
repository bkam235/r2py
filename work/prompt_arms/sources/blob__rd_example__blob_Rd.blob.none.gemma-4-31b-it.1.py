import numpy as np

class Blob:
    def __init__(self, data):
        # R's blob can be a list of raw vectors
        self.data = data

    def __repr__(self):
        # R output format:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        n = len(self.data)
        header = f"<blob[{n}]>"
        details = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {details}"

def new_blob(x=None):
    if x is None:
        return Blob([])
    # Ensure elements are bytes
    data = [b if isinstance(b, (bytes, bytearray)) else bytes(b) for b in x]
    return Blob(data)

def blob(*args):
    # R's blob() takes multiple raw vectors
    data = [b if isinstance(b, (bytes, bytearray)) else bytes(b) for b in args]
    return Blob(data)

def as_blob(x):
    # R's as.blob converts strings or raw vectors to a blob
    if isinstance(x, (list, tuple, np.ndarray)):
        data = [i.encode('utf-8') if isinstance(i, str) else bytes(i) for i in x]
        return Blob(data)
    elif isinstance(x, str):
        return Blob([x.encode('utf-8')])
    else:
        return Blob([bytes(x)])

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