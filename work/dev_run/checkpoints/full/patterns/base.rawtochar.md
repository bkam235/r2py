---
id: base.rawtochar
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.rawtochar

## Guidance
Translate R `rawToChar` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f27a2676", "r_snippet": "out <- rawToChar(message)", "py_snippet": "pad_len = message[-1]\nout = message[:-pad_len].decode('utf-8')", "score": 1.0, "script_id": "openssl__rd_example__rsa_encrypt_Rd", "n_calls": 1}

## Edit Examples
(none)
