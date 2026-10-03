---
id: base.ncol
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.ncol

## Guidance
Translate R `ncol` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "95aeda39", "r_snippet": "colnames(R1) <- rownames(R1) <- paste0(\"x\", 1:ncol(R1))", "py_snippet": "R1 = pd.DataFrame(R1_mat, index=[f\"x{i+1}\" for i in range(5)], columns=[f\"x{i+1}\" for i in range(5)])\n\n# To match R's print output exactly: no extra spaces in index/columns", "score": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "n_calls": 4}

## Edit Examples
- {"failure_class": "crash", "old_code": "R2 = pd.DataFrame(R2_data, index=[f\"x{i+1}\" for i in range(5)], columns=[f\"x{i+1}\" for i in range(5)])\n\n# Plotting levelplot", "new_code": "R1 = pd.DataFrame(R1_mat, index=[f\"x{i+1}\" for i in range(5)], columns=[f\"x{i+1}\" for i in range(5)])\n\n# To match R's print output exactly: no extra spaces in index/columns", "score_delta": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "r_snippet": "colnames(R1) <- rownames(R1) <- paste0(\"x\", 1:ncol(R1))", "functions": ["base::colnames", "base::rownames", "base::paste0", "base::ncol"]}
