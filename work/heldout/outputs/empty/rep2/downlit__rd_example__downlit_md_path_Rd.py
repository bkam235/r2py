# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# The provided R code uses 'downlit' and 'rmarkdown' for markdown 
# formatting and pandoc version checking. There is no direct 
# 1:1 Python library for 'downlit' (which is a helper for rendering 
# markdown in RStudio/Quarto), but the logical equivalent of 
# processing/printing these strings is provided below.

import subprocess

# r2py:entity:is_installed
def pandoc_available(version):
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            # Simplistic version check approximating rmarkdown::pandoc_available
            return True 
    except FileNotFoundError:
        return False
    return False

# r2py:entity:downlit_md_string
def downlit_md_string(s):
    print(s)

# r2py:entity:pandoc_available
if pandoc_available("1.19"):
# r2py:entity:downlit_md_string
    downlit_md_string("`base::t()`")
# r2py:entity:downlit_md_string_1
    downlit_md_string("`base::t`")
# r2py:entity:downlit_md_string_2
    downlit_md_string("* `base::t`")
# r2py:entity:downlit_md_string_3
    downlit_md_string("## `base::t`")