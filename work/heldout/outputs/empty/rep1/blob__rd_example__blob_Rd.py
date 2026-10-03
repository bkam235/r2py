# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import warnings

# r2py:entity:new_blob
class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R output format:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self.data)}]> "
        elements = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {elements}"

def is_raw_list(x):
    if not isinstance(x, list):
        return False
    for item in x:
        if item is not None and not isinstance(item, (bytes, bytearray)):
            return False
    return True

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("x must be a list of raw vectors")

def new_blob(x=None):
    if x is None:
        x = []
    # new_list_of(x, ptype = raw(), class_val= "blob")
    # Convert input to bytes if it's a string (simulating vec_cast/as_blob)
    processed_x = []
    for item in x:
        if isinstance(item, str):
            processed_x.append(item.encode('utf-8'))
        elif isinstance(item, (bytes, bytearray)):
            processed_x.append(bytes(item))
        else:
            processed_x.append(item)
    return Blob(processed_x)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # R implementation: signal_soft_deprecated is called, then UseMethod("as.blob")
    # which calls as_blob(x) -> vec_cast(x, new_blob())
    if isinstance(x, (list, tuple)):
        return new_blob(x)
    else:
        # Handle single value as a vector of 1
        return new_blob([x])

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