---
id: openssl.rsa-decrypt
package: openssl
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# openssl.rsa-decrypt

## Guidance
Translate R `rsa_decrypt` (FunctionCall from openssl) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "28834e70", "r_snippet": "tempkey <- rsa_decrypt(ciphertext, key)", "py_snippet": "tempkey = key.decrypt(\n    ciphertext,\n    padding.PKCS1v15()\n)\n\n# message <- aes_cbc_decrypt(blob, tempkey, iv)", "score": 1.0, "script_id": "openssl__rd_example__rsa_encrypt_Rd", "n_calls": 0}

## Edit Examples
(none)
