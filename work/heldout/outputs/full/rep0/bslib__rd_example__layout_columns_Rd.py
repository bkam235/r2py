# Translated from <R script> by r2py v0.3.0

from shiny import ui

# x <- card("A simple card")
# r2py:entity:x
x = ui.card("A simple card")

# page_fillable(layout_columns(x, x, x, x))
# r2py:entity:page_fillable
ui.page_fillable(
    ui.layout_columns(x, x, x, x)
)

# page_fillable(layout_columns(!!!list(x, x, x)))
# r2py:entity:page_fillable_1
ui.page_fillable(
    ui.layout_columns(*[x, x, x])
)

# page_fillable(layout_columns(col_widths = c(6, 6, 12), x, x, x))
# r2py:entity:page_fillable_2
ui.page_fillable(
    ui.layout_columns(x, x, x, col_widths=[6, 6, 12])
)

# page_fillable(layout_columns(col_widths = c(6, 6, -2, 8), row_heights = c(1, 3), x, x, x))
# r2py:entity:page_fillable_3
ui.page_fillable(
    ui.layout_columns(x, x, x, col_widths=[6, 6, -2, 8], row_heights=[1, 3])
)

# page_fillable(fillable_mobile = TRUE, layout_columns(col_widths = breakpoints(...), x, x, x))
# r2py:entity:page_fillable_4
ui.page_fillable(
    ui.layout_columns(
        x, x, x, 
        col_widths={
            "sm": [12, 12, 12],
            "md": [6, 6, 12],
            "lg": [4, 4, 4]
        }
    ),
    fillable_mobile=True
)