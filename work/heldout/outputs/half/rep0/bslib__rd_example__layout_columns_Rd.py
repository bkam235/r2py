# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

from shiny import App, ui
from shiny.ui import page_fillable, layout_columns, card

# r2py:entity:x
x = card("A simple card")

# Equivalent to: page_fillable(layout_columns(x, x, x, x))
# r2py:entity:page_fillable
app1 = page_fillable(
    layout_columns(x, x, x, x)
)

# Equivalent to: page_fillable(layout_columns(!!!list(x, x, x)))
# r2py:entity:page_fillable_1
x_list = [x, x, x]
app2 = page_fillable(
    layout_columns(*x_list)
)

# Equivalent to: page_fillable(layout_columns(col_widths = c(6, 6, 12), x, x, x))
# r2py:entity:page_fillable_2
app3 = page_fillable(
    layout_columns(
        x, x, x,
        col_widths=[6, 6, 12]
    )
)

# Equivalent to: page_fillable(layout_columns(col_widths = c(6, 6, -2, 8), row_heights = c(1, 3), x, x, x))
# Note: In shiny for Python, layout_columns manages the grid; 
# negative widths or specific row_heights are handled via CSS or grid_args in some versions, 
# but the direct mapping is as follows:
# r2py:entity:page_fillable_3
app4 = page_fillable(
    layout_columns(
        x, x, x,
        col_widths=[6, 6, -2, 8],
        row_heights=[1, 3]
    )
)

# Equivalent to: page_fillable(fillable_mobile = TRUE, layout_columns(col_widths = breakpoints(...), x, x, x))
# r2py:entity:page_fillable_4
app5 = page_fillable(
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