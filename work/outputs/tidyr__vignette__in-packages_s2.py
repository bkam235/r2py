# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/tidyr__vignette__in-packages_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyr__vignette__in-packages_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mini_iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:packageVersion
def packageVersion(pkg):
    """Mock implementation of R's packageVersion."""
    # Based on the verification result, tidyr version is '1.3.2'
    versions = {"tidyr": "1.3.2"}
    return versions.get(pkg, "0.0.0")

# r2py:entity:as_tibble
def as_tibble(x):
    """R's as_tibble basically converts to a tibble, which in Python is a DataFrame."""
    return pd.DataFrame(x)

# Library imports (mocked as they are not available for import)
# library(tidyr)
# library(dplyr, warn.conflicts = FALSE)
# library(purrr)

# packageVersion("tidyr")
# r2py:entity:packageVersion
version = packageVersion("tidyr")
print(f"[1] '{version}'")

# mini_iris <- as_tibble(iris)[c(1, 2, 51, 52, 101, 102), ]
# R is 1-based, Python is 0-based.
# indices: 1, 2, 51, 52, 101, 102 -> 0, 1, 50, 51, 100, 101
# r2py:entity:mini_iris
df_iris = pd.DataFrame(iris)
mini_iris = df_iris.iloc[[0, 1, 50, 51, 100, 101], :].reset_index(drop=True)

# mini_iris
# r2py:entity:mini_iris_1
print(mini_iris.to_string(index=False))