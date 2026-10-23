# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from shiny import App, ui, render

# r2py:entity:xs
xs = [np.random.uniform(0, 1, 10).tolist() for _ in range(8)]
# r2py:entity:xs[[1]][[1]]
xs[0][0] = np.nan

# r2py:entity:ws
ws = [(np.random.poisson(5, 10) + 1).tolist() for _ in range(8)]