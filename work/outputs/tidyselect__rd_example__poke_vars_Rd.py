# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/tidyselect__rd_example__poke_vars_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyselect__rd_example__poke_vars_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import string
from contextlib import contextmanager

# Simulate the global variable environment for tidyselect
vars_env = {"selected": None}

def vars_validate(vars_val):
    if vars_val is not None and not isinstance(vars_val, (list, tuple)):
        raise TypeError("`vars` must be a character vector")
    return list(vars_val) if vars_val is not None else None

# r2py:entity:poke_vars
def poke_vars(vars_val):
    if vars_val is not None:
        vars_val = vars_validate(vars_val)
    old = vars_env["selected"]
    vars_env["selected"] = vars_val
    return old

# r2py:entity:peek_vars
def peek_vars(fn_name=None):
    x = vars_env["selected"]
    if x is None:
        name = f"`{fn_name}()`" if fn_name else "Selection helpers"
        raise RuntimeError(f"{name} must be used within a *selecting* function.")
    return x

# r2py:entity:all_of
def all_of(x):
    vars_val = peek_vars(fn_name="all_of")
    # R's all_of returns indices (1-based).
    if isinstance(x, str):
        x = [x]
    
    indices = []
    for item in x:
        try:
            indices.append(vars_val.index(item) + 1)
        except ValueError:
            raise IndexError(f"Column {item} not found in variables")
    return indices

# r2py:entity:fn_3
def starts_with(match, ignore_case=True):
    vars_val = peek_vars(fn_name="starts_with")
    if isinstance(match, str):
        match = [match]
    
    indices = []
    for m in match:
        for i, v in enumerate(vars_val):
            v_check = v.lower() if ignore_case else v
            m_check = m.lower() if ignore_case else m
            if v_check.startswith(m_check):
                indices.append(i + 1)
    return indices

@contextmanager
# r2py:entity:fn_3
def scoped_vars(vars_val):
    old = poke_vars(vars_val)
    try:
        yield
    finally:
        poke_vars(old)

# r2py:entity:fn_5
def with_vars(vars_val, expr_fn):
    with scoped_vars(vars_val):
        return expr_fn()

# --- Main script translation ---

# r2py:entity:poke_vars
poke_vars(letters)
# r2py:entity:peek_vars
print(peek_vars())

# Now that the variables are registered, the helpers can figure out
# the locations of elements within the variable vector:
# r2py:entity:all_of
print(all_of(["d", "z"]))

# In a function be sure to restore the previous variables.
# r2py:entity:fn
def fn_custom(vars_val):
    old = poke_vars(vars_val)
    try:
        return all_of("d")
    finally:
        poke_vars(old)

# r2py:entity:fn_1
print(fn_custom(letters))
# letters[3:5] in R is indices 3, 4, 5 (1-based).
# In Python, letters[2:5] gives a list of 3 elements.
# r2py:entity:fn_2
print(fn_custom(letters[2:5]))

# The previous variables are still registered after fn() was
# called:
# r2py:entity:peek_vars_1
print(peek_vars())


# It is recommended to use the scoped variant as it restores the
# state automatically when the function returns:
# r2py:entity:fn_3
def fn_scoped(vars_val):
    with scoped_vars(vars_val):
        return starts_with("r")
# r2py:entity:fn_4
print(fn_scoped(["red", "blue", "rose"]))

# The with_vars() helper makes it easy to pass an expression that
# should be evaluated in a variable context.
# r2py:entity:fn_5
def fn_with(expr_fn):
    vars_list = ["red", "blue", "rose"]
    return with_vars(vars_list, expr_fn)
# r2py:entity:fn_6
print(fn_with(lambda: starts_with("r")))