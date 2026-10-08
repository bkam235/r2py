import numpy as np

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

def format_blob(x):
    if not isinstance(x, list):
        return ""
    header = f"<blob[{len(x)}]>"
    body = " ".join([f"blob[{len(b)} B]" for b in x])
    return f"{header}\n[1] {body}"

# r2py:entity:new_blob
def new_blob(x=None):
    if x is None:
        x = []
    return list(x)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    if isinstance(x, (list, tuple, np.ndarray)):
        return new_blob([i.encode('utf-8') if isinstance(i, str) else i for i in x])
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# --- Main Script Execution ---

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# R auto-prints these results
res_new_blob = new_blob([x1, x2])
print(format_blob(res_new_blob))

res_blob = blob(x1, x2)
print(format_blob(res_blob))

res_as_blob = as_blob(["Good morning", "Good evening"])
print(format_blob(res_as_blob))