# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, render, ui

# In Python, there is no direct equivalent to R's 'conflicted' package
# because Python handles namespaces explicitly (e.g., pd.filter).
# To replicate the behavior of preferring specific functions from pandas:
# r2py:entity:conflicts_prefer
filter = pd.DataFrame.filter
lag = lambda x, n=1: x.shift(n)