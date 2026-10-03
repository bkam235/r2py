# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, render, ui

# In Python/Pandas, name collisions are handled by the namespace (e.g., pd.merge).
# There is no direct equivalent to conflicted::conflicts_prefer as functions 
# are not globally imported into the namespace in the same way as R.
# The following logic ensures we use the pandas versions of filter and lag.

# Define aliases to mimic the R preference if needed
# r2py:entity:conflicts_prefer
filter = pd.DataFrame.filter
lag = lambda x, n=1: x.shift(n)