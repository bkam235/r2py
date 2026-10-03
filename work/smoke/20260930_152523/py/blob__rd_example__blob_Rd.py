# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# suppressPackageStartupMessages(library(blob))
pass

# No direct Python equivalent for R's 'blob' package; implementing a custom class to mimic behavior.

# r2py:entity:new_blob
class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R output for blob:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self.data)} rõ]>"
        # Correcting " rõ" to simply match R's <blob[n]>
        header = f"<blob[{len(self.data)}]>"
        elements = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {elements}"

# x1 <- charToRaw("Good morning")
# r2py:entity:x1
x1 = "Good morning".encode('utf-8')

# x2 <- as.raw(c(0x48, 0x65, 0x6c, 0x6c, 0x6f))
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# new_blob(list(x1, x2))
def new_blob(x=None):
    if x is None:
        x = []
    return Blob(x)

res_new = new_blob([x1, x2])
print(res_new)

# blob(x1, x2)
# r2py:entity:blob
def blob(*args):
    return new_blob(list(args))

res_blob = blob(x1, x2)
print(res_blob)

# as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
def as_blob(x):
    # Convert input to a list of bytes
    casted = [s.encode('utf-8') if isinstance(s, str) else s for s in x]
    return new_blob(casted)

res_as = as_blob(["Good morning", "Good evening"])
print(res_as)