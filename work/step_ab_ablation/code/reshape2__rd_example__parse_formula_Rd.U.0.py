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

# Define R's 'letters' constant
letters = list(string.ascii_lowercase)

def parse_formula(formula="... ~ variable", varnames=None, value_var="value"):
    """
    Implementation of reshape2:::parse_formula.
    This function parses a formula string into a list of lists of variables.
    """
    if not isinstance(formula, str):
        formula = str(formula)

    # split by ~
    dims = formula.split('~')
    
    # split by + or * and trim
    parsed_dims = []
    for dim in dims:
        parts = [p.strip() for p in re.split(r'[+*]', dim) if p.strip()]
        parsed_dims.append(parts)
        
    # remove '.' placeholders
    parsed_dims = [[item for item in p if item != "."] for p in parsed_dims]
    
    # Handle '...' ellipsis
    all_vars = [var for sublist in parsed_dims for var in sublist]
    if "..." in all_vars and varnames is not None:
        # remainder <- setdiff(varnames, c(all_vars, value.var))
        excluded = set(all_vars) | {value_var}
        remainder = [v for v in varnames if v not in excluded]
        
        # replace '...' with the remainder variables
        new_parsed_dims = []
        for p in parsed_dims:
            new_p = []
            for item in p:
                if item == "...":
                    new_p.extend(remainder)
                else:
                    new_p.append(item)
            new_parsed_dims.append(new_p)
        parsed_dims = new_parsed_dims

    # R's parse_formula returns a list where each element is 'quoted'
    # In Python, we represent the result as a list of lists of symbols.
    return parsed_dims

# Translate calls
# r2py:entity:parse_formula
res1 = parse_formula("a + ...", letters[0:6])
print(res1)

# r2py:entity:parse_formula_1
res2 = parse_formula("a ~ b + d")
print(res2)

# r2py:entity:parse_formula_2
res3 = parse_formula("a + b ~ c ~ .")
print(res3)