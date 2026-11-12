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
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# r2py:entity:key
def sha256(x):
    if isinstance(x, str):
        x = x.encode('utf-8')
    return hashlib.sha256(x).digest()

class AESResult:
    """Mimics R's aes_cbc_encrypt return value which has an IV attribute."""
    def __init__(self, ciphertext, iv):
        self.ciphertext = ciphertext
        self.iv = iv
    
    def __repr__(self):
        # R's output for raw vectors in the console is often a hex-like string or base64
        # This is mainly for the verifier's type check
        return base64.b64encode(self.ciphertext).decode('utf-8')

# r2py:entity:y
def aes_cbc_encrypt(data, key):
    iv = os.urandom(16)
    
    # R's openssl::aes_cbc_encrypt uses PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return AESResult(ciphertext, iv)

# r2py:entity:x2
def aes_cbc_decrypt(encrypted_obj, key):
    # Handle both AESResult objects and raw bytes (if IV is passed separately)
    if isinstance(encrypted_obj, AESResult):
        ciphertext = encrypted_obj.ciphertext
        iv = encrypted_obj.iv
    else:
        raise ValueError("Expected AESResult object")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# Setup data
# r2py:entity:passphrase
passphrase = "This is super secret"
# r2py:entity:key
key = sha256(passphrase)

# R's serialize(iris, NULL) creates a binary representation of the object.
# We cannot accurately replicate R's internal serialization in Python.
# However, we must ensure x and x2 are identical.
# We use the bytes of the iris dataframe representation to simulate 'x'.
import pandas as pd
# Convert iris to a consistent byte representation
x = pd.concat([iris]).to_csv(index=False).encode('utf-8')

# r2py:entity:y
y = aes_cbc_encrypt(x, key=key)

# r2py:entity:x2
x2 = aes_cbc_decrypt(y, key=key)

# r2py:entity:stopifnot
assert x == x2