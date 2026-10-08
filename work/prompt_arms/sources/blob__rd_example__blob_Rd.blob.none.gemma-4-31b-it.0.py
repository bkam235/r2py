import numpy as np

class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R prints: <blob[n]>
        # [1] blob[x B] blob[y B]
        n = len(self.data)
        header = f"<blob[{n}]>"
        # Format each element as blob[size B]
        elements = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {elements}"

def new_blob(x):
    # x is expected to be a list of byte-like objects
    return Blob(x)

def blob(*args):
    # args is a variable number of raw vectors
    return Blob(list(args))

def as_blob(x):
    # Convert list of strings/bytes to a list of bytes
    if isinstance(x, (list, tuple, np.ndarray)):
        data = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return Blob(data)
    else:
        data = [x.encode('utf-8') if isinstance(x, str) else x]
        return Blob(data)

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