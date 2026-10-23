import hashlib
import pickle
import os
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
    # Generate a random IV
    iv = os.urandom(16)
    
    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # In R's openssl, the IV is stored as an attribute. 
    # To simulate this in Python, we can store it in a custom object or a tuple.
    class EncryptedData:
        def __init__(self, ciphertext, iv):
            self.ciphertext = ciphertext
            self.iv = iv
        def __bytes__(self):
            return self.ciphertext

    return EncryptedData(ciphertext, iv)

def aes_cbc_decrypt(encrypted_obj, key):
    # Extract IV and ciphertext from the object
    iv = encrypted_obj.iv
    ciphertext = encrypted_obj.ciphertext
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# aes-256 requires 32 byte key
passphrase = "This is super secret"
# Convert string to raw bytes equivalent to charToRaw
passphrase_bytes = passphrase.encode('utf-8')
key = sha256(passphrase_bytes)

# symmetric encryption uses same key for decryption
# x <- serialize(iris, NULL)
x = pickle.dumps(iris)
# y <- aes_cbc_encrypt(x, key = key)
y = aes_cbc_encrypt(x, key=key)
# x2 <- aes_cbc_decrypt(y, key = key)
x2 = aes_cbc_decrypt(y, key=key)

# stopifnot(identical(x, x2))
assert x == x2