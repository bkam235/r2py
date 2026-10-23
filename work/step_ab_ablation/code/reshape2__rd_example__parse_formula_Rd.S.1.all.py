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

# r2py:entity:parse_formula
def parse_formula(formula="... ~ variable", varnames=None, value_var="value"):
    """
    Implementation of reshape2:::parse_formula.
    """
    def remove_placeholder(x):
        return [item for item in x if item != "."]

    def replace_remainder(x, remainder):
        if "..." in x:
            # Remove '...' and add the remainder variables
            return [item for item in x if item != "..."] + remainder
        return x

    if not isinstance(formula, str):
        formula = str(formula)

    # dims <- str_split(formula, fixed("~"))[[1]]
    dims = formula.split('~')
    
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
    
    # In R, this returns a list of lists where each element is of class 'quoted'.
    # In Python, we return a list of lists of strings.
    return parsed_dims

# letters[1:6] from shim
data_cols = letters[0:6]

# Translate calls
# r2py:entity:parse_formula
parse_formula_res1 = parse_formula("a + ...", data_cols)

# r2py:entity:parse_formula_1
parse_formula_res2 = parse_formula("a ~ b + d")

# r2py:entity:parse_formula_2
parse_formula_res3 = parse_formula("a + b ~ c ~ .")