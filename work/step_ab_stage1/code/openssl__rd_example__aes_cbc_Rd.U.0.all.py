import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import pandas as pd

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

def aes_cbc_encrypt(plaintext, key):
    # R's openssl::aes_cbc_encrypt uses a random IV and prepends/attaches it.
    # To match identical(x, x2), we just need consistency.
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return IV + ciphertext to allow decryption without separate IV tracking
    return iv + ciphertext

def aes_cbc_decrypt(ciphertext_with_iv, key):
    iv = ciphertext_with_iv[:16]
    ciphertext = ciphertext_with_iv[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

# aes-256 requires 32 byte key
passphrase = "This is super secret"
key = sha256(passphrase)

# R's serialize(iris, NULL) produces a specific byte stream.
# We simulate this by converting the dataframe to bytes.
# The core of the test is whether encrypt -> decrypt returns the same bytes.
x = pd.DataFrame(iris).to_csv(index=False).encode('utf-8')

y = aes_cbc_encrypt(x, key=key)
x2 = aes_cbc_decrypt(y, key=key)

assert x == x2