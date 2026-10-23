# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:df
def tribble_mimic(data):
    """Mimics R's tribble for creating data frames from a list of rows."""
    return pd.DataFrame(data)

# Creating the data frame
# In R: ~rng, ~params
# Note: 'lambda' in the list is renamed to 'lambda_val' if it were a variable, 
# but inside a dictionary key as a string it is fine.
data_rows = [
    ["runif", {"min": -1, "max": 1}],
    ["rnorm", {}],
    ["rpois", {"lambda": 5}],
]
df = pd.DataFrame(data_rows, columns=["rng", "params"])

# r2py:entity:f
def f(rng, params):
    """
    Mimics the logic of purrr::exec(rng, n = 10, !!!params).
    In R, rng is a string like 'runif' which is then called as a function.
    """
    # Map R function names to numpy/random equivalents
    funcs = {
        "runif": lambda p: np.random.uniform(p.get("min", 0), p.get("max", 1), 10),
        "rnorm": lambda p: np.random.standard_normal(10),
        "rpois": lambda p: np.random.poisson(p.get("lambda", 1), 10),
    }
    
    func = funcs.get(rng)
    if func:
        return func(params)
    return None

# df |> mutate(data = list(f(rng, params)))
# rowwise() in R ensures the function f is called for each row.
# In pandas, we use apply(axis=1).
# r2py:entity:mutate
df["data"] = df.apply(lambda row: f(row["rng"], row["params"]), axis=1)

print(df)