from shiny import ui

# r2py:entity:value_box
value_box = ui.value_box(
    "KPI Title",
    ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
    ui.span(
        ui.HTML('<i class="bi bi-arrow-up"></i>'),
        " 30% VS PREVIOUS 30 DAYS"
    ),
    showcase=ui.HTML('<i class="bi bi-piggy-bank"></i>'),
    theme="success"
)

print(value_box)