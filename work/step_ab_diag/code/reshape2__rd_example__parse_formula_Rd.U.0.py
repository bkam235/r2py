import re
import string

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__parse_formula_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__parse_formula_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Define R's 'letters' constant
letters = list(string.ascii_lowercase)

def parse_formula(formula="... ~ variable", varnames=None, value_var="value"):
    """
    Implementation of reshape2:::parse_formula.
    """
    def remove_placeholder(x):
        return [item for item in x if item != "."]

    def replace_remainder(x, remainder):
        if "..." in x:
            # Replace "..." with the remainder list
            # The R code: if (any(all_vars == "...")) { ... } 
            # replaces the "..." element with the whole remainder vector
            res = []
            for item in x:
                if item == "...":
                    res.extend(remainder)
                else:
                    res.append(item)
            return res
        return x

    if not isinstance(formula, str):
        formula = str(formula)

    # Split by ~
    dims = formula.split('~')
    
    # Split by + or * and trim
    parsed_dims = []
    for dim in dims:
        parts = [p.strip() for p in re.split(r'[+*]', dim)]
        parsed_dims.append(parts)
        
    # Remove "." placeholders
    parsed_dims = [remove_placeholder(p) for p in parsed_dims]
    
    # Calculate all variables currently in the formula
    all_vars = [var for sublist in parsed_dims for var in sublist]
    
    # Handle "..." (the remainder)
    if "..." in all_vars and varnames is not None:
        # remainder <- setdiff(varnames, c(all_vars, value.var))
        excluded = set(all_vars) | {value_var}
        remainder = [v for v in varnames if v not in excluded]
        
        # Replace "..." with the remainder list in each dimension
        parsed_dims = [replace_remainder(p, remainder) for p in parsed_dims]
    
    # The R function returns a list of lists, where each inner list 
    # is marked with class "quoted". In Python, we return the list of lists.
    return parsed_dims

# Translate calls
# r2py:entity:parse_formula
res1 = parse_formula("a + ...", letters[0:6])

# r2py:entity:parse_formula_1
res2 = parse_formula("a ~ b + d")

# r2py:entity:parse_formula_2
res3 = parse_formula("a + b ~ c ~ .")