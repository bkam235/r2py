import uuid
import numpy as np

# r2py:entity:u
def as_UUID(x):
    if x is None:
        return None
    if isinstance(x, uuid.UUID):
        return x
    if isinstance(x, (list, np.ndarray)):
        return [as_UUID(i) for i in x]
    try:
        # R's as.UUID handles strings and other types via as.character
        return uuid.UUID(str(x))
    except (ValueError, TypeError):
        return None

# r2py:entity:uv
def UUIDgenerate(n=1, output="uuid"):
    res = [uuid.uuid4() for _ in range(n)]
    if output == "string":
        return [str(u) for u in res]
    elif output == "raw":
        return [u.bytes for u in res]
    return res

# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
u = as_UUID("837bc850-07d9-42f9-9afb-716409bf87b7")
print(u)

# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
generated = UUIDgenerate(n=3, output="uuid")
uv = [u, None] + generated
# To match R's printing of UUID vectors:
print(f'[1] "{uv[0]}"')
print(f'[2] "{uv[1] if uv[1] is not None else "NA"}"')
print(f'[3] "{uv[2]}"')
print(f'[4] "{uv[3]}"')
print(f'[5] "{uv[4]}"')

# as.character(u)
# r2py:entity:as.character
print(f'[1] "{str(u)}"')

# uv == u
res_eq = []
for x in uv:
    if x is None:
        res_eq.append("NA")
    else:
        res_eq.append(str(x == u).upper())
print(f'[1] {" ".join(res_eq)}')

# is.na(uv)
# r2py:entity:is.na
res_na = [str(x is None).upper() for x in uv]
print(f'[1] {" ".join(res_na)}')

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
uv_char = [str(x) if x is not None else "NA" for x in uv]
uv_reconstructed = [as_UUID(x) if x != "NA" else None for x in uv_char]
print(f'[1] {str(uv_reconstructed == uv).upper()}')

# as.raw(u)
# r2py:entity:as.raw
raw_u = u.bytes
print(f'[1] {" ".join(f"{b:02x}" for b in raw_u)}')

# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
raw_uv = [x.bytes if x is not None else None for x in uv]
reconstructed_raw_uv = [uuid.UUID(bytes=x) if x is not None else None for x in raw_uv]
print(f'[1] {str(reconstructed_raw_uv == uv).upper()}')

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
inner_uuid = reconstructed_raw_uv
inner_char = [str(x) if x is not None else "NA" for x in inner_uuid]
final_uuid = [as_UUID(x) if x != "NA" else None for x in inner_char]
print(f'[1] {str(final_uuid == uv).upper()}')