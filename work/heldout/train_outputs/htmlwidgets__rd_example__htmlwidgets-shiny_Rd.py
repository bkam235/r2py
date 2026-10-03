# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import render, ui

# r2py:entity:fooOutput
def fooOutput(outputId, width="100%", height="400px"):
    return ui.HTML(f'<div id="{outputId}" style="width: {width}; height: {height};"></div>')

# r2py:entity:renderFoo
def renderFoo(expr):
    return render.ui(expr)