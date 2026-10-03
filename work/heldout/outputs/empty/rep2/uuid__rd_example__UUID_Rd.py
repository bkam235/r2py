# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import uuid
import numpy as np
import pandas as pd

# r2py:entity:u
def as_UUID(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [uuid.UUID(str(i)) if pd.notna(i) else None for i in x]
    if pd.isna(x):
        return None
    return uuid.UUID(str(x))

# r2py:entity:uv
def UUIDgenerate(n=1, output="uuid", use_time=None):
    res = []
    for _ in range(n):
        if use_time is True:
            res.append(uuid.uuid1())
        else:
            res.append(uuid.uuid4())
    
    if output == "string":
        return [str(u) for u in res]
    elif output == "raw":
        return [u.bytes for u in res]
    elif output == "uuid":
        return res
    return res

# r2py:entity:identical
def identical(x, y):
    if isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)):
        if len(x) != len(y):
            return False
        return all((a == b) if (a is not None and b is not None) else (a is b) for a, b in zip(x, y))
    if x is None or y is None:
        return x is y
    return x == y

# r2py:entity:as.raw
def as_raw(x):
    if isinstance(x, (list, np.ndarray)):
        return [u.bytes if u is not None else None for u in x]
    if x is None:
        return None
    return x.bytes

# Formatting helper to match R output
def r_print_uuid(x):
    if isinstance(x, uuid.UUID):
        print(f"UUID: {str(x)}")
    elif isinstance(x, list):
        print("UUID vector:")
        for i, val in enumerate(x, 1):
            print(f'[{i}] "{str(val) if val is not None else "NA"}"')
    else:
        print(x)

# r2py:entity:u
u = as_UUID("837bc850-07d9-42f9-9afb-716409bf87b7")
r_print_uuid(u)

# r2py:entity:uv
uv = [u, None] + UUIDgenerate(n=3, output="uuid")
r_print_uuid(uv)

# r2py:entity:as.character
print(f'[1] "{str(u)}"')

# uv == u
uv_eq_u = [ (val == u if val is not None else False) for val in uv]
print(f'[1] {" ".join(map(str, uv_eq_u)).upper()}')

# r2py:entity:is.na
is_na_uv = [pd.isna(val) for val in uv]
print(f'[1] {" ".join(map(str, is_na_uv)).upper()}')

# r2py:entity:identical
print(f'[1] {str(identical(as_UUID([str(i) if i is not None else None for i in uv]), uv)).upper()}')

# r2py:entity:as.raw
raw_u = as_raw(u)
print(f'[1] {" ".join(f"{b:02x}" for b in raw_u)}')

# All forms are can be coerced losslessly
# r2py:entity:identical_1
uv_raw = as_raw(uv)
uv_from_raw = as_UUID([uuid.UUID(bytes=b) if b is not None else None for b in uv_raw])
print(f'[1] {str(identical(uv_from_raw, uv)).upper()}')

# r2py:entity:identical_2
uv_char = [str(i) if i is not None else None for i in uv_from_raw]
uv_final = as_UUID(uv_char)
print(f'[1] {str(identical(uv_final, uv)).upper()}')