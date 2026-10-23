import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, args_or_kwargs=None, **kwargs):
    """
    Equivalent to purrr::invoke(f, args). 
    args_or_kwargs can be a list/dict or None.
    """
    if isinstance(args_or_kwargs, dict):
        params = {**args_or_kwargs, **kwargs}
        return func(**params)
    elif args_or_kwargs is not None:
        # If it's a list/tuple, treat as positional args
        return func(*args_or_kwargs, **kwargs)
    return func(**kwargs)

# r2py:entity:exec
def exec_func(func, *args, **kwargs):
    """
    Equivalent to purrr::exec(f, !!!args).
    Renamed to exec_func because 'exec' is a Python built-in.
    """
    return func(*args, **kwargs)

# r2py:entity:invoke_map
def invoke_map(funs_list, **kwargs):
    """
    Simplified invoke_map for the specific usage in the script.
    """
    if isinstance(funs_list, dict):
        return {k: invoke(v, **kwargs) for k, v in funs_list.items()}
    return [invoke(f, **kwargs) for f in funs_list]

# --- Execution ---

# invoke(runif, list(n = 10))
# r2py:entity:invoke
invoke(np.random.uniform, {'size': 10})

# invoke(runif, n = 10)
# r2py:entity:invoke_1
invoke(np.random.uniform, size=10)

# exec(runif, n = 10)
# r2py:entity:exec
exec_func(np.random.uniform, size=10)

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
invoke(lambda *x, args, sep="-": sep.join(map(str, x)), sep="-")

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
exec_func(lambda *x, sep="-": sep.join(map(str, x)), *args, sep="-")

# r2py:entity:funs
funs = [np.random.uniform, np.random.normal]
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
invoke_map(funs, size=5)

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
args_list = [{'size': 10}, {'size': 5}]
[invoke(f, arg) for f, arg in zip(funs, args_list)]

# funs |> map(exec, n = 5)
# r2py:entity:map
[exec_func(f, size=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
[exec_func(f, **arg) for f, arg in zip(funs, args_list)]

# r2py:entity:df
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'size': 10}, {'size': 5}]
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
df.apply(lambda row: exec_func(row['fun'], **row['args']), axis=1).tolist()

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = np.random.standard_cauchy(100)
# r2py:entity:invoke_map_2
invoke_map(funs_stats, x=data_cauchy) # Note: np.mean/median’s first arg is treated as x

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:list_1
funs_stats_list = {"m1": np.mean, "m2": np.median} 
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats_list.items()}