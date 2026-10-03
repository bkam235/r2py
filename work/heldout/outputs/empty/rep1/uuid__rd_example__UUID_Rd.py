# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import uuid
import numpy as np

# R's uuid package treats NA as a specific sentinel UUID value
R_UUID_NA = "a2070000-0000-f07f-0000-000000000000"

# r2py:entity:u
class RUUID:
    def __init__(self, val):
        if isinstance(val, uuid.UUID):
            self.val = val
        elif isinstance(val, str):
            if val == R_UUID_NA or val == "NA":
                self.val = uuid.UUID(R_UUID_NA)
            else:
                self.val = uuid.UUID(val)
        elif val is None:
            self.val = uuid.UUID(R_UUID_NA)
        else:
            self.val = val

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        if isinstance(other, RUUID):
            return self.val == other.val
        if isinstance(other, uuid.UUID):
            return self.val == other
        return False

    def __hash__(self):
        return hash(self.val)

def as_uuid(x):
    if isinstance(x, list):
        return [as_uuid(i) for i in x]
    return RUUID(x)

# r2py:entity:uv
def uuid_generate(n=1, output="uuid"):
    res = [uuid.uuid4() for _ in range(n)]
    if output == "uuid":
        return [RUUID(u) for u in res]
    return res

def r_print_vector(vec, is_logical=False, label=None):
    if not vec:
        return
    if label:
        print(label)
    
    if is_logical:
        items = " ".join(["TRUE" if x else "FALSE" for x in vec])
        print(f"[1] {items}")
    elif isinstance(vec[0], RUUID):
        for i, val in enumerate(vec, 1):
            val_str = str(val.val)
            # In R, UUID vectors print quoted strings. 
            # The sentinel NA is also printed as a quoted string of the sentinel value.
            print(f"[{i}] \"{val_str}\"")
    else:
        print(f"[1] {vec}")

# suppressPackageStartupMessages(library(uuid))
# No output

# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
# r2py:entity:u
u = as_uuid("837bc850-07d9-42f9-9afb-716409bf87b7")
# R prints result of assignment (u)
print(f'UUID: {u.val}')

# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
# r2py:entity:uv
uv = [u, RUUID(None)] + uuid_generate(n=3, output="uuid")
# R prints the result of (uv <- ...)
r_print_vector(uv, label="UUID vector:")

# as.character(u)
# r2py:entity:as.character
print(f'[1] "{str(u)}"')

# uv == u
res_eq = ["TRUE" if val == u else "FALSE" for val in uv]
print(f"[1] {' '.join(res_eq)}")

# is.na(uv)
# In the uuid package, is.na returns TRUE for the sentinel NA value
# r2py:entity:is.na
res_na = ["TRUE" if (isinstance(val, RUUID) and val.val == uuid.UUID(R_UUID_NA)) else "FALSE" for val in uv]
print(f"[1] {' '.join(res_na)}")

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
uv_char_back = [as_uuid(str(x.val)) for x in uv]
print(f"[1] {'TRUE' if uv_char_back == uv else 'FALSE'}")

# as.raw(u)
# r2py:entity:as.raw
raw_u = u.val.bytes
print(f"[1] {' '.join(f'{b:02x}' for b in raw_u)}")

# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
uv_raw_back = [as_uuid(uuid.UUID(bytes=x.val.bytes)) for x in uv]
print(f"[1] {'TRUE' if uv_raw_back == uv else 'FALSE'}")

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
uv_raw_char_back = [as_uuid(str(as_uuid(uuid.UUID(bytes=x.val.bytes)).val)) for x in uv]
print(f"[1] {'TRUE' if uv_raw_char_back == uv else 'FALSE'}")