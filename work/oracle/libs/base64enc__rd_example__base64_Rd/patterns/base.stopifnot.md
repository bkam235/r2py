---
id: base.stopifnot
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.stopifnot

## Guidance
Translate R `stopifnot` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "07aed11d", "r_snippet": "stopifnot(div < z)", "py_snippet": "mod = z % y", "score": 1.0, "script_id": "openssl__vignette__bignum_s2.R", "n_calls": 1}
- {"r_hash": "e7e688e8", "r_snippet": "stopifnot(identical(msg, orig))", "py_snippet": "# Remove PKCS7 padding", "score": 1.0, "script_id": "openssl__rd_example__encrypt_envelope_Rd.R", "n_calls": 2}

## Edit Examples
(none)
