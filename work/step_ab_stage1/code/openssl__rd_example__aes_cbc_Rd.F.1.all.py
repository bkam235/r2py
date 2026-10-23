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

# r2py:entity:key
def sha256(x, key=None):
    if isinstance(x, str):
        x = x.encode('utf-8')
    if key is not None:
        import hmac
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hmac.new(key, x, hashlib.sha256).digest()
    return hashlib.sha256(x).digest()

# r2py:entity:y
def aes_cbc_encrypt(data, key, iv=None):
    if iv is None:
        iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # In R's openssl, the result is a raw vector and the IV is an attribute.
    # To simulate this in Python and allow decryption without passing IV separately,
    # we attach the IV to the object.
    class EncryptedData(bytes):
        pass
    
    result = EncryptedData(ciphertext)
    result.iv = iv
    return result

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
passphrase = "This is super secret"
# r2py:entity:key
key = sha256(passphrase)

# R's serialize(iris, NULL) creates a binary representation of the object.
# Since we cannot perfectly mimic R's internal serialization, 
# we use a consistent binary representation of the dataframe provided by the shim.
import pandas as pd
df_iris = pd.DataFrame(iris)
x = df_iris.to_csv().encode('utf-8')

# r2py:entity:y
y = aes_cbc_encrypt(x, key=key)
# r2py:entity:x2
x2 = aes_cbc_decrypt(y, key=key)

# r2py:entity:stopifnot
assert x == x2