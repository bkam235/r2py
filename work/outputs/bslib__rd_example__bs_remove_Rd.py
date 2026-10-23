# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/bslib__rd_example__bs_remove_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'bslib__rd_example__bs_remove_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['version']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Note: bslib is an R package for Bootstrap theming. 
# Python's shiny implementation handles themes via ui.page_navbar or custom CSS.
# Since the R code manipulates a Bootstrap theme object's internal CSS classes,
# we simulate the theme object logic using a dictionary/class structure.

# r2py:entity:bs4
class BSTheme:
    def __init__(self, version=4):
        self.version = version
        self.components = {
            "_print": "print-styles",
            "_carousel": "carousel-styles",
            "bs3compat": "compat-styles"
        }

# r2py:entity:bs_retrieve
    def retrieve(self, component, include_unnamed=False):
        return self.components.get(component, None)

# r2py:entity:bs4_no_print
    def remove(self, components_to_remove):
        new_theme = BSTheme(self.version)
        new_theme.components = {k: v for k, v in self.components.items() 
                               if k not in components_to_remove}
        return new_theme

bs4 = BSTheme(version=4)

# bs_retrieve(bs4, "_print", include_unnamed = FALSE)
# r2py:entity:bs_retrieve
bs4.retrieve("_print", include_unnamed=False)

# bs4_no_print <- bs_remove(bs4, c("_print", "_carousel"))
bs4_no_print = bs4.remove(["_print", "_carousel"])

# suppressWarnings(bs_retrieve(bs4_no_print, "_print", include_unnamed = FALSE))
# r2py:entity:suppressWarnings
bs4_no_print.retrieve("_print", include_unnamed=False)

# bs4_no_compat <- bs_remove(bs4, "bs3compat")
# r2py:entity:bs4_no_compat
bs4_no_compat = bs4.remove(["bs3compat"])