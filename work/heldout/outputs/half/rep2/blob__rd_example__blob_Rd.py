# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class BlobList(list):
    """
    Custom list class to mimic R's 'blob' class printing behavior.
    """
    def __repr__(self):
        header = f"<blob[{len(self)}]>"
        elements = " ".join([f"blob[{len(x)} B]" if x is not None else "NULL" for x in self])
        return f"{header}\n[1] {elements}"

def new_blob(x=None):
    if x is None:
        x = []
    # In R, new_blob creates a list of raw vectors with class "blob"
    return BlobList(x)

# r2py:entity:blob
def is_raw_list(x):
    if not isinstance(x, list):
        return False
    # R checks if all elements are either raw or NULL
    return all(isinstance(item, (bytes, bytearray)) or item is None for item in x)

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("must be a list of raw vectors")

def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    # Convert elements to bytes (similar to vec_cast)
    if isinstance(x, (list, np.ndarray)):
        items = [s.encode("utf-8") if isinstance(s, str) else bytes(s) for s in x]
    else:
        items = [x.encode("utf-8") if isinstance(x, str) else bytes(x)]
    return new_blob(items)

def as_blob_default(x, *args, **kwargs):
    return as_blob(x)

# Main script translation
# r2py:entity:x1
x1 = "Good morning".encode("utf-8")
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
print(new_blob([x1, x2]))
# r2py:entity:blob
print(blob(x1, x2))

# as.blob calls as.blob.default which calls as_blob
# r2py:entity:as.blob
print(as_blob_default(["Good morning", "Good evening"]))