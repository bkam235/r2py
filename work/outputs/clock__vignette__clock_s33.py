import pandas as pd
import numpy as np

# suppressPackageStartupMessages is used to silence startup messages in R; no direct equivalent needed in Python.

# library(clock) is equivalent to importing date/time utilities.

# r2py:entity:x
def date_build(year, month=1, day=1):
    # Mimics R's date_build which returns a Date object
    return pd.Timestamp(year=year, month=month, day=day).date()

x = date_build(2020, 1, 1)

# r2py:entity:add_years
def add_years(date_obj, n):
    # n can be a scalar or a sequence (1:5 in R)
    if isinstance(n, (list, np.ndarray, range)):
        results = []
        for val in n:
            # Use DateOffset to add years
            res = pd.Timestamp(date_obj) + pd.DateOffset(years=int(val))
            results.append(res.strftime('%Y-%m-%d'))
        return results
    else:
        res = pd.Timestamp(date_obj) + pd.DateOffset(years=int(n))
        return res.strftime('%Y-%m-%d')

# R code: add_years(x, 1:5)
# r2py:entity:add_years
years_to_add = np.arange(1, 6)
res_add_years = add_years(x, years_to_add)

# To match R's output: [1] "2021-01-01" "2022-01-01" ...
formatted_output = ' '.join([f'"{d}"' for d in res_add_years])
print(f"[1] {formatted_output}")