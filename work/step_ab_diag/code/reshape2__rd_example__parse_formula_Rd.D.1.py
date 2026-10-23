# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__parse_formula_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__parse_formula_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re
import string

# Define R's built-in letters constant
letters = list(string.ascii_lowercase)

# r2py:entity:parse_formula
def parse_formula(formula="... ~ variable", varnames=None, value_var="value"):
    """
    Implementation of reshape2:::parse_formula.
    """
    def remove_placeholder(x):
        return [item for item in x if item != "."]

    def replace_remainder(x, remainder):
        if "..." in x:
            # Find position of ... and replace it with the remainder list
            res = []
            for item in x:
                if item == "...":
                    res.extend(remainder)
                else:
                    res.append(item)
            return res
        return x

    if not isinstance(formula, str):
        formula_str = str(formula)
    else:
        formula_str = formula

    # dims <- str_split(formula, fixed("~"))[[1]]
    dims = formula_str.split('~')
    
    # formula <- lapply(str_split(dims, "[+*]"), str_trim)
    parsed_dims = []
    for dim in dims:
        parts = [p.strip() for p in re.split(r'[+*]', dim)]
        parsed_dims.append(parts)
        
    # formula <- lapply(formula, remove.placeholder)
    parsed_dims = [remove_placeholder(p) for p in parsed_dims]
    
    # all_vars <- unlist(formula)
    all_vars = [var for sublist in parsed_dims for var in sublist]
    
    # if (any(all_vars == "...")) { ... }
    if "..." in all_vars and varnames is not None:
        # remainder <- setdiff(varnames, c(all_vars, value.var))
        excluded = set(all_vars) | {value_var}
        remainder = [v for v in varnames if v not in excluded]
        
        # formula <- lapply(formula, replace.remainder)
        parsed_dims = [replace_remainder(p, remainder) for p in parsed_dims]
    
    # In R, parse_formula returns a list of lists of 'quoted' objects.
    # We represent this as a list of lists of strings.
    return parsed_dims

# letters[1:6] from shim (translated to 0-indexed)
data_cols = letters[0:6]

# Translate calls
# r2py:entity:parse_formula
res1 = parse_formula("a + ...", data_cols)
print(res1)

# r2py:entity:parse_formula_1
res2 = parse_formula("a ~ b + d")
print(res2)

# r2py:entity:parse_formula_2
res3 = parse_formula("a + b ~ c ~ .")
print(res3)