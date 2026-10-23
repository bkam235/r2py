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
    iv = os.urandom(16)
    # R openssl uses PKCS7 padding for AES_CBC
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # R's openssl returns the ciphertext and stores IV in attributes.
    # For equivalence in a Python environment where we need to decrypt, 
    # we can store the IV with the ciphertext.
    return ciphertext + iv # This is a common way to store IV, but we must be careful in decrypt

def aes_cbc_decrypt(encrypted_data_with_iv, key):
    # Assuming the IV was appended to the end
    iv = encrypted_data_with_iv[-16:]
    ciphertext = encrypted_data_with_iv[:-16]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# Setup
passphrase = "This is super secret".encode('utf-8')
key = sha256(passphrase)

# To match R's serialize(iris, NULL), we would need an R-compatible serializer.
# Since we cannot produce the exact binary of R's serialization in pure Python,
# we use a placeholder that simulates the data flow, but for the test to pass,
# the most critical part is that x2 == x.
import pickle
x = pickle.dumps(iris)

y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

assert x == x2