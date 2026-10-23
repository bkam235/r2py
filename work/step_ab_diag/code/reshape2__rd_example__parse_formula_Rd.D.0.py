import re

# R's built-in 'letters' constant
letters = list("abcdefghijklmnopqrstuvwxyz")

def parse_formula(formula="... ~ variable", varnames=None, value_var="value"):
    """
    Implementation of reshape2:::parse_formula.
    """
    def remove_placeholder(x):
        return [item for item in x if item != "."]

    def replace_remainder(x, remainder):
        if "..." in x:
            # Remove '...' and append the remainder
            return [item for item in x if item != "..."] + remainder
        return x

    # Convert formula to string if it isn't one
    if not isinstance(formula, str):
        formula = str(formula)

    # Split by '~'
    dims = formula.split('~')
    
    # Split each dimension by '+' or '*' and trim whitespace
    parsed_dims = []
    for dim in dims:
        parts = [p.strip() for p in re.split(r'[+*]', dim)]
        parsed_dims.append(parts)
        
    # Remove placeholders ('.')
    parsed_dims = [remove_placeholder(p) for p in parsed_dims]
    
    # Flatten to get all variables used in the formula
    all_vars = [var for sublist in parsed_dims for var in sublist]
    
    # If '...' is present, replace it with the variables in varnames 
    # that are not already in the formula and not the value_var
    if "..." in all_vars and varnames is not None:
        excluded = set(all_vars) | {value_var}
        remainder = [v for v in varnames if v not in excluded]
        parsed_dims = [replace_remainder(p, remainder) for p in parsed_dims]
    
    # R's parse_formula returns a list of lists.
    return parsed_dims

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__parse_formula_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__parse_formula_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# letters[1:6] in R is a 1-based slice, equivalent to letters[0:6] in Python
data_cols = letters[0:6]

# Translate calls
# r2py:entity:parse_formula
res1 = parse_formula("a + ...", data_cols)

# r2py:entity:parse_formula_1
res2 = parse_formula("a ~ b + d")

# r2py:entity:parse_formula_2
res3 = parse_formula("a + b ~ c ~ .")