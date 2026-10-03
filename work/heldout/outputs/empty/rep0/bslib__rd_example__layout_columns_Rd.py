# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

from shiny import ui

# Note: shiny for Python handles layout differently than bslib in R.
# layout_columns is approximated using ui.layout_columns.
# card() is approximated using ui.card().

# r2py:entity:x
x = ui.card("A simple card")

# Example 1
# r2py:entity:page_fillable
ui.page_fillable(
    ui.layout_columns(x, x, x, x)
)

# Example 2
# !!!list(x, x, x) in R is equivalent to unpacking a list in Python
# r2py:entity:page_fillable_1
x_list = [x, x, x]
ui.page_fillable(
    ui.layout_columns(*x_list)
)

# Example 3
# r2py:entity:page_fillable_2
ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths=[6, 6, 12]
    )
)

# Example 4
# r2py:entity:page_fillable_3
ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths=[6, 6, -2, 8],
        row_heights=[1, 3]
    )
)

# Example 5
# Python shiny's layout_columns col_widths accepts a dictionary for breakpoints
# r2py:entity:page_fillable_4
ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths={
            "sm": [12, 12, 12],
            "md": [6, 6, 12],
            "lg": [4, 4, 4]
        },
        fillable_mobile=True
    )
)