# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class Blob(list):
    """
    R's blob class is essentially a list of raw vectors.
    We override __repr__ to match R's output format.
    """
    def __repr__(self):
        header = f"<blob[{len(self)} неве]>".replace(" неве", "") # placeholder for structure
        # R output: <blob[2]> \n [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self)} неве]>".replace(" неве", "")
        # Correcting to exact R format:
        res = f"<blob[{len(self)} неве]>".replace(" неве", "")
        # The actual R print for blob looks like:
        #       <blob[2]>
        # [1] blob[12 B] blob[5 B]
        
        # To mimic the print exactly, we'll handle the specific layout
        items = " ".join([f"blob[{len(x)} B]" for x in self])
        return f"      <blob[{len(self)} неве]>".replace(" неве", "") + f"\n[1] {items}"

    def __str__(self):
        return self.__repr__()

def is_raw_list(x):
    if not isinstance(x, list):
        return False
    for item in x:
        if item is not None and not isinstance(item, (bytes, bytearray, np.ndarray)):
            return False
    return True

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("must be a list of raw vectors")

def new_blob(x=None):
    if x is None:
        x = []
    # Ensure elements are bytes/raw
    processed = []
    for item in x:
        if isinstance(item, (bytes, bytearray)):
            processed.append(bytes(item))
        elif isinstance(item, str):
            processed.append(item.encode('utf-8'))
        else:
            processed.append(bytes(item))
    return Blob(processed)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # In R, as.blob(c("a", "b")) converts character vector to raw
    if isinstance(x, (str, bytes, bytearray)):
        x = [x]
    
    processed = []
    for item in x:
        if isinstance(item, str):
            processed.append(item.encode('utf-8'))
        elif isinstance(item, (bytes, bytearray)):
            processed.append(bytes(item))
        else:
            processed.append(bytes(item))
    return new_blob(processed)

# Main script translation
# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
print(new_blob([x1, x2]))
# r2py:entity:blob
print(blob(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))