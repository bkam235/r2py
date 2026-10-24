# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from shiny import ui

# In bslib (R), bs_icon is used. bsicons produces SVG paths.
# We use HTML for the icons to match the R output's SVG structure.
# r2py:entity:value_box
result = ui.div(
    ui.value_box(
        "KPI Title",
        ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
        ui.span(
            ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.146a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/></svg>'),
            " 30% VS PREVIOUS 30 DAYS"
        ),
        showcase=ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-piggy-bank" viewBox="0 0 16 16"><path d="M7 14.5V12a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v2.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5z"/><path d="M3 5.5A.5.5 0 0 1 3.5 5h10a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5v-7zM3 4a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1h-12V4z"/></svg>'),
        theme="success"
    ),
    class_="container-fluid"
)

print(result)