from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# r2py:entity:key
_private_key_obj = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
# R's rsa_keygen() returns the key in PEM format
key = _private_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# r2py:entity:pubkey
# R's as.list(key)$pubkey returns the public key in PEM format
pubkey = _private_key_obj.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# r2py:entity:write_pem
pem_data = _private_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.BestAvailableEncryption(b"supersecret")
)
with open("id_rsa", "wb") as f:
    f.write(pem_data)

# r2py:entity:read_key
with open("id_rsa", "rb") as f:
    key_bytes = f.read()
    # read_key in R returns the key object; since it's auto-printed, 
    # we load it and then convert to PEM to match the expected string output.
    loaded_key = serialization.load_pem_private_key(
        key_bytes,
        password=b"supersecret"
    )
    read_key = loaded_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    print(read_key)

# r2py:entity:unlink
os.remove("id_rsa")