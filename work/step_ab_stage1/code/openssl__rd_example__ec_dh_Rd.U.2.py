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
    # R prints raw bytes in groups of 25
    for i in range(0, len(b), 25):
        chunk = b[i : i + 25]
        chunk_str = " ".join(f"{x:02x}" for x in chunk)
        index = i + 1
        lines.append(f"[{index}] {chunk_str}")
    
    # R's first line is indented by 6 spaces
    if not lines:
        return ""
    
    first_line = "      " + lines[0]
    other_lines = "\n".join(lines[1:])
    
    return first_line + ("\n" + other_lines if other_lines else "")

# Generate keys (equivalent to ec_keygen("P-521"))
# r2py:entity:alice_key
alice_key = ec.generate_private_key(ec.SECP521R1())
# r2py:entity:bob_key
bob_key = ec.generate_private_key(ec.SECP521R1())

# Derive public keys (equivalent to as.list(key)$pubkey)
# r2py:entity:as.list
alice_pub = alice_key.public_key()
# r2py:entity:as.list_1
bob_pub = bob_key.public_key()

# Both peers can derive the (same) shared secret via each other's pubkey
# r2py:entity:ec_dh
shared_secret_alice = alice_key.exchange(ec.ECDH(), bob_pub)
print(format_raw_bytes(shared_secret_alice))

# r2py:entity:ec_dh_1
shared_secret_bob = bob_key.exchange(ec.ECDH(), alice_pub)
print(format_raw_bytes(shared_secret_bob))