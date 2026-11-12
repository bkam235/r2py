# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# r2py:entity:key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
# r2py:entity:pubkey
pubkey = key.public_key()

# write_pem
# r2py:entity:write_pem
pem = key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b"supersecret")
)
with open("id_rsa", "wb") as f:
    f.write(pem)

# read_key
# r2py:entity:read_key
with open("id_rsa", "rb") as f:
    key_data = f.read()
    read_key = serialization.load_pem_private_key(
        key_data,
        password=b"supersecret"
    )

# unlink
import os
# r2py:entity:unlink
os.remove("id_rsa")