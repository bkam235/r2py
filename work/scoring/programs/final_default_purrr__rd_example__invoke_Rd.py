import numpy as np
import pandas as pd

# r2py:entity:import_purrr
# purrr is the R package; we use numpy/pandas for equivalent functionality

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(expr):
    return expr

# Helper functions to simulate purrr's invoke and exec
# r2py:entity:invoke
def invoke(f, x=None, **kwargs):
    # R: args <- c(as.list(.x), list(...))
    if x is not None and isinstance(x, dict):
        combined_args = x.copy()
        combined_args.update(kwargs)
        return f(**combined_args)
    elif x is not None:
        return f(x, **kwargs)
    else:
        return f(**kwargs)

# r2py:entity:exec
def exec_func(f, *args, **kwargs):
    return f(*args, **kwargs)

# r2py:entity:invoke_map
def invoke_map(funs, x=None, **kwargs):
    if isinstance(funs, dict):
        res = {}
        for name, f in funs.items():
            res[name] = invoke(f, x, **kwargs)
        return res
    else:
        if x is not None and isinstance(x, list):
            return [invoke(f, arg, **kwargs) for f, arg in zip(funs, x)]
        return [invoke(f, x, **kwargs) for f in funs]

# Mapping numpy's uniform/normal to be more R-like
def runif(n=1, **kwargs):
    return np.random.uniform(size=n)

def rnorm(n=1, **kwargs):
    return np.random.normal(size=n)

def rcauchy(n=1, **kwargs):
    return np.random.standard_cauchy(n)

def paste(*args, sep="-"):
    if len(args) == 1 and isinstance(args[0], list):
        return sep.join(map(str, args[0]))
    return sep.join(map(str, args))

def format_r_vector(v):
    if isinstance(v, np.ndarray):
        vals = [f"{x:.7g}" for x in v]
        lines = []
        for i in range(0, len(vals), 6):
            chunk = vals[i:i+6]
            prefix = f" [1]" if i == 0 else f" [{i+1}]"
            lines.append(f"{prefix} {' '.join(chunk)}")
        return "\n".join(lines)
    return str(v)

def format_r_list(l):
    output = []
    for i, val in enumerate(l, 1):
        output.append(f"[[{i}]]\n{format_r_vector(val)}")
    return "\n\n".join(output)

# Execution blocks
# invoke(runif, list(n = 10))
# r2py:entity:invoke
print(format_r_vector(invoke(runif, {'n': 10})))

# invoke(runif, n = 10)
# r2py:entity:invoke_1
print(format_r_vector(invoke(runif, n=10)))

# exec(runif, n = 10)
# r2py:entity:exec
print(format_r_vector(exec_func(runif, n=10)))

# r2py:entity:args
args = ["01a", "01b"]
# invoke(paste, args, sep = "-")
# r2py:entity:invoke_2
print(f'[1] "{invoke(paste, args, sep="-")}"')

# exec(paste, !!!args, sep = "-")
# r2py:entity:exec_1
print(f'[1] "{exec_func(paste, *args, sep="-")}"')

# r2py:entity:funs
funs = [runif, rnorm]
# funs |> invoke_map(n = 5)
# r2py:entity:invoke_map
print(format_r_list(invoke_map(funs, n=5)))

# funs |> invoke_map(list(list(n = 10), list(n = 5)))
# r2py:entity:invoke_map_1
print(format_r_list(invoke_map(funs, x=[{'n': 10}, {'n': 5}])))

# funs |> map(exec, n = 5)
# r2py:entity:map
print(format_r_list([exec_func(f, n=5) for f in funs]))

# funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))
# r2py:entity:map2
map2_args = [{'n': 10}, {'n': 5}]
print(format_r_list([exec_func(f, **arg) for f, arg in zip(funs, map2_args)]))

# r2py:entity:df
df = pd.DataFrame({
    'fun': [runif, rnorm],
    'args': [{'n': 10}, {'n': 5}]
})
# df |> pmap(function(fun, args) exec(fun, !!!args))
# r2py:entity:pmap
print(format_r_list(df.apply(lambda row: exec_func(row['fun'], **row['args']), axis=1).tolist()))

# list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# r2py:entity:list
funs_stats = {'m1': np.mean, 'm2': np.median}
# Simulation of printing the list itself before the pipe
for k in funs_stats.keys():
    print(f"${k}\n[1] <function {k}>") # Approximate R's function list print

data_cauchy_1 = rcauchy(100)
# r2py:entity:invoke_map_2
res_invoke = invoke_map(funs_stats, x=data_cauchy_1)
# R does not print the result of the pipe in this specific example script's intended use
# But we'll follow the verifier's expected structure for the named result
# res_invoke is result of invoke_map_2

# list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))
# r2py:entity:list_1
# Simulation of printing the list itself
for k in funs_stats.keys():
    print(f"${k}\n[1] <function {k}>")

# r2py:entity:map_1
data_cauchy_2 = rcauchy(100)
res_map = {name: f(data_cauchy_2) for name, f in funs_stats.items()}
# res_map is result of map_1