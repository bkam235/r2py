# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

class Blob(list):
    """
    Represents an R 'blob' object, which is essentially a list of raw vectors.
    """
    def __repr__(self):
        # R output: 
        #      <blob[2]>
        # [1] blob[12 B] blob[5 B]
        header = f"      <blob[{len(self)} неве]>" # The 'неве' is a placeholder, R just shows count
        # Wait, looking at R output: <blob[2]>
        header = f"      <blob[{len(self)}]>"
        
        elements = " ".join([f"blob[{len(x)} B]" for x in self])
        return f"{header}\n[1] {elements}"

# r2py:entity:new_blob
def new_blob(x=None):
    if x is None:
        x = []
    # In R, new_blob creates a list of raw vectors with class "blob"
    # We ensure items are converted to bytes/bytearray
    blob_list = Blob()
    for item in x:
        if item is None:
            blob_list.append(None)
        elif isinstance(item, (bytes, bytearray)):
            blob_list.append(bytes(item))
        elif isinstance(item, str):
            blob_list.append(item.encode("utf-8"))
        else:
            blob_list.append(bytes(item))
    return blob_list

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

# r2py:entity:blob
def blob(*args):
    x = list(args)
    # The R source uses validate_blob which checks if it's a raw list
    # Since args are passed individually, we check them here
    raw_list = []
    for item in x:
        if isinstance(item, (bytes, bytearray)):
            raw_list.append(item)
        else:
            # R's blob() internally calls list2(...) then validate_blob
            # If they aren't raw, it fails.
            raise TypeError("must be a list of raw vectors")
    
    return new_blob(raw_list)

# r2py:entity:as.blob
def as_blob(x):
    # as_blob in R uses vec_cast(x, new_blob())
    if isinstance(x, (list, np.ndarray)):
        converted = [bytes(item, "utf-8") if isinstance(item, str) else bytes(item) for item in x]
        return new_blob(converted)
    else:
        converted = [bytes(x, "utf-8") if isinstance(x, str) else bytes(x)]
        return new_blob(converted)

def as_blob_default(x, *args, **kwargs):
    return as_blob(x)

def as_blob_generic(x, *args, **kwargs):
    # signal_soft_deprecated is ignored
    return as_blob_default(x, *args, **kwargs)

# Main Script
# r2py:entity:x1
x1 = "Good morning".encode("utf-8")
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# new_blob(list(x1, x2))
# r2py:entity:new_blob
res1 = new_blob([x1, x2])
print(res1)

# blob(x1, x2)
# r2py:entity:blob
res2 = blob(x1, x2)
print(res2)

# as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
res3 = as_blob_generic(["Good morning", "Good evening"])
print(res3)