from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# r2py:entity:key
# Generate keypair
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
# pubkey <- as.list(key)$pubkey
pubkey = _key_obj.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

# Write/read the key with a passphrase
# r2py:entity:write_pem
pem_data = _key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b"supersecret")
)
with open("id_rsa", "wb") as f:
    f.write(pem_data)

# r2py:entity:read_key
with open("id_rsa", "rb") as f:
    key_bytes = f.read()
    read_key_obj = serialization.load_pem_private_key(
        key_bytes,
        password=b"supersecret"
    )
    # R's read_key auto-prints the PEM representation of the key
    read_key = read_key_obj.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    print(read_key)

# r2py:entity:unlink
os.remove("id_rsa")