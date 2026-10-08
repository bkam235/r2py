import numpy as np

class Blob:
    def __init__(self, data):
        # data is expected to be a list of bytes/bytearrays
        self.data = data

    def __repr__(self):
        # R prints: <blob[n]>
        # [1] blob[size1 B] blob[size2 B] ...
        n = len(self.data)
        sizes = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"<blob[{n}]>\n[1] {sizes}"

def new_blob(x):
    if isinstance(x, list):
        return Blob(x)
    raise TypeError("must be a list of raw vectors")

def blob(*args):
    # R's blob(...) can take multiple raw vectors
    return new_blob(list(args))

def as_blob(x):
    # R's as.blob converts strings to raw
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return new_blob(converted)
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# --- Main Script Execution ---

x1 = "Good morning".encode('utf-8')
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

res_new_blob = new_blob([x1, x2])
print(res_new_blob)

res_blob = blob(x1, x2)
print(res_blob)

res_as_blob = as_blob(["Good morning", "Good evening"])
print(res_as_blob)