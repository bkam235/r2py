from cryptography.hazmat.primitives.asymmetric import ec

# Generate keys (equivalent to ec_keygen("P-521"))
# r2py:entity:alice_key
alice_key = ec.generate_private_key(ec.SECP521R1())
# r2py:entity:bob_key
bob_key = ec.generate_private_key(ec.SECP521R1())

# Derive public keys (equivalent to as.list(key)$pubkey)
# r2py:entity:as.list
alice_pub = alice_key.public_key()
# r2py:entity:alice_pub
alice_pub = alice_pub

# r2py:entity:as.list_1
bob_pub = bob_key.public_key()
# r2py:entity:bob_pub
bob_pub = bob_pub

# Both peers can derive the (same) shared secret via each other's pubkey
# r2py:entity:ec_dh
ec_dh = alice_key.exchange(ec.ECDH(), bob_pub)

# r2py:entity:ec_dh_1
ec_dh_1 = bob_key.exchange(ec.ECDH(), alice_pub)