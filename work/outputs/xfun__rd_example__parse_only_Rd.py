import pandas as pd
import numpy as np
import ast

# r2py:entity:parse_only
def parse_only(code):
    """
    R's parse_only converts a character vector to an expression object.
    Logic:
    if (length(code) == 0) return(expression())
    parse(text = code, keep.source = FALSE)
    """
    if isinstance(code, (list, np.ndarray)) or (hasattr(code, '__iter__') and not isinstance(code, str)):
        if len(code) == 0:
            return "expression()"
        
        # R's parse() removes comments and parses the code.
        # We simulate the 'expression(expr1, expr2)' string representation.
        parsed_parts = []
        for item in code:
            # Remove R comments (starting with #)
            clean_item = item.split('#')[0].strip()
            # In R, 'y~x' is a formula. In Python, we can't parse it with ast.
            # We keep the expression as a string to mimic the R output representation.
            parsed_parts.append(clean_item)
        
        return f"expression({', '.join(parsed_parts)})"
    
    if not code:
        return "expression()"
    
    # Handle single string input
    clean_code = code.split('#')[0].strip()
    return f"expression({clean_code})"

# To mimic R's auto-printing behavior in a script
def print_result(res):
    print(res)

# Translate calls
# r2py:entity:parse_only
res_0 = parse_only("1+1")
print_result(res_0)

# r2py:entity:parse_only_1
res_1 = parse_only(["y~x", "1:5 # a comment"])
print_result(res_1)

# r2py:entity:parse_only_2
res_2 = parse_only([])
print_result(res_2)