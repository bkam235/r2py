import numpy as np

class Blob:
    def __init__(self, data):
        # data is expected to be a list of bytes/byte-like objects
        self.data = list(data)

    def __repr__(self):
        # R prints: <blob[N]>\n[1] blob[M1 B] blob[M2 B] ...
        header = f"<blob[{len(self.data)}]>"
        details = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {details}"

# r2py:entity:new_blob
def new_blob(x):
    return Blob(x)

# r2py:entity:blob
def blob(*args):
    # R's blob() takes multiple raw vectors
    return Blob(list(args))

# r2py:entity:as.blob
def as_blob(x):
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

# R auto-prints these
# r2py:entity:new_blob
print(new_blob([x1, x2]))

# r2py:entity:blob
print(blob(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))