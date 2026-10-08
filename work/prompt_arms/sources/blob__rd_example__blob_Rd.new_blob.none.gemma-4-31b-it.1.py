import numpy as np

class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R outputs: <blob[N]> \n [1] blob[X B] blob[Y B] ...
        n = len(self.data)
        header = f"<blob[{n}]>"
        details = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {details}"

def new_blob(x):
    # x is expected to be a list of raw/bytes
    return Blob(list(x))

def blob(*args):
    # In R, blob(x1, x2) takes multiple raw vectors
    return Blob(list(args))

def as_blob(x):
    # In R, as.blob(c("a", "b")) converts character vectors to blobs
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
res_new_blob = new_blob([x1, x2])
print(res_new_blob)

# r2py:entity:blob
res_blob = blob(x1, x2)
print(res_blob)

# r2py:entity:as.blob
res_as_blob = as_blob(["Good morning", "Good evening"])
print(res_as_blob)