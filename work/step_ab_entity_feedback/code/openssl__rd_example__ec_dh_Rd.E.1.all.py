from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def format_raw_bytes(b):
    """
    Matches R's raw vector printing format exactly.
    Example output:
          [1] 01 55 3b 59 f7 56 78 e7 cd 3a 4e e2 73 9d 6c ea af fc 38 93 18 8c 51 77 39
    [26] f8 8d ab c2 ec 57 c9 64 71 73 65 4e c6 81 44 09 45 16 b6 b9 74 a6 66 f9 b3
    [51] 6c 11 d1 e4 3c c5 20 fe 1f 70 5a ba c4 1b 8c c1
    """
    if not b:
        return ""
    
    lines = []
    for i in range(0, len(b), 25):
        chunk = b[i : i + 25]
        chunk_str = " ".join(f"{x:02x}" for x in chunk)
        index = i + 1
        # First line has 6 leading spaces, subsequent lines have 0
        prefix = f"      [{index}] " if i == 0 else f"[{index}] "
        lines.append(f"{prefix}{chunk_str}")
    
    return "\n".join(lines)

# Generate keys
# r2py:entity:alice_key
_alice_key_obj = ec.generate_private_key(ec.SECP521R1())
alice_key = _alice_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# r2py:entity:bob_key
_bob_key_obj = ec.generate_private_key(ec.SECP521R1())
bob_key = _bob_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# Extract public keys
# r2py:entity:as.list
_alice_pub_obj = _alice_key_obj.public_key()
# r2py:entity:alice_pub
alice_pub = _alice_pub_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# r2py:entity:as.list_1
_bob_pub_obj = _bob_key_obj.public_key()
# r2py:entity:bob_pub
bob_pub = _bob_pub_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# Both peers can derive the (same) shared secret via each other's pubkey
# r2py:entity:ec_dh
shared_secret_alice = _alice_key_obj.exchange(ec.ECDH(), _bob_pub_obj)
print(format_raw_bytes(shared_secret_alice))

# r2py:entity:ec_dh_1
shared_secret_bob = _bob_key_obj.exchange(ec.ECDH(), _alice_pub_obj)
print(format_raw_bytes(shared_secret_bob))