# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import bslib
from shiny import ui

# r2py:entity:x
x = bslib.card("A simple card")

# Always has 2 columns (on non-mobile)
# layout_column_wrap(width = 1/2, x, x, x)
# r2py:entity:layout_column_wrap
layout_column_wrap = bslib.layout_column_wrap(x, x, x, width=1/2)

# Automatically lays out three cards into columns
# such that each column is at least 200px wide:
# layout_column_wrap(x, x, x)
# r2py:entity:layout_column_wrap_1
layout_column_wrap_1 = bslib.layout_column_wrap(x, x, x)

# To use larger column widths by default, set `width`.
# This example has 3 columns when the screen is at least 900px wide:
# layout_column_wrap(width = "300px", x, x, x)
# r2py:entity:layout_column_wrap_2
layout_column_wrap_2 = bslib.layout_column_wrap(x, x, x, width="300px")

# You can add a list of items, spliced with rlang's `!!!` operator
# layout_column_wrap(!!!list(x, x, x))
# In Python, the * operator handles the unpacking equivalent to !!! in R
# r2py:entity:layout_column_wrap_3
elements = [x, x, x]
layout_column_wrap_3 = bslib.layout_column_wrap(*elements)