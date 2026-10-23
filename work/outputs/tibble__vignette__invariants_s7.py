# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from shiny import App, ui, render

# r2py:entity:with_df
def with_df(code_func, verbose=False):
    df = new_df()
    result = code_func(df)
    if verbose:
        print(f"Executing operation on df: {code_func}")
    return result

# r2py:entity:with_tbl
def with_tbl(code_func, verbose=False):
    tbl = new_tbl()
    result = code_func(tbl)
    if verbose:
        print(f"Executing operation on tbl: {code_func}")
    return result

# r2py:entity:with_df2
def with_df2(code_func):
    df2 = new_df2()
    return code_func(df2)

# r2py:entity:with_tbl2
def with_tbl2(code_func):
    tbl2 = new_tbl2()
    return code_func(tbl2)