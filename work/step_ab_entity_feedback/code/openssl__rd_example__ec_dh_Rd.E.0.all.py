import base64
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
    return "      " + result if len(lines) > 0 else ""

def key_to_pem(key):
    """Helper to convert cryptography key to R-style PEM string."""
    if hasattr(key, "private_bytes"):
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    else:
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    # R's openssl prints PEM without the header/footer markers in some contexts 
    # but the verification output shows the Base64 body.
    # We strip the delimiters and whitespace to match the R output format seen in the log.
    lines = pem.decode().strip().split('\n')
    return "".join(line.strip() for line in lines if "---" not in line)

# Generate keys
# r2py:entity:alice_key
alice_key_obj = ec.generate_private_key(ec.SECP521R1())
alice_key = key_to_pem(alice_key_obj)

# r2py:entity:bob_key
bob_key_obj = ec.generate_private_key(ec.SECP521R1())
bob_key = key_to_pem(bob_key_obj)

# Derive public keys
# r2py:entity:as.list
alice_pub_obj = alice_key_obj.public_key()
# r2py:entity:alice_pub
alice_pub = key_to_pem(alice_pub_obj)

# r2py:entity:as.list_1
bob_pub_obj = bob_key_obj.public_key()
# r2py:entity:bob_pub
bob_pub = key_to_pem(bob_pub_obj)

# Both peers can derive the (same) shared secret via each other's pubkey
# r2py:entity:ec_dh
shared_secret_alice = alice_key_obj.exchange(ec.ECDH(), bob_pub_obj)
print(format_raw_bytes(shared_secret_alice))

# r2py:entity:ec_dh_1
shared_secret_bob = bob_key_obj.exchange(ec.ECDH(), alice_pub_obj)
print(format_raw_bytes(shared_secret_bob))