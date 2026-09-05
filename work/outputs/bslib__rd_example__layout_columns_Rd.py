# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

from shiny import App, ui

# r2py:entity:x
x = ui.card("A simple card")

# r2py:entity:page_fillable
print(ui.page_fillable(
    ui.layout_columns(x, x, x, x)
))

# Or add a list of items, spliced with rlang's `!!!` operator
# r2py:entity:page_fillable_1
print(ui.page_fillable(
    ui.layout_columns(*[x, x, x])
))

# r2py:entity:page_fillable_2
print(ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths=[6, 6, 12]
    )
))

# r2py:entity:page_fillable_3
print(ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths=[6, 6, -2, 8],
        row_heights=[1, 3]
    )
))

# r2py:entity:page_fillable_4
print(ui.page_fillable(ui.layout_columns(
        x, x, x,
        col_widths={
            "sm": [12, 12, 12],
            "md": [6, 6, 12],
            "lg": [4, 4, 4]
        }
    ), fillable_mobile=True))

# Note: R source has a global scope execution pattern; 
# since this is a UI example, we output the fragments.