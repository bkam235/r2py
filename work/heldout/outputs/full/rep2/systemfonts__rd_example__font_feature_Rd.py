# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Note: systemfonts and font_feature are specific to R's graphics device (like ragg/showtext)
# Python's matplotlib/plotnine handles fonts via rcParams or font properties.
# There is no direct 1:1 functional equivalent to font_feature() in a general Python library 
# as it interacts with OpenType feature tags at the rendering engine level.
# To achieve similar results, one typically sets a specific font family that has these 
# features enabled by default or uses low-level matplotlib font properties.

# Approximation of font configuration for plotnine/matplotlib
import matplotlib.pyplot as plt

# r2py:entity:font_feature
plt.rcParams['font.family'] = 'sans-serif'
# Note: 'lining' and 'tabular' figures are typically handled by choosing a 
# font that supports them or using specific matplotlib font managers.