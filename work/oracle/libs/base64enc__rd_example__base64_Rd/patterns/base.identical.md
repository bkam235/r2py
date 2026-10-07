---
id: base.identical
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.identical

## Guidance
Translate R `identical` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d01fe70c", "r_snippet": "identical(preds.rfo[, , -c(1, 3, 5)], y = preds.dfo)", "py_snippet": "preds_dfo = np.array([tree.predict_proba(X_values) for tree in dfo.model.estimators_])\n\n# identical(preds.rfo[, , -c(1, 3, 5)], y = preds.dfo)\nmask = np.ones(len(rfo.model.estimators_), dtype=bool)\nmask[[0, 2, 4]] = False", "score": 1.0, "script_id": "ranger__rd_example__deforest_Rd.R", "n_calls": 1}
- {"r_hash": "e7e688e8", "r_snippet": "stopifnot(identical(msg, orig))", "py_snippet": "# Remove PKCS7 padding", "score": 1.0, "script_id": "openssl__rd_example__encrypt_envelope_Rd.R", "n_calls": 2}

## Edit Examples
(none)
