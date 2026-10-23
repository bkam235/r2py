# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 19

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/purrr__rd_example__reduce_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__rd_example__reduce_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'x', 'y']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import random
import string
from typing import Any, Callable, List

class Done:
    """Helper to implement short-circuiting in reduce."""
    def __init__(self, value: Any):
        self.value = value

# r2py:entity:str
def str_r(obj, indent=""):
    """Simplified simulation of R's str() for nested lists."""
    if isinstance(obj, list):
        res = f"List of {len(obj)}\n"
        for i, item in enumerate(obj):
            prefix = f"{indent} $ " if i == 0 else f"{indent} $ " # R's str is complex
            # This is a very rough approximation of R's list str output
            if isinstance(item, list):
                res += f"{indent} $ : {str_r(item, indent + '  ..')}\n"
            else:
                res += f"{indent} $ : {type(item).__name__} {item}\n"
        return res.strip()
    return str(obj)

def r_print(val):
    """Simulates R's print output [1] value"""
    if isinstance(val, str):
        print(f'[1] "{val}"')
    else:
        print(f'[1] {val}')

# r2py:entity:reduce
def reduce_py(x: List, f: Callable, init: Any = None, dir_val: str = "forward", *args) -> Any:
    if not x:
        if init is None:
            raise ValueError("Must supply .init when .x is empty.")
        return init
    
    # In R, .dir = "backward" reduces from the end of the vector
    data = x[::-1] if dir_val == "backward" else x
    
    if init is not None:
        acc = init
        start_idx = 0
    else:
        acc = data[0]
        start_idx = 1
    
    for i in range(start_idx, len(data)):
        # For .dir = "backward", R flips the arguments to .f(next_elt, acc)
        if dir_val == "backward":
            res = f(data[i], acc, *args)
        else:
            res = f(acc, data[i], *args)
            
        if isinstance(res, Done):
            return res.value
        acc = res
    return acc

# r2py:entity:reduce2
def reduce2_py(x: List, y: List, f: Callable, init: Any = None, *args) -> Any:
    if init is not None:
        acc = init
        start_idx = 0
    else:
        acc = x[0]
        start_idx = 1
    
    for i in range(start_idx, len(x)):
        y_val = y[i - (1 if init is None else 0)]
        res = f(acc, x[i], y_val, *args)
        if isinstance(res, Done):
            return res.value
        acc = res
    return acc

# Reducing `+` computes the sum of a vector while reducing `*` computes the product:
# r2py:entity:reduce
r_print(reduce_py(list(range(1, 4)), lambda a, b: a + b))
# r2py:entity:reduce_1
r_print(reduce_py(list(range(1, 11)), lambda a, b: a * b))

# By ignoring the input vector (nxt), you can turn output of one step into
# the input for the next. This code takes 10 steps of a random walk:
# r2py:entity:reduce_2
r_print(reduce_py(list(range(1, 11)), lambda acc, nxt: acc + random.gauss(0, 1), init=0))

# When the operation is associative, the direction of reduction does not matter:
# r2py:entity:reduce_3
r_print(reduce_py(list(range(1, 5)), lambda a, b: a + b))
# r2py:entity:reduce_4
r_print(reduce_py(list(range(1, 5)), lambda a, b: a + b, dir_val="backward"))

# Non-associative operations: list()
# r2py:entity:str
print(str_r(reduce_py(list(range(1, 5)), lambda a, b: [a, b])))
# r2py:entity:str_1
print(str_r(reduce_py(list(range(1, 5)), lambda a, b: [a, b], dir_val="backward")))

# reduce2() takes a ternary function and a second vector
# r2py:entity:paste2
def paste2(x, y, sep="."):
    return f"{x}{sep}{y}"

# Use the letters provided by data shim
letters_list = letters
# r2py:entity:reduce_5
r_print(reduce_py(letters_list[0:4], paste2))
# r2py:entity:reduce2
r_print(reduce2_py(letters_list[0:4], ["-", ".", "-"], paste2))

# r2py:entity:x
x_vals = x
# r2py:entity:y
y_vals = y
# r2py:entity:reduce2_1
def paste_impl(acc, val_x, val_y):
    return f"{acc} {val_x} {val_y}"

# R's paste on lists converts to strings and joins with spaces
def paste_r_sim(acc, val_x, val_y):
    return f"{acc} {val_x} {val_y}"

r_print(reduce2_py(x_vals, y_vals, paste_r_sim))

# Short-circuiting
# r2py:entity:paste3
def paste3(out, input_val, sep="."):
    if len(str(out)) > 4:
        return Done(out)
    return f"{out}{sep}{input_val}"

# r2py:entity:reduce_6
r_print(reduce_py(letters_list, paste3))

# r2py:entity:paste4
def paste4(out, input_val, sep="."):
    if input_val == "j":
        return Done(out)
    return f"{out}{sep}{input_val}"

# r2py:entity:reduce_7
r_print(reduce_py(letters_list, paste4))