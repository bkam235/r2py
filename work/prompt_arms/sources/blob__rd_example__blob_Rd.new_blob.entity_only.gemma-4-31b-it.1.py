import numpy as np

class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        header = f"<blob[{len(self.data)}]>"
        elements = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {elements}"

def new_blob(x=None):
    if x is None:
        x = []
    if not isinstance(x, list):
        x = list(x)
    return Blob(x)

def blob(*args):
    return new_blob(list(args))

def as_blob(x):
    if isinstance(x, (list, tuple, np.ndarray)):
        items = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return new_blob(items)
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# R auto-prints these expressions
# r2py:entity:new_blob
print(new_blob([x1, x2]))
# r2py:entity:blob
print(blob(x1, x2))
# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))