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

# Define the R constant 'letters'
letters = list(string.ascii_lowercase)

def as_quoted(x):
    """
    Mimics R's as.quoted. In R, as.quoted() returns a list of symbols.
    The R output shows these as named lists: $ a: symbol a.
    """
    # Returns a dictionary where keys are the variable names and values are the 'symbol' strings
    return {var: f"symbol {var}" for var in x}

# r2py:entity:parse_formula
def parse_formula(formula="... ~ variable", varnames=None, value_var="value"):
    """
    Implementation of reshape2:::parse_formula.
    """
    def remove_placeholder(x):
        return [item for item in x if item != "."]

    def replace_remainder(x, remainder):
        if "..." in x:
            # R's c(x[x != "..."], remainder)
            return [item for item in x if item != "..."] + remainder
        return x

    if not isinstance(formula, str):
        # This handles the case where formula might be a formula object (simplified to string)
        formula = str(formula)

    if isinstance(formula, str):
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
        
        formula_list = parsed_dims
    else:
        formula_list = formula

    if not isinstance(formula_list, list):
        raise ValueError(f"Don't know how to parse {formula}")

    # lapply(formula, as.quoted)
    return [as_quoted(part) for part in formula_list]

def r_print_quoted_list(res):
    """
    Helper to print the result in the format R's print.default(list) would.
    """
    for i, item in enumerate(res, 1):
        print(f"      [[{i}]]")
        if isinstance(item, dict):
            print(f"List of {len(item)}")
            for k, v in item.items():
                print(f" $ {k}: {v}")
            # Simplified representation of attributes
            print(f" - attr(*, \"env\")=<environment: 0x0000000000000000>") 
            print(f" - attr(*, \"class\")= chr \"quoted\"")
        else:
            print(" list()")
        print()

# letters[1:6] in R is letters[0:6] in Python
data_cols = letters[0:6]

# Translate calls
# r2py:entity:parse_formula
res1 = parse_formula("a + ...", data_cols)
r_print_quoted_list(res1)

# r2py:entity:parse_formula_1
res2 = parse_formula("a ~ b + d")
r_print_quoted_list(res2)

# r2py:entity:parse_formula_2
res3 = parse_formula("a + b ~ c ~ .")
r_print_quoted_list(res3)