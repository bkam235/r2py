import numpy as np

class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        n = len(self.data)
        header = f"<blob[{n}]>"
        # R output for blob: [1] blob[12 B] blob[5 B]
        blobs_str = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {blobs_str}"

def new_blob(x=None):
    if x is None:
        x = []
    if not isinstance(x, list):
        x = list(x)
    return Blob(x)

def blob(*args):
    # R's blob() accepts multiple arguments and treats them as a list
    return new_blob(list(args))

def as_blob(x):
    # R's as.blob converts a vector of strings to a blob of raw vectors
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