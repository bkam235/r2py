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

# Need two EC keypairs from the same curve
# r2py:entity:alice_key
alice_key = ec.generate_private_key(ec.SECP521R1())
# r2py:entity:bob_key
bob_key = ec.generate_private_key(ec.SECP521R1())

# Derive public keys
# r2py:entity:as.list
alice_pub = alice_key.public_key()
# r2py:entity:as.list_1
bob_pub = bob_key.public_key()

# Both peers can derive the (same) shared secret via each other's pubkey
# r2py:entity:ec_dh
res_ec_dh = alice_key.exchange(ec.ECDH(), bob_pub)
print(format_raw_bytes(res_ec_dh))

# r2py:entity:ec_dh_1
res_ec_dh_1 = bob_key.exchange(ec.ECDH(), alice_pub)
print(format_raw_bytes(res_ec_dh_1))