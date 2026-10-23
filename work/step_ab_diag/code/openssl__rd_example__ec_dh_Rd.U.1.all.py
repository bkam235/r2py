from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def format_raw_bytes(b):
    """
    Matches R's print.raw output format.
    R prints raw vectors in chunks of 25 bytes.
    The first line is indented, and subsequent lines start with [index].
    """
    if not b:
        return ""
    
    lines = []
    for i in range(0, len(b), 25):
        chunk = b[i : i + 25]
        chunk_str = " ".join(f"{x:02x}" for x in chunk)
        index = i + 1
        lines.append(f"[{index}] {chunk_str}")
    
    # R's print.raw: first line has 6 leading spaces, subsequent lines have 0
    formatted_lines = []
    for idx, line in enumerate(lines):
        if idx == 0:
            formatted_lines.append("      " + line)
        else:
            formatted_lines.append(line)
            
    return "\n".join(formatted_lines)

# Generate keys (equivalent to ec_keygen("P-521"))
# r2py:entity:alice_key
alice_key = ec.generate_private_key(ec.SECP521R1())
# r2py:entity:bob_key
bob_key = ec.generate_private_key(ec.SECP521R1())

# Extract public keys (equivalent to as.list(key)$pubkey)
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