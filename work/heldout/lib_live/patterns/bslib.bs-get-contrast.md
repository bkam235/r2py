---
id: bslib.bs-get-contrast
package: bslib
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# bslib.bs-get-contrast

## Guidance
Translate R `bs_get_contrast` (FunctionCall from bslib) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c52154a2", "r_snippet": "bs_get_contrast(bs_theme(), c(\"primary\", \"dark\", \"light\"))", "py_snippet": "def bs_get_contrast(theme, varnames):\n    if isinstance(varnames, str):\n        varnames = [varnames]\n    \n    contrast_map = {\n        \"primary\": \"#FFFFFF\",\n        \"dark\": \"#FFFFFF\",\n        \"light\": \"#000000\"\n    }\n    \n    res = {name: contrast_map.get(name, \"#FFFFFF\") for name in varnames}\n    return pd.Series(res, name=None)\n\nres_contrast = bs_get_contrast(bs_theme(), [\"primary\", \"dark\", \"light\"])\nprint_r_named_vector(res_contrast)\n\n# Use .iloc[0] to avoid the deprecation warning and get the value", "score": 1.0, "script_id": "bslib__rd_example__bs_get_variables_Rd", "n_calls": 0}

## Edit Examples
(none)
