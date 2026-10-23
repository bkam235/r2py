# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dbplyr__rd_example__sql_expr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dbplyr__rd_example__sql_expr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:con
def simulate_dbi():
    """Simulates a DBI connection object."""
    return {"type": "TestConnection"}

# r2py:entity:x
def ident(name):
    """Mimics the ident function by wrapping a string as an identifier."""
    return {"type": "ident", "value": name}

def is_infix_base(fun):
    return fun in {"+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="}

def is_infix_user(fun):
    # R's %as% and %::% are infix operators. In this mock, they start/end with %
    return fun.startswith("%") and fun.endswith("%")

# r2py:entity:sql_expr
def replace_expr(x, con=None):
    if x is None:
        return "NULL"
    
    # Handle ident object
    if isinstance(x, dict) and x.get("type") == "ident":
        return f"`{x['value']}`"
    
    # Handle atomic types (strings, numbers)
    if isinstance(x, (str, int, float)):
        if isinstance(x, float) or (isinstance(x, int) and False): # Simplified
            return str(float(x))
        if isinstance(x, int):
            # In dbplyr, constants are often cast to floats in SQL
            return f"{float(x)}"
        return f"'{x}'" if isinstance(x, str) and not x.startswith("`") else str(x)

    # Handle "calls" (simulated as tuples or nested structures)
    if isinstance(x, tuple):
        fun_name = x[0]
        fun_upper = fun_name.upper() if isinstance(fun_name, str) else str(fun_name).upper()
        
        args = [replace_expr(arg, con=con) for arg in x[1:]]
        
        if is_infix_base(fun_upper):
            if len(args) == 1:
                return f"{fun_upper}{args[0]}"
            else:
                return f"{args[0]} {fun_upper} {args[1]}"
        
        if is_infix_user(fun_upper):
            # Strip % from both ends
            clean_fun = fun_upper[1:-1]
            return f"{args[0]} {clean_fun} {args[1]}"
        
        if fun_upper == "(":
            return f"({', '.join(args)})"
        
        # Standard function call
        return f"{fun_upper}({', '.join(args)})"

    return str(x)

def sql(x):
    """Simulates the sql() function which adds the <SQL> prefix."""
    return f"<SQL> {x}"

def sql_expr(expr_tuple, con=None):
    """
    Translates a mock expression (tuple) into a SQL string.
    """
    res = replace_expr(expr_tuple, con=con)
    return sql(res)

# r2py:entity:sql_call2
def sql_call2(fn, *args, con=None):
    """Mimics sql_call2 which constructs a SQL call."""
    expr_tuple = (fn, *args)
    res = replace_expr(expr_tuple, con=con)
    return sql(res)

# Helper for R's %as% and %::%
# r2py:entity:sql_expr_4
def as_op(x, y):
    return ("%as%", x, y)

def cast_op(x, y):
    return ("%as%", x, y)

# r2py:entity:sql_expr_5
def double_colon_op(x, y):
    return ("%::%", x, y)

# Main execution
# r2py:entity:con
con = simulate_dbi()

# sql_expr(f(x + 1), con = con)
# We represent f(x + 1) as a tuple: ('f', ('+', 'x', 1))
# r2py:entity:sql_expr
print(sql_expr(('f', ('+', 'x', 1)), con=con))

# sql_expr(f("x", "y"), con = con)
# r2py:entity:sql_expr_1
print(sql_expr(('f', 'x', 'y'), con=con))

# sql_expr(f(x, y), con = con)
# r2py:entity:sql_expr_2
print(sql_expr(('f', 'x', 'y'), con=con))

# x <- ident("x")
# r2py:entity:x
x_ident = ident("x")
# sql_expr(f(!!x, y), con = con)
# r2py:entity:sql_expr_3
print(sql_expr(('f', x_ident, 'y'), con=con))

# sql_expr(cast("x" %as% DECIMAL), con = con)
# CAST is a function in R, and %as% is an operator
# R: cast("x" %as% DECIMAL) -> cast( ("%as%", "x", "DECIMAL") )
# r2py:entity:sql_expr_4
print(sql_expr(('cast', ('%as%', 'x', 'DECIMAL')), con=con))

# sql_expr(round(x) %::% numeric, con = con)
# R: round(x) %::% numeric -> ("%::%", ('round', 'x'), 'numeric')
# r2py:entity:sql_expr_5
print(sql_expr(('%::%', ('round', 'x'), 'numeric'), con=con))

# sql_call2("+", quote(x), 1, con = con)
# quote(x) just passes the name 'x'
# r2py:entity:sql_call2
print(sql_call2("+", 'x', 1, con=con))

# sql_call2("+", "x", 1, con = con)
# In this case, "x" is a string literal
# r2py:entity:sql_call2_1
print(sql_call2("+", '"x"', 1, con=con))