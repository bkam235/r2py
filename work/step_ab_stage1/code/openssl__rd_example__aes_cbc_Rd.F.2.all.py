import hashlib
import os
import numpy as np
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

def sha256(x, key=None):
    if isinstance(x, str):
        x = x.encode('utf-8')
    if key is not None:
        # R openssl sha256 with a key is an HMAC
        import hmac
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hmac.new(key, x, hashlib.sha256).digest()
    return hashlib.sha256(x).digest()

def aes_cbc_encrypt(data, key, iv=None):
    if iv is None:
        iv = os.urandom(16)
    
    # PKCS7 padding is required for CBC in cryptography library
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # R's openssl package attaches the IV as an attribute to the result
    # We return a tuple or a custom object to mimic this behavior
    return (ciphertext, iv)

def aes_cbc_decrypt(data_with_iv, key, iv=None):
    # In R, if iv is not provided, it's taken from the attribute of the data
    if iv is None:
        ciphertext, iv = data_with_iv
    else:
        ciphertext = data_with_iv

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# aes-256 requires 32 byte key
passphrase = "This is super secret"
# Convert string to raw bytes to match charToRaw
passphrase_raw = passphrase.encode('utf-8')
key = sha256(passphrase_raw)

# In R, serialize(iris, NULL) creates a binary blob. 
# To be execution-equivalent for the encryption test, we use a stable byte representation.
import pandas as pd
iris_df = pd.DataFrame(iris)
x = iris_df.to_csv(index=False).encode('utf-8')

y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2