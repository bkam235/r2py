# Translated from <R script> by r2py v0.3.0

import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/openssl__rd_example__aes_cbc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'openssl__rd_example__aes_cbc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def sha256(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).digest()

def aes_cbc_encrypt(data, key):
    # R's openssl::aes_cbc_encrypt generates a random IV and attaches it as an attribute.
    # To maintain execution equivalence for the identity check, we need the same IV during decrypt.
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # To mimic R's attribute, we'll store the IV on the bytes object (though not standard Python)
    # or return it. But since the R test is identical(x, x2), we just need to ensure decrypt uses the same IV.
    # In R, aes_cbc_decrypt uses the IV attribute if not provided.
    setattr(ciphertext, 'iv', iv)
    return ciphertext

def aes_cbc_decrypt(ciphertext, key, iv=None):
    if iv is None:
        iv = getattr(ciphertext, 'iv', None)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# aes-256 requires 32 byte key
passphrase = "This is super secret".encode('utf-8')
key = sha256(passphrase)

# Use a consistent serialization for Python to ensure identical(x, x2) works
# Since we can't easily replicate R's internal serialize(), we use a stable byte representation.
import pickle
x = pickle.dumps(iris)

# symmetric encryption uses same key for decryption
y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2