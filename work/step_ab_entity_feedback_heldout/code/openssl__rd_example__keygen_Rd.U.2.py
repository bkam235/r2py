from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# r2py:entity:key
# In R, rsa_keygen() results in an object that prints as PEM.
# We generate the key and immediately convert it to PEM to match the expected output form.
_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
key = _private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# r2py:entity:pubkey
# as.list(key)$pubkey in R returns the public key in PEM format.
pubkey = _private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# write_pem
# r2py:entity:write_pem
# Note: R's write_pem writes the private key.
pem = _private_key.private_bytes(
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
    # load_pem_private_key returns the object; R's read_key prints the PEM string.
    _loaded_key = serialization.load_pem_private_key(
        key_data,
        password=b"supersecret"
    )
    # Convert back to PEM string to match R's output format
    read_key = _loaded_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

# R auto-prints the result of the last expression
print(read_key)

# unlink
# r2py:entity:unlink
os.remove("id_rsa")