import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
def invoke(func, args, **kwargs):
    if isinstance(args, dict):
        return func(**args, **kwargs)
    elif isinstance(args, (list, tuple)):
        # R's invoke(f, list(n=10)) treats the list as named arguments if possible
        # Since we can't easily detect named lists in Python, 
        # we assume if it's used like invoke(runif, list(n=10)), it's passed as a dict
        return func(*args, **kwargs)
    else:
        return func(args, **kwargs)

def purrr_exec(func, *args, **kwargs):
    return func(*args, **kwargs)

def invoke_map(funs_list, **kwargs):
    # In R, if funs is a named list, it returns a named list
    if isinstance(funs_list, dict):
        return {name: invoke(f, kwargs, **{}) for name, f in funs_list.items()}
    else:
        return [invoke(f, kwargs, **{}) for f in funs_list]

# invoke(runif, list(n = 10))
# r2py:entity:invoke
invoke(np.random.uniform, {'size': 10})

# invoke(runif, n = 10)
# r2py:entity:invoke_1
# In R: invoke(runif, n = 10) is effectively passing n=10 as the args
invoke(np.random.uniform, {'size': 10})

# exec(runif, n = 10)
# r2py:entity:exec
purrr_exec(np.random.uniform, size=10)

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
invoke(lambda x, args, sep="-": sep.join(x), sep="-")

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
purrr_exec(lambda *args, sep="-": sep.join(args), *args, sep="-")

# r2py:entity:funs
# R: funs <- list(runif, rnorm)
funs = [np.random.uniform, np.random.normal]
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
[invoke(f, {'size': 5}) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
args_list = [{'size': 10}, {'size': 5}]
[invoke(f, arg) for f, arg in zip(funs, args_list)]

# funs |> map(exec, n = 5)
# r2py:entity:map
[purrr_exec(f, size=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
[purrr_exec(f, **arg) for f, arg in zip(funs, args_list)]

# r2py:entity:df
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'n': 10}, {'n': 5}]
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
df.apply(lambda row: purrr_exec(row['fun'], **row['args']), axis=1).tolist()

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = np.random.standard_cauchy(100)
# r2py:entity:invoke_map_2
# R's invoke_map(x = ...) passes x as the argument to the function
{name: f(data_cauchy) for name, f in funs_stats.items()}

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:list_1
# The R code is: list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats.items()}