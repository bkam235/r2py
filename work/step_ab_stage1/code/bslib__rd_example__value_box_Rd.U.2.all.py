# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from shiny import ui

# In bslib (R), bs_icon is used. In Python shiny, there isn't a direct 1:1 bsicons port,
# so we use HTML for the icons to match the R output.
# r2py:entity:value_box
result = ui.value_box(
    "KPI Title",
    ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
    ui.span(
        ui.HTML('<i class="bi bi-arrow-up"></i>'),
        " 30% VS PREVIOUS 30 DAYS"
    ),
    showcase=ui.HTML('<i class="bi bi-piggy-bank"></i>'),
    theme="success"
)
print(result)