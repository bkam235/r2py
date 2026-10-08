import numpy as np

class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R prints: <blob[N]>
        # [1] blob[X B] blob[Y B]
        n = len(self.data)
        header = f"<blob[{n}]>"
        details = " ".join([f"blob[{len(b)} B]" for b in self.data])
        return f"{header}\n[1] {details}"

def new_blob(x):
    # Expects a list of raw-like objects
    return Blob(x)

def blob(*args):
    # Variadic input of raw-like objects
    return Blob(list(args))

def as_blob(x):
    # Convert strings or lists of strings to bytes
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return Blob(converted)
    elif isinstance(x, str):
        return Blob([x.encode('utf-8')])
    else:
        return Blob([x])

# --- Main Script Execution ---

# x1 <- charToRaw("Good morning")
x1 = "Good morning".encode('utf-8')
# x2 <- as.raw(c(0x48, 0x65, 0x6c, 0x6c, 0x6f))
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# new_blob(list(x1, x2))
res_new_blob = new_blob([x1, x2])
print(res_new_blob)

# blob(x1, x2)
res_blob = blob(x1, x2)
print(res_blob)

# as.blob(c("Good morning", "Good evening"))
res_as_blob = as_blob(["Good morning", "Good evening"])
print(res_as_blob)