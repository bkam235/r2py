# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from shiny import App, ui, render
from plotnine import ggplot, aes, geom_point
import sys

# Equivalent to options(scipen = 3) - formatting float output
# r2py:entity:options
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)