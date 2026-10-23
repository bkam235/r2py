from shiny import ui

# r2py:entity:value_box
ui.value_box(
    "KPI Title",
    ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
    ui.span(
        ui.BSIcon("arrow-up"),
        " 30% VS PREVIOUS 30 DAYS"
    ),
    showcase=ui.BSIcon("piggy-bank"),
    theme="success"
)