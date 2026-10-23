import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
def invoke(func, args, **kwargs):
    """
    In R, invoke(func, list(n=10)) calls func(n=10).
    If args is a dict, it unpacks it as keyword arguments.
    """
    if isinstance(args, dict):
        return func(**args, **kwargs)
    return func(args, **kwargs)

def exec_purrr(func, *args, **kwargs):
    """
    In R, exec is just a wrapper for calling a function with unpacked arguments.
    Renamed to exec_purrr because 'exec' is a Python built-in.
    """
    return func(*args, **kwargs)

def invoke_map(funs, **kwargs):
    """
    Simulates invoke_map: applies the same arguments to a list/dict of functions.
    """
    if isinstance(funs, dict):
        return {k: invoke(v, {}, **kwargs) if not kwargs else invoke(v, kwargs, {}) for k, v in funs.items()}
    # This is a simplified version for the specific examples provided
    return [invoke(f, {}, **kwargs) for f in funs]

# --- Translation of R script ---

# invoke(runif, list(n = 10))
# R's runif(n=10) -> np.random.uniform(size=10)
invoke(np.random.uniform, {'size': 10})

# invoke(runif, n = 10)
# R's invoke can take named args directly
invoke(np.random.uniform, {'size': 10})

# exec(runif, n = 10)
exec_purrr(np.random.uniform, size=10)

# args <- list("01a", "01b")
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# paste in R joins vectors; here we simulate with "-".join()
invoke(lambda x, args, sep="-": sep.join(x), sep="-")

# exec(paste, !!!args, sep = "-")
exec_purrr(lambda *args, sep="-": sep.join(args), *args, sep="-")

# funs <- list(runif, rnorm)
funs = [np.random.uniform, np.random.normal]

# funs |> invoke_map(n = 5)
# Since Python's numpy uses 'size', we map to that
[f(size=5) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
args_list = [{'size': 10}, {'size': 5}]
[f(**a) for f, a in zip(funs, args_list)]

# funs |> map(exec, n = 5)
[exec_purrr(f, size=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
[exec_purrr(f, **a) for f, a in zip(funs, args_list)]

# df <- tibble::tibble(...)
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'size': 10}, {'size': 5}]
})

# df |> pmap(function(fun, args) exec(fun, !!!args))
pmap_res = [exec_purrr(row['fun'], **row['args']) for _, row in df.iterrows()]

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
funs_stats = {'m1': np.mean, 'm2': np.median}
x_val = np.random.standard_cauchy(100)
# invoke_map applies the same x to all
res_invoke_map = {name: f(x_val) for name, f in funs_stats.items()}

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
res_map = {name: f(np.random.standard_cauchy(100)) for name, f in funs_stats.items()}