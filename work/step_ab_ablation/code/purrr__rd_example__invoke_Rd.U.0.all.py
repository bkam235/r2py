import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, args, **kwargs):
    if isinstance(args, dict):
        # Merge dict args with kwargs
        combined_args = {**args, **kwargs}
        return func(**combined_args)
    else:
        # If args is a list/tuple, treat as positional, then kwargs
        return func(*args, **kwargs)

# r2py:entity:exec
def exec_func(func, *args, **kwargs):
    return func(*args, **kwargs)

# r2py:entity:invoke_map
def invoke_map(funs, **kwargs):
    # In R, invoke_map applies the same args to a list of functions
    if isinstance(funs, dict):
        return {name: invoke(f, {}, **kwargs) for name, f in funs.items()}
    else:
        return [invoke(f, {}, **kwargs) for f in funs]

# Define R-like runif and rnorm wrappers to match expected argument names
def runif(n=1, **kwargs):
    return np.random.uniform(size=n, **kwargs)

def rnorm(n=1, **kwargs):
    return np.random.normal(size=n, **kwargs)

def paste(*args, sep=" ", **kwargs):
    # Handle case where first arg is a list (mimics R's list passing)
    if len(args) == 1 and isinstance(args[0], list):
        return sep.join(map(str, args[0]))
    return sep.join(map(str, args))

# invoke(runif, list(n = 10))
# r2py:entity:invoke
invoke(runif, {'n': 10})

# invoke(runif, n = 10)
# r2py:entity:invoke_1
invoke(runif, {}, n=10)

# exec(runif, n = 10)
# r2py:entity:exec
exec_func(runif, n=10)

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
invoke(paste, args, sep="-")

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
exec_func(paste, *args, sep="-")

# r2py:entity:funs
funs = [runif, rnorm]
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
invoke_map(funs, n=5)

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
args_list = [{'n': 10}, {'n': 5}]
[invoke(f, a) for f, a in zip(funs, args_list)]

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
data_cauchy = np.random.standard_cauchy(100)
# r2py:entity:invoke_map_2
# R: list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# In Python, np.mean doesn't take 'x' as keyword, it's first positional.
# We wrap it to accept x=...
def mean_wrapper(x=None, **kwargs): return np.mean(x)
def median_wrapper(x=None, **kwargs): return np.median(x)
funs_stats_wrapped = {"m1": mean_wrapper, "m2": median_wrapper}
invoke_map(funs_stats_wrapped, x=data_cauchy)

# r2py:entity:list_1
# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats.items()}