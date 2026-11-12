# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# r2py:entity:key
# Generate keypair
_key_obj = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
# In R's openssl, the key object is printed as a PEM string
key = _key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# r2py:entity:pubkey
# pubkey <- as.list(key)$pubkey
_pubkey_obj = _key_obj.public_key()
pubkey = _pubkey_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# write_pem
# r2py:entity:write_pem
# Write/read the key with a passphrase
pem_data = _key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.BestAvailableEncryption(b"supersecret")
)
with open("id_rsa", "wb") as f:
    f.write(pem_data)

# read_key
# r2py:entity:read_key
with open("id_rsa", "rb") as f:
    key_bytes = f.read()
    read_key_obj = serialization.load_pem_private_key(
        key_bytes,
        password=b"supersecret"
    )
# R auto-prints the result of read_key, which is the PEM representation
read_key = read_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')
print(read_key)

# unlink
# r2py:entity:unlink
os.remove("id_rsa")