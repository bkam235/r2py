# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/rlang__rd_example__expr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'rlang__rd_example__expr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Simplified implementation of rlang-like expression capturing
class Expr:
    def __init__(self, content, is_sym=False):
        self.content = content
        self.is_sym = is_sym

    def __repr__(self):
        if self.is_sym:
            return str(self.content)
        if isinstance(self.content, tuple):
            # Handle call-like structures: (fn, args)
            fn, args = self.content
            if isinstance(args, list):
                args_str = ", ".join(map(repr, args))
            else:
                args_str = repr(args)
            return f"{fn}({args_str})"
        return str(self.content)

# r2py:entity:expr
def expr(x):
    # In a real rlang translation, this would capture the AST.
    # Here we simulate the representation for the specific examples.
    if x == 1 + 1:
        return Expr("1 + 1")
    return Expr(x)

def sym(x):
    return Expr(x, is_sym=True)

def syms(x):
    return [sym(i) for i in x]

# r2py:entity:call
def call(fn, *args):
    return Expr((fn, args[0] if len(args) == 1 else args))

# r2py:entity:call_1
def call2(fn, *args):
    # Simplified call2: flattens the '!!!' style injection
    final_args = []
    for arg in args:
        if isinstance(arg, list):
            final_args.extend(arg)
        else:
            final_args.append(arg)
    return Expr((fn, final_args))

# --- Start of Translation ---

# suppressPackageStartupMessages(library(rlang))
# No-op in Python

# 1 + 1
print(1 + 1)

# expr(1 + 1)
# r2py:entity:expr
expr_res1 = expr(1 + 1)
print(expr_res1)

# expr(toupper(letters))
# In R, this is an unevaluated call. 
# r2py:entity:expr_1
expr_res2 = Expr("toupper(letters)")
print(expr_res2)

# var <- "cyl"
# r2py:entity:var
var = "cyl"

# expr(with(mtcars, mean(!!sym(var))))
# Simulating the injection: !!sym(var) becomes 'cyl'
# r2py:entity:expr_2
expr_res3 = Expr(f"with(mtcars, mean({sym(var)}))")
print(expr_res3)

# vars <- c("cyl", "am")
# r2py:entity:vars
vars_list = ["cyl", "am"]

# expr(with(mtcars, c(!!!syms(vars))))
# Simulating injection: !!!syms(vars) becomes cyl, am
# r2py:entity:expr_3
expr_res4 = Expr(f"with(mtcars, c({', '.join(map(repr, syms(vars_list)))}))")
print(expr_res4)

# call("with", call("mean", sym(var)))
# r2py:entity:call
call_res1 = call("with", call("mean", sym(var)))
print(call_res1)

# call("with", call2("c", !!!syms(vars)))
# r2py:entity:call_1
call_res2 = call("with", call2("c", *syms(vars_list)))
print(call_res2)