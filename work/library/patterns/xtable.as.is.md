---
id: xtable.as.is
package: xtable
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# xtable.as.is

## Guidance
Translate R `as.is` (FunctionCall from xtable) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "565f96f0", "r_snippet": "as.is(insane)", "py_snippet": "def as_is(str_val):\n    return str_val\n\nres_asis = as_is(insane_1)\nr_print_named(res_asis, insane_1_names)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "f0d94563", "r_snippet": "print.xtableList(xList)", "py_snippet": "def print_xtableList(x, type=\"latex\", colnames_format=\"single\", booktabs=False, include_rownames=True, include_colnames=True):\n    \"\"\"Mimics the LaTeX output of print.xtableList.\"\"\"\n    if not x[\"items\"]:\n        return\n\n    # Check the first dataframe to determine column count\n    first_df = x[\"items\"][0][\"data\"]\n    n_cols = len(first_df.columns)\n    total_cols = n_cols + (1 if include_rownames else 0)\n    \n    m_rule = \"\\\\midrule\" if booktabs else \"\\\\hline\"\n    t_rule = \"\\\\toprule\" if booktabs else \"\\\\hline\"\n    b_rule = \"\\\\bottomrule\" if booktabs else \"\\\\hline\"\n    \n    output = []\n    out", "score": 0.8976, "script_id": "auto"}

## Edit Examples
(none)
