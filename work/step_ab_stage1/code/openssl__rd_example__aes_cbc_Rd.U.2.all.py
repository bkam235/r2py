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
    # R's openssl aes_cbc_encrypt generates a random IV and returns it as an attribute
    iv = os.urandom(16)
    
    # AES CBC requires padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # To mimic R's attribute, we return a tuple (ciphertext, iv)
    return (ciphertext, iv)

def aes_cbc_decrypt(encrypted_data, key):
    # If encrypted_data is a tuple, it contains (ciphertext, iv)
    if isinstance(encrypted_data, tuple):
        ciphertext, iv = encrypted_data
    else:
        # In a real R-to-Python scenario, the IV would be stored in the object metadata
        raise ValueError("IV is required for decryption")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# The R code uses serialize(iris, NULL) which produces a raw byte vector.
# Since we cannot perfectly replicate R's internal serialization in Python, 
# and the goal is to test encryption/decryption, we represent 'x' as the bytes 
# of the iris dataframe (e.g., via its string representation or pickle) 
# as long as x and x2 are compared for identity.
import pickle
x = pickle.dumps(iris)

passphrase = "This is super secret"
# R's charToRaw("...") creates a raw vector
passphrase_raw = passphrase.encode('utf-8')
key = sha256(passphrase_raw)

# symmetric encryption uses same key for decryption
y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2