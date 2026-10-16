from shiny import ui

# In bslib (R), bs_icon is used. In Python shiny, there isn't a direct 1:1 bsicons port,
# so we use HTML for the icons to match the R output.
def bs_icon(name):
    return ui.HTML(f'<i class="bi bi-{name}"></i>')

# r2py:entity:value_box
print(
    ui.value_box(
        "KPI Title",
        ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
        ui.span(
            bs_icon("arrow-up"),
            " 30% VS PREVIOUS 30 DAYS"
        ),
        showcase=bs_icon("piggy-bank"),
        theme="success"
    )
)