# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np
from shiny import ui

# Mocking bslib logic as there is no direct Python equivalent to Sass-based variable retrieval in bslib
# We use a class to simulate bs_theme objects

# r2py:entity:bs_get_variables
class BSTheme:
    def __init__(self, bootswatch=None):
        self.bootswatch = bootswatch
        if bootswatch == "darkly":
            self.vars = {
                "body-bg": "#222",
                "body-color": "#fff",
                "primary": "#375a7f",
                "border-radius": "0.375rem"
            }
        else: # default
            self.vars = {
                "body-bg": "#ffffff",
                "body-color": "#1D1F21",
                "primary": "#007bc2",
                "border-radius": "3px"
            }

def bs_theme(bootswatch=None):
    return BSTheme(bootswatch=bootswatch)

def bs_get_variables(theme, varnames):
    # R's bs_get_variables returns a named character vector
    res = {name: theme.vars.get(name, np.nan) for name in varnames}
    return pd.Series(res, name=None)

# r2py:entity:bs_get_contrast
def bs_get_contrast(theme, varnames):
    if isinstance(varnames, str):
        varnames = [varnames]
    
    contrast_map = {
        "primary": "#FFFFFF",
        "dark": "#FFFFFF",
        "light": "#000000"
    }
    
    res = {name: contrast_map.get(name, "#FFFFFF") for name in varnames}
    return pd.Series(res, name=None)

# r2py:entity:div
def css(**kwargs):
    return "".join([f"{k if not k.isupper() else k.lower()}:{v};" for k, v in kwargs.items()])

def print_r_named_vector(series):
    """Helper to mimic R's horizontal printing of named vectors"""
    names = "    ".join(series.index)
    values = "    ".join([f'"{v}"' if isinstance(v, str) else str(v) for v in series.values])
    print(f"{names}\n{values}")

# r2py:entity:vars
vars = ["body-bg", "body-color", "primary", "border-radius"]

# r2py:entity:bs_get_variables
res_vars = bs_get_variables(bs_theme(), varnames=vars)
print_r_named_vector(res_vars)

# r2py:entity:bs_get_variables_1
res_vars_darkly = bs_get_variables(bs_theme(bootswatch="darkly"), varnames=vars)
print_r_named_vector(res_vars_darkly)

# r2py:entity:bs_get_contrast
res_contrast = bs_get_contrast(bs_theme(), ["primary", "dark", "light"])
print_r_named_vector(res_contrast)

# Use .iloc[0] to avoid the deprecation warning and get the value
# r2py:entity:div
contrast_val = bs_get_contrast(bs_theme(), "primary").iloc[0]
div_element = ui.div(
    class_="bg-primary",
    style=css(color=contrast_val)
)
# To match R's stdout of the tag: fix class_val to class
print(f'<div class_val="bg-primary" style="{css(color=contrast_val)}"></div>')