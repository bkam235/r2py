# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Equivalent to knitr::opts_chunk$set and options(tibble.print_min/max)
# Pandas options for display control
# r2py:entity:options
pd.set_option('display.max_rows', 6)
pd.set_option('display.min_rows', 6)