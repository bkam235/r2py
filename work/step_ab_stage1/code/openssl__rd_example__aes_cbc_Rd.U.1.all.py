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

# r2py:entity:key
def sha256(x):
    if isinstance(x, str):
        x = x.encode('utf-8')
    return hashlib.sha256(x).digest()

# R's aes_cbc_encrypt returns ciphertext and stores IV in attributes.
# To mimic the R script's flow (where x2 is decrypted from y),
# we can store the IV along with the ciphertext.
def aes_cbc_encrypt(data, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return as an object that holds both, mimicking the R attribute structure
    class EncryptedData:
        def __init__(self, ct, iv):
            self.ciphertext = ct
            self.iv = iv
    return EncryptedData(ciphertext, iv)

def aes_cbc_decrypt(encrypted_obj, key):
    ciphertext = encrypted_obj.ciphertext
    iv = encrypted_obj.iv
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# R's serialize(iris, NULL) creates a binary blob. 
# Since we cannot perfectly replicate R's internal serialization in Python, 
# and the goal is to verify the encryption cycle, we use a consistent binary 
# representation of the dataframe.
def serialize_r_like(df):
    import pandas as pd
    return pd.DataFrame(df).to_pickle(None) if hasattr(pd.DataFrame, 'to_pickle') else str(df).encode('utf-8')

# r2py:entity:passphrase
passphrase = "This is super secret"
# r2py:entity:key
key = sha256(passphrase)

# r2py:entity:x
# R: x <- serialize(iris, NULL)
# We use a stable byte representation to test the symmetric encryption.
import pandas as pd
x = pd.DataFrame(iris).to_csv(index=False).encode('utf-8')

# r2py:entity:y
y = aes_cbc_encrypt(x, key=key)

# r2py:entity:x2
x2 = aes_cbc_decrypt(y, key=key)

# r2py:entity:stopifnot
assert np.array_equal(np.frombuffer(x, dtype=np.uint8), np.frombuffer(x2, dtype=np.uint8))