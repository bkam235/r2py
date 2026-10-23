import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, args_or_kwargs=None, **kwargs):
    if isinstance(args_or_kwargs, dict):
        return func(**args_or_kwargs, **kwargs)
    elif isinstance(args_or_kwargs, (list, tuple)):
        # If it's a list, R's invoke usually treats it as positional arguments 
        # but in these examples it's often passed as a list of arguments
        return func(*args_or_kwargs, **kwargs)
    return func(**kwargs)

# r2py:entity:exec
def py_exec(func, *args, **kwargs):
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
py_exec(np.random.uniform, size=10)

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
# R's paste(args, sep="-") joins the elements of the vector
invoke(lambda x, sep: sep.join(x), args, sep="-")

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
py_exec(lambda *args, sep="-": sep.join(args), *args, sep="-")

# r2py:entity:funs
funs = [np.random.uniform, np.random.normal]
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
# Since funs is a list here, we simulate map(invoke, ...)
[invoke(f, size=5) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
args_list = [{'size': 10}, {'size': 5}]
[invoke(f, args_list[i]) for i, f in enumerate(funs)]

# funs |> map(exec, n = 5)
# r2py:entity:map
[py_exec(f, size=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
[py_exec(f, **a) for f, a in zip(funs, args_list)]

# r2py:entity:df
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'size': 10}, {'size': 5}]
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
# Result should be a list of results
pmap_res = df.apply(lambda row: py_exec(row['fun'], **row['args']), axis=1).tolist()

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = np.random.standard_cauchy(100)
# r2py:entity:invoke_map_2
invoke_map(funs_stats, x=data_cauchy)

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:list_1
funs_stats_list = {"m1": np.mean, "m2": np.median}
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats_list.items()}