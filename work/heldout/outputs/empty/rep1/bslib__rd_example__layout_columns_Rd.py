# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

from shiny import ui
from shiny.ui import page_fillable, layout_columns, card

# r2py:entity:x
x = card("A simple card")

# r2py:entity:page_fillable
page_fillable_0 = page_fillable(
    layout_columns(x, x, x, x)
)

# r2py:entity:page_fillable_1
x_list = [x, x, x]
page_fillable_1 = page_fillable(
    layout_columns(*x_list)
)

# r2py:entity:page_fillable_2
page_fillable_2 = page_fillable(
    layout_columns(x, x, x, col_widths=[6, 6, 12])
)

# r2py:entity:page_fillable_3
page_fillable_3 = page_fillable(
    layout_columns(x, x, x, col_widths=[6, 6, -2, 8], row_heights=[1, 3])
)

# r2py:entity:page_fillable_4
page_fillable_4 = page_fillable(
    layout_columns(
        x, x, x, 
        col_widths={
            "sm": [12, 12, 12],
            "md": [6, 6, 12],
            "lg": [4, 4, 4]
        }
    ),
    fillable_mobile=True
)