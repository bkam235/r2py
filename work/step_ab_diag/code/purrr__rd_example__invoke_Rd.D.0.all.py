import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, args_or_kwargs=None, **kwargs):
    if isinstance(args_or_kwargs, dict):
        # If first arg is a dict, merge with kwargs
        combined_kwargs = {**args_or_kwargs, **kwargs}
        return func(**combined_kwargs)
    elif args_or_kwargs is not None:
        # If first arg is a list/tuple, treat as positional, but purrr::invoke 
        # primarily maps a list of arguments to the function's named parameters.
        # For the case 'invoke(paste, args, sep = "-")', it's treating args as a positional.
        return func(args_or_kwargs, **kwargs)
    return func(**kwargs)

# r2py:entity:exec
def exec_func(func, *args, **kwargs):
    return func(*args, **kwargs)

# Rename exec to avoid collision with python builtin if necessary, 
# but here we use exec_func to be safe.
exec = exec_func

# r2py:entity:invoke_map
def invoke_map(funs_dict, **kwargs):
    return {name: invoke(f, None, **kwargs) for name, f in funs_dict.items()}

# Simulation of R's runif (returns array of size n)
def runif(n=1):
    return np.random.uniform(0, 1, size=n)

# Simulation of R's rnorm (returns array of size n)
def rnorm(n=1):
    return np.random.normal(0, 1, size=n)

# Simulation of R's paste (joins strings with sep)
def paste(*args, sep=" "):
    return sep.join(map(str, args))

# Simulation of R's rcauchy
def rcauchy(n=1):
    return np.random.standard_cauchy(size=n)

# invoke(runif, list(n = 10))
invoke(runif, {'n': 10})

# invoke(runif, n = 10)
invoke(runif, n=10)

# exec(runif, n = 10)
exec(runif, n=10)

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
invoke(paste, args, sep="-")

# exec(paste, !!!args, sep = "-")
exec(paste, *args, sep="-")

# r2py:entity:funs
funs = [runif, rnorm]
# funs |> invoke_map(n = 5)
# Since funs is a list here, invoke_map needs to handle lists or we use a map
invoke_map_result = [invoke(f, n=5) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
args_list = [{'n': 10}, {'n': 5}]
invoke_map_list_result = [invoke(f, args_list[i]) for i, f in enumerate(funs)]

# funs |> map(exec, n = 5)
map_exec_result = [exec(f, n=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
map2_result = [exec(f, **args) for f, args in zip(funs, args_list)]

# r2py:entity:df
df = pd.DataFrame({
    'fun': funs,
    'args': args_list
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
pmap_result = df.apply(lambda row: exec(row['fun'], **row['args']), axis=1).tolist()

# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = rcauchy(100)
# r2py:entity:invoke_map_2
invoke_map(funs_stats, x=data_cauchy) # np.mean/median might need adjustment

# r2py:entity:list_1
# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
map_stats_result = {name: f(data_cauchy) for name, f in funs_stats.items()}