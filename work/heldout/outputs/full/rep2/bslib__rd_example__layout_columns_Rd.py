# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

from shiny import ui

# r2py:entity:x
x = ui.card("A simple card")

# Example 1: Simple columns
# r2py:entity:page_fillable
ui.page_fillable(
    ui.layout_columns(x, x, x, x)
)

# Example 2: List unpacking (equivalent to !!!list() in R)
# r2py:entity:page_fillable_1
cards_list = [x, x, x]
ui.page_fillable(
    ui.layout_columns(*cards_list)
)

# Example 3: Specific column widths
# r2py:entity:page_fillable_2
ui.page_fillable(
    ui.layout_columns(x, x, x, col_widths=[6, 6, 12])
)

# Example 4: Complex column widths and row heights
# r2py:entity:page_fillable_3
ui.page_fillable(
    ui.layout_columns(x, x, x, col_widths=[6, 6, -2, 8], row_heights=[1, 3])
)

# Example 5: Responsive breakpoints
# r2py:entity:page_fillable_4
def breakpoints(**kwargs):
    return kwargs

ui.page_fillable(
    ui.layout_columns(
        x, x, x, 
        col_widths=breakpoints(
            sm=[12, 12, 12],
            md=[6, 6, 12],
            lg=[4, 4, 4]
        )
    ), 
    fillable_mobile=True
)