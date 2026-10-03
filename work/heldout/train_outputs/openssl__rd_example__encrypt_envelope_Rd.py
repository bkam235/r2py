# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/openssl__rd_example__encrypt_envelope_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'openssl__rd_example__encrypt_envelope_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import pickle
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# iris is provided by the shim.
# R's serialize(iris, NULL) produces a specific binary format.
# We use a byte representation to mimic the operation.
iris_df = pd.DataFrame(iris)

# key <- rsa_keygen()
# r2py:entity:key
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
# r2py:entity:pubkey
pubkey = key.public_key()

# msg <- serialize(iris, NULL)
# r2py:entity:msg
msg = pickle.dumps(iris_df)

# out <- encrypt_envelope(msg, pubkey)
# r2py:entity:out
session_key = os.urandom(32) 
iv = os.urandom(16)

cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
encryptor = cipher.encryptor()
pad_len = 16 - (len(msg) % 16)
padded_msg = msg + bytes([pad_len] * pad_len)
encrypted_data = encryptor.update(padded_msg) + encryptor.finalize()

# Encrypt the session key with RSA
encrypted_session = pubkey.encrypt(
    session_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

out = {
    'iv': iv,
    'session': encrypted_session,
    'data': encrypted_data
}

# str(out)
# r2py:entity:str
def r_str_list(obj):
    # R's str() for this structure:
    #      List of 3
    #  $ iv     : raw [1:16] 5a 1e ff a9 ...
    #  $ session: raw [1:256] 2b 28 c8 1a ...
    #  $ data   : raw [1:5808] 94 74 a1 33 ...
    res = "      List of 3\n"
    # R's order is iv, session, data
    for k in ['iv', 'session', 'data']:
        v = obj[k]
        # Hex values for the first 4 bytes
        hex_vals = ' '.join(f"{b:02x}" for b in v[:4])
        # The label is left-aligned in a field of 8 characters
        res += f" $ {k:<7}: raw [1:{len(v)}] {hex_vals} ...\n"
    return res.strip()

print(r_str_list(out))

# orig <- decrypt_envelope(out$data, out$iv, out$session, key)
# r2py:entity:orig
session_key_dec = key.decrypt(
    out['session'],
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

cipher_dec = Cipher(algorithms.AES(session_key_dec), modes.CBC(out['iv']))
decryptor = cipher_dec.decryptor()
decrypted_padded_msg = decryptor.update(out['data']) + decryptor.finalize()

# Remove PKCS7 padding
pad_len_dec = decrypted_padded_msg[-1]
orig = decrypted_padded_msg[:-pad_len_dec]

# stopifnot(identical(msg, orig))
# r2py:entity:stopifnot
assert msg == orig