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
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class RRawVector(bytes):
    """Simulates R's raw vector with attributes."""
    def __init__(self, data, iv=None):
        super().__init__(data)
        self.iv = iv

def sha256(x):
    if isinstance(x, str):
        x = x.encode('utf-8')
    return hashlib.sha256(x).digest()

def aes_cbc_encrypt(data, key):
    iv = os.urandom(16)
    
    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return a custom object that stores the IV as an attribute, mimicking R
    return RRawVector(ciphertext, iv=iv)

def aes_cbc_decrypt(data_with_iv, key):
    # Extract IV from the attribute if it's our custom RRawVector
    if isinstance(data_with_iv, RRawVector):
        iv = data_with_iv.iv
        ciphertext = bytes(data_with_iv)
    else:
        # Fallback if it's just bytes (though R's aes_cbc_decrypt usually relies on the attribute)
        raise ValueError("IV missing from data")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# passphrase <- charToRaw("This is super secret")
passphrase = "This is super secret".encode('utf-8')
# key <- sha256(passphrase)
key = sha256(passphrase)

# x <- serialize(iris, NULL)
# Since we cannot perfectly replicate R's serialize(), we use a consistent byte representation 
# of the iris dataframe to ensure the encryption/decryption cycle is tested.
import pandas as pd
x = iris.to_csv().encode('utf-8')

# y <- aes_cbc_encrypt(x, key = key)
y = aes_cbc_encrypt(x, key=key)

# x2 <- aes_cbc_decrypt(y, key = key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2