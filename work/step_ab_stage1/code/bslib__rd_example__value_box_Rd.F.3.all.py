from shiny import ui

# r2py:entity:value_box
# R's value_box and bs_icon are available in shiny.ui
res = ui.value_box(
    "KPI Title",
    ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
    ui.span(
        ui.bs_icon("arrow-up"),
        " 30% VS PREVIOUS 30 DAYS"
    ),
    showcase=ui.bs_icon("piggy-bank"),
    theme="success"
)
print(res)