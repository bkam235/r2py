import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, args_val=None, **kwargs):
    if isinstance(args_val, dict):
        return func(**args_val, **kwargs)
    return func(**kwargs)

# r2py:entity:exec
def exec_func(func, *args, **kwargs):
    return func(*args, **kwargs)

# r2py:entity:invoke_map
def invoke_map(funs_dict, **kwargs):
    return {name: invoke(f, **kwargs) for name, f in funs_dict.items()}

# Define R-like random functions for consistency
def runif(n=1, **kwargs):
    return np.random.uniform(low=0, high=1, size=n)

def rnorm(n=1, **kwargs):
    return np.random.normal(loc=0, scale=1, size=n)

def rcauchy(n=1, **kwargs):
    return np.random.standard_cauchy(size=n)

def paste(*args, sep=" ", **kwargs):
    # Filter out None/empty and convert to string
    return sep.join(str(x) for x in args if x is not None)

# invoke(runif, list(n = 10))
# r2py:entity:invoke
invoke(runif, args_val={'n': 10})

# invoke(runif, n = 10)
# r2py:entity:invoke_1
invoke(runif, n=10)

# exec(runif, n = 10)
# r2py:entity:exec
exec_func(runif, n=10)

# r2py:entity:args
args = ["01a", "01b"]

# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
# In R, invoke(paste, args, ...) passes args as the first argument
invoke(paste, args_val=args, sep="-") if isinstance(args, dict) else paste(args, sep="-")
# To match the R logic of invoke(paste, args, sep="-") where args is a list:
# we actually need to pass the list as the first arg to paste.
# But purrr::invoke handles the list by unpacking if it's the first arg? 
# No, invoke(f, list(a=1)) calls f(a=1). invoke(f, x) calls f(x).
# Since args is a list, invoke(paste, args, sep="-") calls paste(args, sep="-")
# We'll use a helper to match that specific behavior:
def invoke_paste_shim(func, val, **kwargs):
    return func(val, **kwargs)

invoke_paste_shim(paste, args, sep="-")

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
exec_func(paste, *args, sep="-")

# r2py:entity:funs
funs = [runif, rnorm]

# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
[invoke(f, n=5) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
args_list = [{'n': 10}, {'n': 5}]
[f(**a) for f, a in zip(funs, args_list)]

# funs |> map(exec, n = 5)
# r2py:entity:map
[exec_func(f, n=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
[exec_func(f, **a) for f, a in zip(funs, args_list)]

# r2py:entity:df
df = pd.DataFrame({
    'fun': [runif, rnorm],
    'args': [{'n': 10}, {'n': 5}]
})

# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
df.apply(lambda row: exec_func(row['fun'], **row['args']), axis=1).tolist()

# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = rcauchy(100)

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:invoke_map_2
# np.mean/median use 'a' as the first positional arg
invoke_map(funs_stats, a=data_cauchy)

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats.items()}