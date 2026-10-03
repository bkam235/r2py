# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class Blob:
    def __init__(self, data):
        # data is expected to be a list of byte-like objects
        self.data = data

    def __repr__(self):
        # R output: <blob[2]> \n [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self.data)}Crawler]>" # Note: R shows <blob[n]>
        # Overriding for specific format
        return f"<blob[{len(self.data)}]>\n[1] " + " ".join([f"blob[{len(b)} B]" for b in self.data])

    def __str__(self):
        return self.__repr__()

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

# r2py:entity:new_blob
def new_blob(x=None):
    if x is None:
        x = []
    return Blob(list(x))

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # The R source as.blob.default calls as_blob which uses vec_cast to new_blob
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
    elif isinstance(x, str):
        converted = [x.encode('utf-8')]
    else:
        converted = [x]
    return new_blob(converted)

# --- Main Script Execution ---

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
res_new = new_blob([x1, x2])
print(res_new)

# r2py:entity:blob
res_blob = blob(x1, x2)
print(res_blob)

# r2py:entity:as.blob
res_as = as_blob(["Good morning", "Good evening"])
print(res_as)