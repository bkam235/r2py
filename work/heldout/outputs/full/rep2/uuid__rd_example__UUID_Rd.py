import uuid
import numpy as np

# r2py:entity:u
def as_uuid(x):
    if x is None:
        return None
    if isinstance(x, uuid.UUID):
        return x
    return uuid.UUID(str(x))

# r2py:entity:uv
def uuid_generate(n=1, output="uuid"):
    # R's UUIDgenerate(n=3, output="uuid") produces 3 UUID objects
    res = [uuid.uuid4() for _ in range(n)]
    if output == "string":
        return [str(u) for u in res]
    elif output == "raw":
        return [u.bytes for u in res]
    return res

def r_print_uuid(u):
    if u is None:
        return "NA"
    return f"UUID: {u}"

def r_print_uuid_vector(uv):
    print("UUID vector:")
    for i, val in enumerate(uv, 1):
        # R represents UUIDs as strings in the vector printout
        s = str(val) if val is not None else "NA"
        print(f'[{i}] "{s}"')

def r_print_logical(vec):
    # R prints logical vectors as [1] TRUE FALSE ...
    vals = ["TRUE" if x else "FALSE" for x in vec]
    print(f"[1] {' '.join(vals)}")

# r2py:entity:as.raw
def r_print_raw(u):
    if u is None:
        print("[1] NA")
        return
    # R as.raw(u) prints hex bytes: 83 7b c8 ...
    hex_bytes = " ".join(f"{b:02x}" for b in u.bytes)
    print(f"[1] {hex_bytes}")

# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
# r2py:entity:u
u = as_uuid("837bc850-07d9-42f9-9afb-716409bf87b7")
print(r_print_uuid(u))

# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
# r2py:entity:uv
uv_gen = uuid_generate(n=3, output="uuid")
uv = [u, None] + uv_gen
r_print_uuid_vector(uv)

# as.character(u)
# r2py:entity:as.character
print(f'[1] "{str(u)}"')

# uv == u
res_eq = [ (x == u) if x is not None else False for x in uv ]
r_print_logical(res_eq)

# is.na(uv)
# r2py:entity:is.na
res_na = [ x is None for x in uv ]
r_print_logical(res_na)

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
uv_chars = [str(x) if x is not None else None for x in uv]
uv_back = [as_uuid(x) for x in uv_chars]
# identical checks for exact object/value equality including NAs
identical_res = np.array_equal([str(x) for x in uv_back], [str(x) for x in uv])
r_print_logical([identical_res])

# as.raw(u)
# r2py:entity:as.raw
r_print_raw(u)

## all forms are can be coerced losslessly
# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
uv_raw = [x.bytes if x is not None else None for x in uv]
uv_raw_back = [as_uuid(uuid.UUID(bytes=x)) if x is not None else None for x in uv_raw]
identical_res_1 = np.array_equal([str(x) for x in uv_raw_back], [str(x) for x in uv])
r_print_logical([identical_res_1])

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
uv_raw_back_chars = [str(x) if x is not None else None for x in uv_raw_back]
uv_final = [as_uuid(x) for x in uv_raw_back_chars]
identical_res_2 = np.array_equal([str(x) for x in uv_final], [str(x) for x in uv])
r_print_logical([identical_res_2])