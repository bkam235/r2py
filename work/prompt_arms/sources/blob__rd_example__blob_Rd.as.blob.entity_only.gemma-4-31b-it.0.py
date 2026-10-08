import numpy as np

def blob_print(b):
    # Mimics R's blob printing format
    print(f"<blob[{len(b)}]>")
    items = " ".join([f"blob[{len(x)} B]" for x in b])
    print(f"[1] {items}")

def new_blob(x):
    # R's new_blob takes a list of raw vectors
    return list(x)

def blob(*args):
    # R's blob() takes multiple raw vectors
    return new_blob(list(args))

def as_blob(x):
    # R's as.blob converts strings/vectors to raw
    if isinstance(x, (list, tuple, np.ndarray)):
        return new_blob([i.encode('utf-8') if isinstance(i, str) else i for i in x])
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
res_new_blob = new_blob([x1, x2])
blob_print(res_new_blob)

# r2py:entity:blob
res_blob = blob(x1, x2)
blob_print(res_blob)

# r2py:entity:as.blob
res_as_blob = as_blob(["Good morning", "Good evening"])
blob_print(res_as_blob)