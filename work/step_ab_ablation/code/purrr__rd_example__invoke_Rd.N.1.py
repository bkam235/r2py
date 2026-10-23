import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
def invoke(func, args=None, **kwargs):
    if isinstance(args, dict):
        # If the first arg is a dict, merge it with kwargs
        combined_args = {**args, **kwargs}
        return func(**combined_args)
    elif args is not None:
        # If the first arg is not a dict, pass it as a positional arg
        return func(args, **kwargs)
    return func(**kwargs)

def exec_func(func, *args, **kwargs):
    return func(*args, **kwargs)

# R: invoke(runif, list(n = 10))
# In numpy, size is the equivalent of n
invoke(np.random.uniform, {'size': 10})

# R: invoke(runif, n = 10)
invoke(np.random.uniform, size=10)

# R: exec(runif, n = 10)
# Using a renamed helper 'exec_func' because 'exec' is a Python keyword
exec_func(np.random.uniform, size=10)

# R: args <- list("01a", "01b")
args = ["01a", "01b"]

# R: invoke(paste, args, sep = "-")
def paste_sim(x, sep="-"):
    if isinstance(x, list):
        return sep.join(x)
    return sep.join([str(x)])

invoke(paste_sim, args, sep="-")

# R: exec(paste, !!!args, sep = "-")
def paste_sim_varargs(*args, sep="-"):
    return sep.join(map(str, args))

exec_func(paste_sim_varargs, *args, sep="-")

# R: funs <- list(runif, rnorm)
funs = [np.random.uniform, np.random.normal]

# R: funs |> invoke_map(n = 5)
# In R, invoke_map applies the same args to a list of functions
invoke_map_res = [invoke(f, size=5) for f in funs]

# R: funs |> invoke_map(list(list(n = 10), list(n = 5)))
args_list = [{'size': 10}, {'size': 5}]
invoke_map_res_list = [invoke(f, a) for f, a in zip(funs, args_list)]

# R: funs |> map(exec, n = 5)
map_res = [exec_func(f, size=5) for f in funs]

# R: funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
map2_res = [exec_func(f, **a) for f, a in zip(funs, args_list)]

# R: df <- tibble::tibble(...)
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'size': 10}, {'size': 5}]
})

# R: df |> pmap(function(fun, args) exec(fun, !!!args))
pmap_res = [exec_func(row['fun'], **row['args']) for _, row in df.iterrows()]

# R: list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
funs_stats = {'m1': np.mean, 'm2': np.median}
data_cauchy = np.random.standard_cauchy(100)
# For stats functions, x is passed as the first positional argument
invoke_map_stats = {name: invoke(f, data_cauchy) for name, f in funs_stats.items()}

# R: list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
map_stats = {name: f(data_cauchy) for name, f in funs_stats.items()}