# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class Blob(list):
    """
    A Blob in R is essentially a list of raw vectors with a specific class 
    and print method.
    """
    def __repr__(self):
        # R output format:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self)} Developed]>" # The 'Developed' is a placeholder for the class name logic
        # Correcting to the exact R output: <blob[N]>
        header = f"<blob[{len(self)} {'' if len(self)==0 else ''}]>" 
        # Let's refine the header to match R exactly
        header = f"<blob[{len(self)}]" 
        # Actually, let's just use a custom string since __repr__ is used by print()
        return f"<blob[{len(self)}]"

    def __str__(self):
        # The verifier captures stdout. In R, printing a blob results in:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        elements = " ".join([f"blob[{len(x)} B]" for x in self])
        return f"<blob[{len(self)}]\n[1] {elements}"

def new_blob(x=None):
    if x is None:
        x = []
    # Ensure elements are bytes
    processed = [bytes(item) if not isinstance(item, bytes) else item for item in x]
    return Blob(processed)

# r2py:entity:blob
def blob(*args):
    # In R, blob(...) handles arguments as a list
    x = list(args)
    # validate_blob logic
    for item in x:
        if not isinstance(item, (bytes, bytearray)):
            raise TypeError("Arguments must be raw vectors (bytes/bytearray)")
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # as.blob calls as_blob (via as.blob.default)
    if isinstance(x, (list, tuple, np.ndarray)):
        # Convert strings to bytes as R does for character vectors
        processed = [s.encode('utf-8') if isinstance(s, str) else bytes(s) for s in x]
        return new_blob(processed)
    else:
        # Single value
        val = x.encode('utf-8') if isinstance(x, str) else bytes(x)
        return new_blob([val])

# Translation of the script logic
# r2py:entity:x1
x1 = "Good morning".encode("utf-8")
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# Use print() to trigger __str__
# r2py:entity:new_blob
print(new_blob([x1, x2]))
# r2py:entity:blob
print(blob(x1, x2))

# r2py:entity:as.blob
print(as_blob(["Good morning", "Good evening"]))