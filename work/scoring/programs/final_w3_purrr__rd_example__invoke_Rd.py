import numpy as np
import pandas as pd

# Helper functions to simulate purrr's invoke and exec
def invoke(func, x=None, **kwargs):
    # R's invoke(f, list(n=10)) or invoke(f, n=10)
    # If x is a dict, it's like passing a list of named arguments in R
    final_kwargs = kwargs.copy()
    if isinstance(x, dict):
        final_kwargs.update(x)
    
    # Handle the 'n' -> 'size' translation for numpy random functions
    if 'n' in final_kwargs:
        final_kwargs['size'] = final_kwargs.pop('n')
    
    # If x is not a dict, it's a positional argument
    if x is not None and not isinstance(x, dict):
        return func(x, **final_kwargs)
    
    return func(**final_kwargs)

def exec(func, *args, **kwargs):
    # Handle 'n' -> 'size' for numpy random functions if passed as keyword
    if 'n' in kwargs:
        kwargs['size'] = kwargs.pop('n')
    return func(*args, **kwargs)

def invoke_map(funs_dict, **kwargs):
    return {name: invoke(f, **kwargs) for name, f in funs_dict.items()}

# runif simulation
def runif(n=0, **kwargs):
    return np.random.uniform(size=n)

# rnorm simulation
def rnorm(n=0, **kwargs):
    return np.random.normal(size=n)

# rcauchy simulation
def rcauchy(n=0, **kwargs):
    return np.random.standard_cauchy(n)

# invoke(runif, list(n = 10))
res_invoke = invoke(runif, {'n': 10})

# invoke(runif, n = 10)
res_invoke_1 = invoke(runif, n=10)

# exec(runif, n = 10)
res_exec = exec(runif, n=10)

# was
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# paste in R: paste(args, sep="-") -> "01a-01b"
def paste_sim(x, sep=" "):
    if isinstance(x, list):
        return sep.join(x)
    return sep.join(map(str, x))

res_invoke_2 = invoke(paste_sim, args, sep="-")

# exec(paste, !!!args, sep = "-")
def paste_exec_sim(*args, sep=" "):
    return sep.join(map(str, args))

res_exec_1 = exec(paste_exec_sim, *args, sep="-")

# was
funs = [runif, rnorm]
# funs |> invoke_map(n = 5)
# In R, invoke_map is often used on named lists. Here funs is a simple list.
# Let's implement map logic
res_invoke_map = [invoke(f, n=5) for f in funs]

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
args_list_map = [{'n': 10}, {'n': 5}]
res_invoke_map_1 = [invoke(f, args_list_map[i]) for i, f in enumerate(funs)]

# now
# funs |> map(exec, n = 5)
res_map = [exec(f, n=5) for f in funs]

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
res_map2 = [exec(f, **args_list_map[i]) for i, f in enumerate(funs)]

# or use pmap + a tibble
df = pd.DataFrame({
    'fun': [runif, rnorm],
    'args': [{'n': 10}, {'n': 5}]
})
res_pmap = df.apply(lambda row: exec(row['fun'], **row['args']), axis=1).tolist()

# was
funs_stats = {'m1': np.mean, 'm2': np.median}
data_cauchy = rcauchy(100)
# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# np.mean/median take the array as the first argument
def stat_invoke(f, x):
    return f(x)

res_invoke_map_2 = {name: f(data_cauchy) for name, f in funs_stats.items()}

# now
# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
res_map_1 = {name: f(data_cauchy) for name, f in funs_stats.items()}