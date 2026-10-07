---
id: base.unlink
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.unlink

## Guidance
Translate R `unlink` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "54857e19", "r_snippet": "unlink(svm_file)", "py_snippet": "pd.options.display.float_format = '{:.6f}'.format\n# Since V2 has 7 decimals and V1 has 6, we can't use a global float_format for both.", "score": 1.0, "script_id": "e1071__rd_example__write_svm_Rd.R", "n_calls": 1}
- {"r_hash": "defc49a9", "r_snippet": "unlink(scale_file)", "py_snippet": "# We'll manually format the print output to match the R verification string.\nprint(scaling_df.to_string(formatters={'V1': '{: .6f}'.format, 'V2': '{: .7f}'.format}))", "score": 1.0, "script_id": "e1071__rd_example__write_svm_Rd.R", "n_calls": 1}

## Edit Examples
(none)
