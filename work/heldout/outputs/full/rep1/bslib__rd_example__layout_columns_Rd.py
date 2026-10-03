from shiny import ui
from shiny.ui import page_fillable, layout_columns, card

# r2py:entity:x
x = card("A simple card")

# Page 1
# r2py:entity:page_fillable
page_fillable(
    layout_columns(x, x, x, x)
)

# Page 2
# r2py:entity:page_fillable_1
page_fillable(
    layout_columns(*[x, x, x])
)

# Page 3
# r2py:entity:page_fillable_2
page_fillable(
    layout_columns(
        x, x, x, 
        col_widths=[6, 6, 12]
    )
)

# Page 4
# r2py:entity:page_fillable_3
page_fillable(
    layout_columns(
        x, x, x, 
        col_widths=[6, 6, -2, 8], 
        row_heights=[1, 3]
    )
)

# Page 5
# r2py:entity:page_fillable_4
def breakpoints(**kwargs):
    """Helper to mimic bslib::breakpoints"""
    return kwargs

page_fillable(
    layout_columns(
        x, x, x, 
        col_widths=breakpoints(
            sm=[12, 12, 12],
            md=[6, 6, 12],
            lg=[4, 4, 4]
        )
    ), 
    fillable_mobile=True
)