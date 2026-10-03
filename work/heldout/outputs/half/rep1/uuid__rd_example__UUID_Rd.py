import uuid
import numpy as np

# suppressPackageStartupMessages(library(uuid))
# No-op in Python

# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
# r2py:entity:u
u = uuid.UUID("837bc850-07d9-42f9-9afb-716409bf87b7")
print(f"UUID: {u}")

# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
# UUIDgenerate(n=3, output="uuid") generates 3 random UUIDs
# r2py:entity:uv
uv = [
    u, 
    None, 
    uuid.uuid4(), 
    uuid.uuid4(), 
    uuid.uuid4()
]
print("UUID vector:")
for i, val in enumerate(uv, 1):
    print(f'[{i}] "{val if val is not None else "NA"}"')

# as.character(u)
# r2py:entity:as.character
print(f'[1] "{str(u)}"')

# uv == u
# R comparison of a vector against a scalar returns a boolean vector
res_eq = [x == u if x is not None else False for x in uv]
print(f'[1] {" ".join(map(lambda x: str(x).upper(), map(str, res_eq)))}')

# is.na(uv)
# r2py:entity:is.na
res_na = [x is None for x in uv]
print(f'[1] {" ".join(map(lambda x: str(x).upper(), map(str, res_na)))}')

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
uv_char = [str(x) if x is not None else None for x in uv]
uv_reconstructed = [uuid.UUID(x) if x is not None else None for x in uv_char]
result_identical = all((a == b) for a, b in zip(uv_reconstructed, uv))
print(f'[1] {str(result_identical).upper()}')

# as.raw(u)
# r2py:entity:as.raw
raw_bytes = u.bytes
print(f'[1] {" ".join(f"{b:02x}" for b in raw_bytes)}')

# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
uv_raw = [x.bytes if x is not None else None for x in uv]
uv_raw_reconstructed = [uuid.UUID(bytes=x) if x is not None else None for x in uv_raw]
result_identical_1 = all((a == b) for a, b in zip(uv_raw_reconstructed, uv))
print(f'[1] {str(result_identical_1).upper()}')

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
uv_raw_char_reconstructed = [
    uuid.UUID(str(uuid.UUID(bytes=x))) if x is not None else None 
    for x in uv_raw
]
result_identical_2 = all((a == b) for a, b in zip(uv_raw_char_reconstructed, uv))
print(f'[1] {str(result_identical_2).upper()}')