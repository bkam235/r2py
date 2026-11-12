# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/openssl__rd_example__aes_cbc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'openssl__rd_example__aes_cbc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def sha256(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).digest()

def aes_cbc_encrypt(data, key):
    # R's openssl::aes_cbc_encrypt generates a random IV and returns ciphertext
    # In R, the IV is stored as an attribute of the returned raw vector
    iv = os.urandom(16)
    
    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # We return the ciphertext. To make decrypt work without passing IV, 
    # we can attach it to the object, but since Python bytes don't have attributes,
    # we'll return a simple custom object or just the bytes and handle IV separately.
    # For the purpose of the 'identical' check, we just need the cycle to work.
    class EncryptedData(bytes):
        def __init__(self, data, iv):
            super().__init__(data)
            self.iv = iv
            
    return EncryptedData(ciphertext, iv)

def aes_cbc_decrypt(encrypted_data, key):
    # Extract IV from the custom object
    iv = getattr(encrypted_data, 'iv', None)
    if iv is None:
        raise ValueError("IV not found in encrypted data")
        
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# aes-256 requires 32 byte key
passphrase = "This is super secret"
key = sha256(passphrase)

# x <- serialize(iris, NULL)
# We simulate the serialization of the iris dataframe to bytes
import pandas as pd
x = pd.DataFrame(iris).to_csv(index=False).encode('utf-8')

# symmetric encryption uses same key for decryption
y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2