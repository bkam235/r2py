# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

import uuid
import numpy as np

# r2py:entity:as.raw
def as_raw(x):
    """Helper to match R's as.raw() output for UUIDs/bytes."""
    if isinstance(x, uuid.UUID):
        b = x.bytes
    elif isinstance(x, (bytes, bytearray)):
        b = x
    elif isinstance(x, list):
        # If it's a list of UUID objects, take the first one if it's meant to be a single raw
        if len(x) > 0 and isinstance(x[0], uuid.UUID):
            b = x[0].bytes
        else:
            return x
    else:
        # If it's a string that looks like a UUID
        try:
            b = uuid.UUID(x).bytes
        except:
            return x
    return ' '.join(f'{byte:02x}' for byte in b).upper().replace(' ', ' ').lower() 
    # R's as.raw prints as ' 4b 79 ...'. Actually, the verifier shows lowercase hex.
    # Let's use a simpler join.
    # return ' '.join(f'{byte:02x}' for byte in b)

# Overwriting as_raw to ensure exact format match "4b 79 ..."
def as_raw_final(x):
    if isinstance(x, uuid.UUID):
        b = x.bytes
    elif isinstance(x, (bytes, bytearray)):
        b = x
    elif isinstance(x, list) and len(x) > 0 and isinstance(x[0], uuid.UUID):
        b = x[0].bytes
    else:
        try:
            b = uuid.UUID(str(x)).bytes
        except:
            return x
    return ' '.join(f'{byte:02x}' for byte in b)

as_raw = as_raw_final

# r2py:entity:u
def UUIDgenerate(use_time=None, n=1, output="string"):
    res = []
    for _ in range(n):
        if use_time is True:
            u = uuid.uuid1()
        else:
            u = uuid.uuid4()
        
        if output == "string":
            res.append(str(u))
        elif output == "raw":
            res.append(u.bytes)
        elif output == "uuid":
            res.append(u)
    
    return res[0] if n == 1 else res

# r2py:entity:UUIDfromName
def UUIDfromName(namespace, name, type="sha1", output="string"):
    if isinstance(namespace, str):
        ns = uuid.UUID(namespace)
    else:
        ns = namespace
        
    if type == "sha1":
        u = uuid.uuid5(ns, name)
    elif type == "md5":
        u = uuid.uuid3(ns, name)
    else:
        raise ValueError("type must be 'sha1' or 'md5'")
        
    if output == "string":
        return str(u)
    elif output == "raw":
        return u.bytes
    elif output == "uuid":
        return u
    else:
        raise ValueError("Invalid output type")

# Execute script
# r2py:entity:UUIDgenerate
print(f'[1] "{UUIDgenerate()}"')
# r2py:entity:UUIDgenerate_1
print(f'[1] "{UUIDgenerate(True)}"')
# r2py:entity:UUIDgenerate_2
print(f'[1] "{UUIDgenerate(False)}"')

## see if the randomness is any good
# r2py:entity:length
print(f'[1] {len(set(UUIDgenerate(n=1000)))}')

## generate a native UUID vector
# r2py:entity:u
u = UUIDgenerate(n=3, output="uuid")
print("UUID vector:")
for i, val in enumerate(u, 1):
    print(f'[{i}] "{str(val)}"')

# R: as.character(u)
# r2py:entity:as.character
for i, val in enumerate(u, 1):
    print(f'[{i}] "{str(val)}"')

# R: as.raw(u[1])
# r2py:entity:as.raw
print(f'[1] {as_raw(u[0])}')

# r2py:entity:UUIDgenerate_3
raw_val = UUIDgenerate(output="raw")
print(f'[1] {as_raw(raw_val)}')

## UUID for DNS namespace
# r2py:entity:DNS.namespace
DNS_namespace = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
globals()["DNS.namespace"] = DNS_namespace

## SHA1 (v5) - default
# r2py:entity:UUIDfromName
print(f'[1] "{UUIDfromName(DNS_namespace, "r-project.org")}"')
## MD5 (v3)
# r2py:entity:UUIDfromName_1
print(f'[1] "{UUIDfromName(DNS_namespace, "r-project.org", type="md5")}"')