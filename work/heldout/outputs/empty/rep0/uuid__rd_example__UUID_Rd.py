# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import uuid
import numpy as np

# suppressPackageStartupMessages(library(uuid))
# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
# r2py:entity:u
u = uuid.UUID("837bc850-07d9-42f9-9afb-716409bf87b7")
print(f"      UUID: {u}")

# r2py:entity:uv
# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
# UUIDgenerate(n=3, output="uuid") generates 3 random UUIDs. 
# Since we can't predict them, we use uuid.uuid4()
uv = np.array([u, None, uuid.uuid4(), uuid.uuid4(), uuid.uuid4()], dtype=object)
print("      UUID vector:")
for i, val in enumerate(uv, 1):
    print(f'[{i}] "{val}"' if val is not None else f'[{i}] "NA"')

# as.character(u)
# r2py:entity:as.character
print(f'      [1] "{str(u)}"')

# uv == u
# R's == on a vector returns a logical vector
res_eq = np.array([val == u for val in uv])
print(f'      [1] {" ".join(map(str, res_eq)).upper()}')

# is.na(uv)
# r2py:entity:is.na
res_na = np.array([val is None for val in uv])
print(f'      [1] {" ".join(map(str, res_na)).upper()}')

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
def as_uuid_vec(vec):
    return np.array([uuid.UUID(str(x)) if x is not None else None for x in vec], dtype=object)

uv_conv = as_uuid_vec(uv)
# identical checks if two objects are exactly the same
print(f'      [1] {"TRUE" if np.array_equal(uv_conv, uv, equal_nan=False) else "FALSE"}')

# as.raw(u)
# r2py:entity:as.raw
raw_u = u.bytes
raw_hex = " ".join(f"{b:02x}" for b in raw_u)
print(f'      [1] {raw_hex}')

# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
def as_uuid_raw_vec(vec):
    return np.array([uuid.UUID(bytes=x.bytes) if x is not None else None for x in vec], dtype=object)

uv_raw_conv = as_uuid_raw_vec(uv)
print(f'      [1] {"TRUE" if np.array_equal(uv_raw_conv, uv, equal_nan=False) else "FALSE"}')

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
uv_full_conv = as_uuid_vec(as_uuid_raw_vec(uv))
print(f'      [1] {"TRUE" if np.array_equal(uv_full_conv, uv, equal_nan=False) else "FALSE"}')