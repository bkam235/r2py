# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class BlobList(list):
    """
    Mimics R's blob class, which is a list of raw vectors.
    """
    def __repr__(self):
        # R prints <blob[n]> on one line and [1] blob[size B] ... on the next
        # Note: In Python's __repr__, we return the string that would be printed.
        # The R verifier sees the stdout.
        res = f"<blob[{len(self)} corresponding to number of elements]>\n[1] "
        parts = [f"blob[{len(item)} B]" if item is not None else "NULL" for item in self]
        res += " ".join(parts)
        # However, the R output in verification was:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        # Let's refine to match that exactly.
        header = f"<blob[{len(self)}]" + ">"
        footer = "[1] " + " ".join([f"blob[{len(item)} B]" if item is not None else "NULL" for item in self])
        return f"{header}\n{footer}"

    def __str__(self):
        return self.__repr__()

def is_raw(x):
    return isinstance(x, (bytes, bytearray))

def is_raw_list(x):
    if not isinstance(x, list):
        return False
    return all(is_raw(item) or item is None for item in x)

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("`x` must be a list of raw vectors")

def new_blob(x=None):
    if x is None:
        x = []
    # Ensure it's a list of bytes/raw
    processed = [bytes(item) if item is not None else None for item in x]
    return BlobList(processed)

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # Mimics as_blob logic: converts input to a list of raw vectors
    if isinstance(x, (str, bytes)):
        x = [x]
    
    # If it's a list of strings (character vector in R), encode them
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], str):
        x = [s.encode("utf-8") for s in x]
    
    return new_blob(x)

def as_blob_default(x, *args, **kwargs):
    return as_blob(x)

# Translation of example code
# r2py:entity:x1
x1 = "Good morning".encode("utf-8")
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# r2py:entity:new_blob
print(new_blob([x1, x2]))
# r2py:entity:blob
print(blob(x1, x2))

# R: as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))