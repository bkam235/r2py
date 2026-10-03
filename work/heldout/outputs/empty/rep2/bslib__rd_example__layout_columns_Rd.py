from shiny import ui

# r2py:entity:x
x = ui.card("A simple card")

# First section: 4 equal columns
# r2py:entity:page_fillable
ui.page_fillable(
    ui.layout_columns(x, x, x, x)
)

# Second section: Dynamic list of 3 cards
# r2py:entity:page_fillable_1
cards_list = [x, x, x]
ui.page_fillable(
    ui.layout_columns(*cards_list)
)

# Third section: Specific col_widths (6, 6, 12)
# r2py:entity:page_fillable_2
ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths=[6, 6, 12]
    )
)

# Fourth section: col_widths with negative values and row_heights
# r2py:entity:page_fillable_3
ui.page_fillable(
    ui.layout_columns(
        x, x, x,
        col_widths=[6, 6, -2, 8],
        row_heights=[1, 3]
    )
)

# Fifth section: Responsive breakpoints
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