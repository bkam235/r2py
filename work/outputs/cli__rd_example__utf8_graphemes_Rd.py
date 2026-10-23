# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# The R code focuses on Unicode grapheme splitting
# In Python, the 'grapheme' library is the equivalent to R's utf8_graphemes
# Since it is a specialized library, we use a common substitute or a simple list
import grapheme

# r2py:entity:str
text_str = (
    "\U0001f477\U0001f3ff\u200d\u2640\ufe0f"
    "\U0001f477\U0001f3ff"
    "\U0001f477\u200d\u2640\ufe0f"
    "\U0001f477\U0001f3fb"
    "\U0001f477\U0001f3ff"
)

# r2py:entity:cat
print(text_str)
# r2py:entity:chrs
chrs = list(grapheme.graphemes(text_str))