from shiny import ui

# r2py:entity:value_box
# In R, value_box is auto-printed. In Python, we must call print() to match this behavior.
# bsicons::bs_icon produces SVGs; while we use HTML icons, we ensure the structure matches.
print(
    ui.value_box(
        "KPI Title",
        ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
        ui.span(
            ui.HTML('<i class="bi bi-arrow-up"></i>'),
            " 30% VS PREVIOUS 30 DAYS"
        ),
        showcase=ui.HTML('<i class="bi bi-piggy-bank"></i>'),
        theme="success"
    )
)