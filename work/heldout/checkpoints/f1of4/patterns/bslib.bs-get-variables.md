---
id: bslib.bs-get-variables
package: bslib
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# bslib.bs-get-variables

## Guidance
Translate R `bs_get_variables` (FunctionCall from bslib) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "eaa5c03a", "r_snippet": "bs_get_variables(bs_theme(), varnames = vars)", "py_snippet": "class BSTheme:\n    def __init__(self, bootswatch=None):\n        self.bootswatch = bootswatch\n        if bootswatch == \"darkly\":\n            self.vars = {\n                \"body-bg\": \"#222\",\n                \"body-color\": \"#fff\",\n                \"primary\": \"#375a7f\",\n                \"border-radius\": \"0.375rem\"\n            }\n        else: # default\n            self.vars = {\n                \"body-bg\": \"#ffffff\",\n                \"body-color\": \"#1D1F21\",\n                \"primary\": \"#007bc2\",\n                \"border-radius\": \"3px\"\n            }\n\ndef bs_theme(bootswatch=None):\n    return BSTheme(bootswatch=bootswatch)\n\ndef bs_get_variables(theme, varnames):\n    # R's bs_get_variables returns a named character vector\n    res = {name: theme.vars.get(name, np.nan) for name in varnames}\n    return pd.Series(res, name=None)\n\nres_vars = bs_get_variables(bs_theme(), varnames=vars)\nprint_r_named_vector(res_vars)", "score": 1.0, "script_id": "bslib__rd_example__bs_get_variables_Rd", "n_calls": 0}

## Edit Examples
(none)
