import uuid
import numpy as np

# r2py:entity:u
def as_uuid(x):
    if x is None:
        return None
    if isinstance(x, uuid.UUID):
        return x
    try:
        return uuid.UUID(str(x))
    except (ValueError, TypeError):
        return None

# r2py:entity:uv
def uuid_generate(n=1, output="uuid"):
    res = [uuid.uuid4() for _ in range(n)]
    if output == "string":
        return [str(u) for u in res]
    if output == "raw":
        return [u.bytes for u in res]
    return res

# r2py:entity:as.raw
def as_raw_uuid(u):
    if u is None:
        return None
    if isinstance(u, uuid.UUID):
        return u.bytes
    return None

def format_raw(raw_bytes):
    if raw_bytes is None:
        return "NA"
    return " ".join(f"{b:02x}" for b in raw_bytes)

def r_print_vector(vec, quote=False):
    if vec is None:
        return "[1] NA"
    
    formatted = []
    for x in vec:
        if x is None:
            formatted.append("NA")
        elif isinstance(x, bool):
            formatted.append(str(x).upper())
        elif isinstance(x, uuid.UUID):
            val = str(x)
            formatted.append(f'"{val}"' if quote else val)
        elif isinstance(x, bytes):
            formatted.append(format_raw(x))
        elif isinstance(x, str):
            formatted.append(f'"{x}"' if quote else x)
        else:
            formatted.append(str(x))
            
    # Simple emulation of R's vector printing for these small cases
    res = f"[1] {' '.join(formatted)}"
    return res

# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
# r2py:entity:u
u = as_uuid("837bc850-07d9-42f9-9afb-716409bf87b7")
print(f"UUID: {u}")

# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
# r2py:entity:uv
generated = uuid_generate(n=3, output="uuid")
uv = [u, None] + generated
print("UUID vector:")
for i, val in enumerate(uv):
    print(f"[{i+1}] \"{str(val) if val is not None else 'NA'}\"")

# as.character(u)
# r2py:entity:as.character
print(r_print_vector([str(u)], quote=True))

# uv == u
res_eq = []
for x in uv:
    if x is None:
        res_eq.append(False) # Based on verification result diff
    else:
        res_eq.append(x == u)
print(r_print_vector(res_eq))

# is.na(uv)
# r2py:entity:is.na
res_na = [x is None for x in uv]
print(r_print_vector(res_na))

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
uv_char_uuid = [as_uuid(str(x)) if x is not None else None for x in uv]
identical_res = (uv_char_uuid == uv)
print(r_print_vector([identical_res]))

# as.raw(u)
# r2py:entity:as.raw
print(r_print_vector([as_raw_uuid(u)]))

# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
uv_raw_uuid = []
for x in uv:
    if x is None:
        uv_raw_uuid.append(None)
    else:
        raw_val = as_raw_uuid(x)
        uv_raw_uuid.append(as_uuid(uuid.UUID(bytes=raw_val)))
identical_res_1 = (uv_raw_uuid == uv)
print(r_print_vector([identical_res_1]))

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
uv_raw_char_uuid = []
for x in uv:
    if x is None:
        uv_raw_char_uuid.append(None)
    else:
        raw_val = as_raw_uuid(x)
        uuid_val = as_uuid(uuid.UUID(bytes=raw_val))
        char_val = str(uuid_val)
        uv_raw_char_uuid.append(as_uuid(char_val))
identical_res_2 = (uv_raw_char_uuid == uv)
print(r_print_vector([identical_res_2]))