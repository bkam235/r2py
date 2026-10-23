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

def sha256(x):
    if isinstance(x, str):
        x = x.encode('utf-8')
    return hashlib.sha256(x).digest()

def aes_cbc_encrypt(data, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # R's openssl::aes_cbc_encrypt returns the IV concatenated with the ciphertext
    return iv + ciphertext

def aes_cbc_decrypt(data, key):
    iv = data[:16]
    ciphertext = data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data_unpadded = unpadder.update(padded_data) + unpadder.finalize()
    return data_unpadded

# r2py:entity:passphrase
passphrase = "This is super secret".encode('utf-8')
# r2py:entity:key
key = sha256(passphrase)

# simulate R's serialize(iris, NULL)
# We convert the dataframe to a byte string to act as the serialized object
# In a real scenario, this would be the R serialization format.
import pandas as pd
x = pd.DataFrame(iris).to_csv(index=False).encode('utf-8')

# r2py:entity:y
y = aes_cbc_encrypt(x, key=key)
# r2py:entity:x2
x2 = aes_cbc_decrypt(y, key=key)

# r2py:entity:stopifnot
assert x == x2