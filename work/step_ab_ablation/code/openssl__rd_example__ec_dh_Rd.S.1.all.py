from cryptography.hazmat.primitives.asymmetric import ec

# r2py:entity:import_openssl
# (openssl import handled by cryptography)

# r2py:entity:suppressPackageStartupMessages
# (No-op in Python)

# Need two EC keypairs from the same curve
# r2py:entity:alice_key
alice_key = ec.generate_private_key(ec.SECP521R1())
# r2py:entity:bob_key
bob_key = ec.generate_private_key(ec.SECP521R1())

# Derive public keys
# r2py:entity:as.list
# In R, as.list(alice_key)$pubkey extracts the public key
# r2py:entity:alice_pub
alice_pub = alice_key.public_key()

# r2py:entity:as.list_1
# r2py:entity:bob_pub
bob_pub = bob_key.public_key()

# Both peers can derive the (same) shared secret via each other's pubkey
# In R, these top-level calls print the result of ec_dh
# r2py:entity:ec_dh
ec_dh = alice_key.exchange(ec.ECDH(), bob_pub)

# r2py:entity:ec_dh_1
ec_dh_1 = bob_key.exchange(ec.ECDH(), alice_pub)