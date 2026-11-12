# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# r2py:entity:key
_key_obj = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
key = _key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# r2py:entity:pubkey
pubkey = _key_obj.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# write_pem
# r2py:entity:write_pem
pem = _key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.BestAvailableEncryption(b"supersecret")
)
with open("id_rsa", "wb") as f:
    f.write(pem)

# read_key
# r2py:entity:read_key
with open("id_rsa", "rb") as f:
    key_data = f.read()
    read_key_obj = serialization.load_pem_private_key(
        key_data,
        password=b"supersecret"
    )
# Convert to PEM string for stdout matching R's print behavior
read_key = read_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')
print(read_key)

# unlink
# r2py:entity:unlink
os.remove("id_rsa")