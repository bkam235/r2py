# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render
import scipy.stats as stats

# Equivalent to options(scipen = 3)
# r2py:entity:options
pd.set_option('display.float_format', lambda x: '%.3f' % x)
np.set_printoptions(suppress=True, precision=3)