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
        if i == 0:
            # First line has leading spaces for alignment
            lines.append(f"      [{index}] {chunk_str}")
        else:
            # Subsequent lines start with the index
            lines.append(f"[{index}] {chunk_str}")
    
    return "\n".join(lines)

# Generate internal key objects for calculations
_alice_priv = ec.generate_private_key(ec.SECP521R1())
_bob_priv = ec.generate_private_key(ec.SECP521R1())

# Store as PEM bytes to match R's object printing behavior
# r2py:entity:alice_key
alice_key = _alice_priv.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
# r2py:entity:bob_key
bob_key = _bob_priv.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Derive public keys
# r2py:entity:as.list
alice_pub_obj = _alice_priv.public_key()
# r2py:entity:alice_pub
alice_pub = alice_pub_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# r2py:entity:as.list_1
bob_pub_obj = _bob_priv.public_key()
# r2py:entity:bob_pub
bob_pub = bob_pub_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Both peers can derive the (same) shared secret via each other's pubkey
# r2py:entity:ec_dh
shared_secret_alice = _alice_priv.exchange(ec.ECDH(), bob_pub_obj)
print(format_raw_bytes(shared_secret_alice))

# r2py:entity:ec_dh_1
shared_secret_bob = _bob_priv.exchange(ec.ECDH(), alice_pub_obj)
print(format_raw_bytes(shared_secret_bob))