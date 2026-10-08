import numpy as np

class Blob:
    """A blob object mimicking R's blob class"""
    def __init__(self, data):
        if not isinstance(data, list):
            data = list(data)
        self.data = data
        # Validate that all items are bytes-like
        for item in self.data:
            if item is not None and not isinstance(item, (bytes, bytearray)):
                raise TypeError("must be a list of raw vectors")
    
    def __repr__(self):
        # R prints: <blob[2]>
        # [1] blob[12 B] blob[5 B]
        lines = [f"<blob[{len(self.data)}]>"]
        
        # Calculate sizes
        sizes = [f"blob[{len(item) if item else 0} B]" for item in self.data]
        
        # Format like R's default print: [1] item1 item2 item3 ...
        if sizes:
            lines.append("[1] " + " ".join(sizes))
        
        return "\n".join(lines)

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

def new_blob(x=None):
    if x is None:
        x = []
    return Blob(x)

def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

def as_blob(x):
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = [i.encode('utf-8') if isinstance(i, str) else i for i in x]
        return new_blob(converted)
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

x1 = "Good morning".encode('utf-8')
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

print(new_blob([x1, x2]))
print(blob(x1, x2))
print(as_blob(["Good morning", "Good evening"]))
