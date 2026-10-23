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
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def sha256(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).digest()

def aes_cbc_encrypt(data, key):
    # R openssl aes_cbc_encrypt generates a random IV and stores it as an attribute.
    # To be execution-equivalent in Python, we must store the IV to allow decryption.
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # We attach the IV to the result object to mimic R's attribute behavior
    # Since Python bytes don't have attributes, we use a simple class.
    class EncryptedData(bytes):
        pass
    
    result = EncryptedData(ciphertext)
    result.iv = iv
    return result

def aes_cbc_decrypt(data, key):
    # If data is our EncryptedData object, use its iv attribute.
    iv = getattr(data, 'iv', None)
    if iv is None:
        raise ValueError("IV not found in encrypted data")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data_unpadded = unpadder.update(padded_data) + unpadder.finalize()
    return data_unpadded

# Main execution
passphrase = "This is super secret".encode('utf-8')
key = sha256(passphrase)

# R's serialize(iris, NULL) creates a binary representation. 
# In Python, we use pickle to get a binary representation of the dataframe.
x = pickle.dumps(iris)
y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2