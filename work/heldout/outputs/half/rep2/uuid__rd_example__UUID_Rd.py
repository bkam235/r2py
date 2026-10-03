import uuid
import numpy as np

# Helper to mimic R's UUID printing style for vectors
def print_uuid_vector(uv):
    print("UUID vector:")
    for i, val in enumerate(uv, 1):
        print(f'[{i}] "{str(val)}"')

# Helper to mimic R's logical vector printing
def print_logical_vector(vec):
    vals = " ".join([str(val).upper() for val in vec])
    print(f"[1] {vals}")

# Helper to mimic R's single logical value printing
def print_logical_single(val):
    print(f"[1] {str(val).upper()}")

# (u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
# r2py:entity:u
u = uuid.UUID("837bc850-07d9-42f9-9afb-716409bf87b7")
print(f'UUID: {str(u)}')

# (uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
# In R's uuid package, NA is represented by this specific UUID constant
# r2py:entity:uv
NA_UUID = uuid.UUID("a2070000-0000-f07f-0000-000000000000")
uv = np.array([u, NA_UUID, uuid.uuid4(), uuid.uuid4(), uuid.uuid4()], dtype=object)
print_uuid_vector(uv)

# as.character(u)
# r2py:entity:as.character
print(f'[1] "{str(u)}"')

# uv == u
# R's == returns a logical vector
res_eq = np.array([val == u for val in uv])
print_logical_vector(res_eq)

# is.na(uv)
# r2py:entity:is.na
res_na = np.array([val == NA_UUID for val in uv])
print_logical_vector(res_na)

# identical(as.UUID(as.character(uv)), uv)
# r2py:entity:identical
uv_char_back = np.array([uuid.UUID(str(x)) for x in uv], dtype=object)
print_logical_single(np.array_equal(uv_char_back, uv))

# as.raw(u)
# r2py:entity:as.raw
raw_u = u.bytes
print(f"[1] {' '.join(f'{b:02x}' for b in raw_u)}")

# identical(as.UUID(as.raw(uv)), uv)
# r2py:entity:identical_1
uv_raw_back = np.array([uuid.UUID(bytes=x.bytes) for x in uv], dtype=object)
print_logical_single(np.array_equal(uv_raw_back, uv))

# identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)
# r2py:entity:identical_2
uv_raw_char_back = np.array([uuid.UUID(str(uuid.UUID(bytes=x.bytes))) for x in uv], dtype=object)
print_logical_single(np.array_equal(uv_raw_char_back, uv))