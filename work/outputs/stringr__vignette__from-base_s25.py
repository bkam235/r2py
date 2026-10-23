# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import textwrap
import pandas as pd
import numpy as np
from plotnine import *

# r2py:entity:gettysburg
gettysburg = "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal."

# Translation of strwrap()
# r2py:entity:cat
print("\n".join(textwrap.wrap(gettysburg, width=60)))

# Translation of str_wrap() (stringr)
# r2py:entity:cat_1
print(textwrap.fill(gettysburg, width=60))