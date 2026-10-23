import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, args_val=None, **kwargs):
    if args_val is not None and isinstance(args_val, dict):
        return func(**args_val, **kwargs)
    elif args_val is not None:
        return func(args_val, **kwargs)
    return func(**kwargs)

# r2py:entity:exec
def exec_(func, *args, **kwargs):
    return func(*args, **kwargs)

# r2py:entity:invoke_map
def invoke_map(funs_dict, **kwargs):
    return {name: invoke(f, **kwargs) for name, f in funs_dict.items()}

# invoke(runif, list(n = 10))
# r2py:entity:invoke
invoke(np.random.uniform, {'size': 10})

# invoke(runif, n = 10)
# r2py:entity:invoke_1
invoke(np.random.uniform, size=10)

# exec(runif, n = 10)
# r2py:entity:exec
exec_(np.random.uniform, size=10)

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
invoke(lambda x, args, sep="-": sep.join(x))

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
exec_(lambda *args, sep="-": sep.join(args), *args, sep="-")

# r2py:entity:funs
funs = [np.random.uniform, np.random.normal]
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
[invoke(f, size=5) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
args_list = [{'size': 10}, {'size': 5}]
[invoke(f, args_list[i]) for i, f in enumerate(funs)]

# funs |> map(exec, n = 5)
# r2py:entity:map
[exec_(f, size=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
[exec_(f, **args) for f, args in zip(funs, args_list)]

# r2py:entity:df
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'size': 10}, {'size': 5}]
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
df.apply(lambda row: exec_(row['fun'], **row['args']), axis=1).tolist()

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = np.random.standard_cauchy(100)
# r2py:entity:invoke_map_2
# In R, invoke_map passed to a named list applies the func to the data. 
# np.mean/median don't take 'x' as a keyword usually but as first positional.
{name: f(data_cauchy) for name, f in funs_stats.items()}

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats.items()}