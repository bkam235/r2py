# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import ui

# Note: bslib card() equivalent in shiny for Python is ui.card()
# r2py:entity:x
x = ui.card("A simple card")

# Always has 2 columns (on non-mobile)
# r2py:entity:layout_column_wrap
ui.layout_column_wrap(x, x, x, width=1/2)

# Automatically lays out three cards into columns
# such that each column is at least 200px wide:
# r2py:entity:layout_column_wrap_1
ui.layout_column_wrap(x, x, x)

# To use larger column widths by default, set `width`.
# This example has 3 columns when the screen is at least 900px wide:
# r2py:entity:layout_column_wrap_2
ui.layout_column_wrap(x, x, x, width="300px")

# You can add a list of items, spliced with rlang's `!!!` operator
# In Python, the * operator handles the unpacking equivalent to !!! in R
# r2py:entity:layout_column_wrap_3
elements = [x, x, x]
ui.layout_column_wrap(*elements)