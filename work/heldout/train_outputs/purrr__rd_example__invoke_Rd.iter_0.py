# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 19

import numpy as np
import pandas as pd
from plotnine import *
from shiny import App, ui, render

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(func, **kwargs, args_dict=None):
    if args_dict:
        return func(**args_dict, **kwargs)
    return func(**kwargs)

# r2py:entity:exec
def exec(func, *args, **kwargs):
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
exec(np.random.uniform, 10) # Adjusted for numpy's positional arguments or use size=10

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
invoke(lambda x, sep: sep.join(x), args, sep="-")

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
exec(lambda *args, sep: sep.join(args), *args, sep="-")

# r2py:entity:funs
funs = {"runif": np.random.uniform, "rnorm": np.random.normal}
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
invoke_map(funs, size=5)

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# In Python, we map specifically over the dictionary values
# r2py:entity:invoke_map_1
args_list = [{'size': 10}, {'size': 5}]
{name: f(**args) for (name, f), args in zip(funs.items(), args_list)}

# funs |> map(exec, n = 5)
# r2py:entity:map
{name: exec(f, 5) for name, f in funs.items()}

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
{name: exec(f, **args) for (name, f), args in zip(funs.items(), args_list)}

# r2py:entity:df
df = pd.DataFrame({
    'fun': [np.random.uniform, np.random.normal],
    'args': [{'size': 10}, {'size': 5}]
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
df.apply(lambda row: exec(row['fun'], **row['args']), axis=1).tolist()

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:list
funs_stats = {"m1": np.mean, "m2": np.median}
data_cauchy = np.random.standard_cauchy(100)
# r2py:entity:invoke_map_2
invoke_map(funs_stats, x=data_cauchy) # Note: np.mean/median take array as first positional arg

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:map_1
{name: f(data_cauchy) for name, f in funs_stats.items()}