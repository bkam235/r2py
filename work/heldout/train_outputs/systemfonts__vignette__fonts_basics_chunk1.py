# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render
import matplotlib.pyplot as plt

# Equivalent to knitr::opts_chunk$set for plotting defaults
# r2py:entity:opts_chunk$set
plt.rcParams.update({
    'figure.dpi': 144,
    'figure.figsize': (7, 4.326),
    'savefig.dpi': 144
})