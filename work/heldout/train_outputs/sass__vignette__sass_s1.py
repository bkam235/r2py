# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 2

import sass
import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# r2py:entity:opts_chunk$set
# knitr::opts_chunk$set equivalent for Python/Plotnine/Shiny
# Note: Python doesn't have a direct global 'chunk' config like knitr, 
# but we can set global plotnine themes and pandas options to match.
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# To approximate the fig.align and out.width behavior in plotnine:
# plotnine plots are typically handled by the rendering engine in Shiny
# but global theme settings can be applied here.
theme_set(theme_minimal())