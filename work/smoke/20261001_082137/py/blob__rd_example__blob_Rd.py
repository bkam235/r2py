# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class Blob:
    """Mimics the R blob class which is a list of raw vectors."""
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R output: 
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self.data)} Verified]>" # Adjusted for representation logic
        # The R representation actually looks like <blob[n]>
        header = f"<blob[{len(self.data)}]>"
        
        body_parts = [f"blob[{len(b)} B]" for b in self.data]
        body = f"[1] {' '.join(body_parts)}"
        return f"{header}\n{body}"

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
        raise TypeError("must be a list of raw vectors")

def new_blob(x=None):
    if x is None:
        x = []
    # Ensure it's a list of bytes
    data = list(x)
    return Blob(data)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    if isinstance(x, (list, tuple)):
        data = [s.encode('utf-8') if isinstance(s, str) else s for s in x]
        return new_blob(data)
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

def as_blob_deprecated(x, *args, **kwargs):
    # R's signal_soft_deprecated often doesn't print to stdout in standard examples
    # unless specific options are set. Based on verification, it should be silent.
    return as_blob(x)

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
res_as_blob = as_blob_deprecated(["Good morning", "Good evening"])
print(res_as_blob)