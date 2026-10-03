# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

from shiny import ui

# Note: bslib cards are implemented as ui.card in shiny for Python
# r2py:entity:x
x = ui.card("A simple card")

# Section 1
# r2py:entity:page_fillable
ui.page_fillable(
    ui.layout_columns(x, x, x, x)
)

# Section 2
# In Python, we can pass the list directly or use unpacking (*) 
# equivalent to !!! in R
# r2py:entity:page_fillable_1
x_list = [x, x, x]
ui.page_fillable(
    ui.layout_columns(*x_list)
)

# Section 3
# r2py:entity:page_fillable_2
ui.page_fillable(
    ui.layout_columns(x, x, x, col_widths=[6, 6, 12])
)

# Section 4
# r2py:entity:page_fillable_3
ui.page_fillable(
    ui.layout_columns(x, x, x, col_widths=[6, 6, -2, 8], row_heights=[1, 3])
)

# Section 5
# breakpoints in R bslib are handled via dictionary mapping in Python's layout_columns
# r2py:entity:page_fillable_4
ui.page_fillable(
    ui.layout_columns(
        x, x, x, 
        col_widths={
            "sm": [12, 12, 12],
            "md": [6, 6, 12],
            "lg": [4, 4, 4],
        }
    ), 
    fillable_mobile=True
)