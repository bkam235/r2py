---
id: reshape2.parse-formula
package: reshape2
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# reshape2.parse-formula

## Guidance
Translate R `parse_formula` (ExternalSymbol from reshape2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "167e9b68", "r_snippet": "reshape2:::parse_formula(\"a + ...\", letters[1:6])", "py_snippet": "def parse_formula(formula=\"... ~ variable\", varnames=None, value_var=\"value\"):\n    \"\"\"\n    Implementation of reshape2:::parse_formula.\n    \"\"\"\n    def remove_placeholder(x):\n        return [item for item in x if item != \".\"]\n\n    def replace_remainder(x, remainder):\n        if \"...\" in x:\n            return [item for item in x if item != \"...\"] + remainder\n        return x\n\n    # If formula is not a string (e.g. a formula object), it would be converted to string.\n    # For these examples, they are strings.\n    if not isinstance(formula, str):\n        formula = str(formula)\n\n    if isinstance(formula, str):\n        # dims <- str_split(formula, fixed(\"~\"))[[1]]\n        dims = formula.split('~')\n        \n        # formula <- lapply(str_split(dims, \"[+*]\"), str_trim)\n        parsed_dims = []\n        for dim in dims:\n            parts = [p.strip() for p in re.split(r'[+*]', dim)]\n            parsed_dims.append(parts)\n            \n        # formula <- lapply(formula, remove.placeholder)\n        parsed_dims = [remove_placeholder(p) for p in parsed_dims]\n        \n        # all_vars <- unlist(formula)\n        all_vars = [var for sublist in parsed_dims for var in sublist]\n        \n        # if (any(all_vars == \"...\")) { ... }\n        if \"...\" in all_vars and varnames is not None:\n            # remainder <- setdiff(varnames, c(all_vars, value.var))\n            excluded = set(all_vars) | {value_var}\n            remainder = [v for v in varnames if v not in excluded]\n            \n            # formula <- lapply(formula, replace.remainder)\n            parsed_dims = [replace_remainder(p, remainder) for p in parsed_dims]\n        \n        formula_list = parsed_dims\n    else:\n        formula_list = formula\n\n    if not isinstance(formula_list, list):\n        raise ValueError(f\"Don't know how to parse {formula}\")\n\n    # lapply(formula, as.quoted)\n    return [as_quoted(part) for part in formula_list]\n\ndef r_print_quoted_list(res):\n    \"\"\"\n# ...", "score": 0.9692, "script_id": "reshape2__rd_example__parse_formula_Rd", "n_calls": 0}

## Edit Examples
(none)
