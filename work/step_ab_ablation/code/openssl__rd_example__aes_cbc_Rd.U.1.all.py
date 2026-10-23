import hashlib
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/openssl__rd_example__aes_cbc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'openssl__rd_example__aes_cbc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def sha256(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).digest()

def aes_cbc_encrypt(data, key):
    # R openssl's aes_cbc_encrypt generates a random IV and returns the ciphertext
    # The IV is stored as an attribute of the returned object in R.
    # To mimic this in Python for the sake of the x == x2 check:
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # In R, the object returned is the ciphertext bytes, with IV as an attribute.
    # We store the IV on the bytes object to mimic R's attribute behavior.
    setattr(ciphertext, 'iv', iv)
    return ciphertext

def aes_cbc_decrypt(ciphertext, key):
    # Retrieve IV from the attribute
    iv = getattr(ciphertext, 'iv', None)
    if iv is None:
        raise ValueError("IV attribute missing from ciphertext")
        
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# aes-256 requires 32 byte key
passphrase = "This is super secret"
key = sha256(passphrase)

# symmetric encryption uses same key for decryption
# R's serialize(iris, NULL) produces a specific binary format. 
# For the purpose of this test, the exact bytes of 'x' must be consistent.
# Since we cannot truly replicate R's serialize in Python, 
# we use the representation of the dataframe provided by the shim.
import pickle
x = pickle.dumps(iris)

y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2