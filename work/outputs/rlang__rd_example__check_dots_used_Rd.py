# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import warnings

def check_dots_used(*args, **kwargs):
    if not args and not kwargs:
        raise TypeError("no arguments passed to function")

def check_dots_empty(*args, **kwargs):
    if args or kwargs:
        # The R code passes a custom error function that calls warning()
        # In Python, we simulate this by issuing a warning
        warnings.warn("arguments passed to function that expects none")

# r2py:entity:g
def g(x, y, *args, **kwargs):
    return x + y

# r2py:entity:f
def f(*args, **kwargs):
    check_dots_used(*args, **kwargs)
    # Since g takes specific named arguments and a dots object, 
    # we pass the kwargs and args directly
    return g(*args, **kwargs)

# f(x = 1, y = 2)
# r2py:entity:f_1
print(f(x=1, y=2))

# try(f(x = 1, y = 2, z = 3))
# r2py:entity:try
try:
    print(f(x=1, y=2, z=3))
except Exception as e:
    print(e)

# try(f(x = 1, y = 2, 3, 4, 5))
# r2py:entity:try_1
try:
    print(f(3, 4, 5, x=1, y=2))
except Exception as e:
    print(e)

# r2py:entity:fn
def fn(*args, **kwargs):
    check_dots_empty(*args, **kwargs)
    return "out"

# fn()
# r2py:entity:fn_1
print(fn())