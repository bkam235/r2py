# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Note: systemfonts and font_feature are R-specific for low-level OpenType font manipulation.
# Python handles font properties via matplotlib/plotnine's font manager or CSS in Shiny.
# There is no direct equivalent to font_feature() in standard Python data libraries,
# as these are system-level font rendering instructions.

# Representing the configuration logically as a dictionary/object since 
# they function as global settings in the R script.
# r2py:entity:font_feature
font_feature_settings = {
    "letters": "stylistic",
    "numbers": ["lining", "tabular"]
}

# r2py:entity:font_feature_1
font_feature_salt = {
    "numbers": ["lining", "tabular"],
    "salt": 2
}