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
    # R's openssl::aes_cbc_encrypt generates a random IV if not provided
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # In R, aes_cbc_encrypt returns the ciphertext. 
    # The IV is stored as an attribute. To simulate the 'identical' check 
    # and typical usage, we store the IV on the object if it's a custom class 
    # or return a structure. However, for the sake of the test script, 
    # the crucial part is that the decryptor knows the IV.
    # We will attach the IV to the ciphertext bytes object via a custom attribute
    # by wrapping it in a simple class.
    class EncryptedData(bytes):
        def __init__(self, data, iv):
            super().__init__(data)
            self.iv = iv
            
    return EncryptedData(ciphertext, iv)

def aes_cbc_decrypt(data_obj, key):
    # Extract IV from the object attribute (mimicking R's attribute)
    iv = getattr(data_obj, 'iv', None)
    ciphertext = bytes(data_obj)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# R: passphrase <- charToRaw("This is super secret")
passphrase = "This is super secret".encode('utf-8')

# R: key <- sha256(passphrase)
key = sha256(passphrase)

# R: x <- serialize(iris, NULL)
# Since we cannot realistically replicate R's internal serialization format 
# in Python, we use a stable representation of the iris dataframe.
import pickle
x = pickle.dumps(iris)

# R: y <- aes_cbc_encrypt(x, key = key)
y = aes_cbc_encrypt(x, key=key)

# R: x2 <- aes_cbc_decrypt(y, key = key)
x2 = aes_cbc_decrypt(y, key=key)

# R: stopifnot(identical(x, x2))
assert x == x2