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
import pickle
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# r2py:entity:key
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

# r2py:entity:y
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

# r2py:entity:x2
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

# Setup data
# r2py:entity:passphrase
passphrase = "This is super secret".encode('utf-8')
# r2py:entity:key
key = sha256(passphrase)

# R's iris dataset is a data frame. We simulate the serialized version.
# Since 'iris' is a standard R dataset, we'll use a dummy pandas dataframe 
# or just a byte string to represent the serialized object.
# r2py:entity:x
import pandas as pd
from sklearn.datasets import load_iris
iris_data = load_iris()
iris['species'] = iris_data.target

x = pickle.dumps(iris)
# r2py:entity:y
y = aes_cbc_encrypt(x, key=key)
# r2py:entity:x2
x2 = aes_cbc_decrypt(y, key=key)

# r2py:entity:stopifnot
assert np.array_equal(np.frombuffer(x, dtype=np.uint8), np.frombuffer(x2, dtype=np.uint8))