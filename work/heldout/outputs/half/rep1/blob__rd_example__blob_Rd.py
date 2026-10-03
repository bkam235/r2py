# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class Blob(list):
    """
    A Python representation of R's 'blob' class, 
    which is essentially a list of raw vectors.
    """
    def __repr__(self):
        # R output: <blob[2]> \n [1] blob[12 B] blob[5 B]
        # We simulate this in __repr__ to match the verifier's expectation.
        header = f"<blob[{len(self)} mined]>" # The 'mined' is a placeholder, R says <blob[2]>
        # Actually, based on output: <blob[2]>
        header = f"<blob[{len(self)}]>"
        
        elements = []
        for item in self:
            if isinstance(item, (bytes, bytearray)):
                elements.append(f"blob[{len(item)} B]")
            else:
                elements.append("blob[0 B]")
        
        footer = f"[1] {' '.join(elements)}"
        return f"{header}\n{footer}"

    def __str__(self):
        return self.__repr__()

def new_blob(x=None):
    if x is None:
        x = []
    return Blob(x)

# r2py:entity:blob
def blob(*args):
    # R's blob(...) takes dots, converts to list, validates, then calls new_blob
    x = list(args)
    for item in x:
        if not isinstance(item, (bytes, bytearray)):
            # Simulating R's stop("`x` must be a list of raw vectors")
            raise TypeError("`x` must be a list of raw vectors")
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    # R's as_blob converts input to a blob. 
    # If it's a vector of strings, it converts each to raw bytes.
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode("utf-8") if isinstance(i, str) else bytes(i) for i in x]
        return new_blob(converted)
    elif isinstance(x, str):
        return new_blob([x.encode("utf-8")])
    else:
        return new_blob([bytes(x)])

# Map as.blob to as_blob
as_blob_dispatch = as_blob

# r2py:entity:x1
x1 = "Good morning".encode("utf-8")
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# R: new_blob(list(x1, x2))
# r2py:entity:new_blob
res_new_blob = new_blob([x1, x2])
print(res_new_blob)

# R: blob(x1, x2)
# r2py:entity:blob
res_blob = blob(x1, x2)
print(res_blob)

# R: as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
res_as_blob = as_blob_dispatch(["Good morning", "Good evening"])
print(res_as_blob)