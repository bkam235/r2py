# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class Blob:
    def __init__(self, x=None):
        if x is None:
            self.data = []
        elif isinstance(x, list):
            self.data = list(x)
        else:
            self.data = [x]

    def __repr__(self):
        # R output format:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        n = len(self.data)
        header = f"<blob[{n}]>"
        elements = " ".join([f"blob[{len(item)} B]" for item in self.data])
        return f"{header}\n[1] {elements}"

def new_blob(x=None):
    return Blob(x)

# r2py:entity:blob
def is_raw(x):
    return isinstance(x, (bytes, bytearray))

def is_raw_list(x):
    if not isinstance(x, list):
        return False
    for item in x:
        if item is not None and not is_raw(item):
            return False
    return True

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("`x` must be a list of raw vectors")

def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # R's as.blob is a wrapper around as_blob (the internal helper)
    # We simulate the conversion of strings to raw bytes
    if isinstance(x, (list, np.ndarray)):
        converted = []
        for item in x:
            if isinstance(item, str):
                converted.append(item.encode('utf-8'))
            else:
                converted.append(item)
        return new_blob(converted)
    else:
        if isinstance(x, str):
            return new_blob([x.encode('utf-8')])
        return new_blob([x])

# Main script execution
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