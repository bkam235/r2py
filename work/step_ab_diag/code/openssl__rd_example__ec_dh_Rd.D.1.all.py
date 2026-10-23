# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def format_raw_bytes(b):
    """
    Matches R's raw vector printing format:
          [1] 01 20 ... (up to 25 elements)
    [26] dd bc ...
    """
    if not b:
        return ""
    
    lines = []
    for i in range(0, len(b), 25):
        chunk = b[i : i + 25]
        chunk_str = " ".join(f"{x:02x}" for x in chunk)
        index = i + 1
        lines.append(f"[{index}] {chunk_str}")
    
    result = "\n".join(lines)
    # R's print.raw adds leading spaces to the first line for alignment
    return "      " + result if len(lines) > 0 else ""

# Generate keys (equivalent to ec_keygen("P-521"))
_alice_key_obj = ec.generate_private_key(ec.SECP521R1())
_bob_key_obj = ec.generate_private_key(ec.SECP521R1())

# To match R's output for data entities, convert keys to PEM strings
# r2py:entity:alice_key
alice_key = _alice_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# r2py:entity:bob_key
bob_key = _bob_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# Derive public keys (equivalent to as.list(key)$pubkey)
_alice_pub_obj = _alice_key_obj.public_key()
_bob_pub_obj = _bob_key_obj.public_key()

# r2py:entity:as.list
# r2py:entity:alice_pub
alice_pub = _alice_pub_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# r2py:entity:as.list_1
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