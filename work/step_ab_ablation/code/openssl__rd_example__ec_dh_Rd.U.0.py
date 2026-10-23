from cryptography.hazmat.primitives.asymmetric import ec

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
            lines.append(f"[{index}] {chunk_str}")
    
    return "\n".join(lines)

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