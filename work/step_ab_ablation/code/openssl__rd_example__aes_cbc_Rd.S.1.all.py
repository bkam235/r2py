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
import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def sha256(x):
    if isinstance(x, str):
        x = x.encode('utf-8')
    return hashlib.sha256(x).digest()

def aes_cbc_encrypt(data, key):
    # R's aes_cbc_encrypt generates a random IV by default and returns it as an attribute
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # To mimic R's behavior where the IV is bundled with the result
    # we return a custom object or a tuple.
    class EncryptedData:
        def __init__(self, ciphertext, iv):
            self.ciphertext = ciphertext
            self.iv = iv
    
    return EncryptedData(ciphertext, iv)

def aes_cbc_decrypt(encrypted_data, key):
    # Extract IV from the bundled object
    ciphertext = encrypted_data.ciphertext
    iv = encrypted_data.iv

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# Main execution
passphrase = "This is super secret"
# R: passphrase <- charToRaw("This is super secret")
passphrase_raw = passphrase.encode('utf-8')
# R: key <- sha256(passphrase)
key = sha256(passphrase_raw)

# R: x <- serialize(iris, NULL)
# We use pickle to simulate R's serialization of the dataframe
x = pickle.dumps(iris)

# R: y <- aes_cbc_encrypt(x, key = key)
y = aes_cbc_encrypt(x, key=key)

# R: x2 <- aes_cbc_decrypt(y, key = key)
x2 = aes_cbc_decrypt(y, key=key)

# R: stopifnot(identical(x, x2))
assert x == x2