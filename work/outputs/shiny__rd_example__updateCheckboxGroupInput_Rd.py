# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 6

from shiny import App, ui
from shiny.render import ui as ui_render

# r2py:entity:ui
app_ui = ui.page_fluid(
    ui.p("The first checkbox group controls the second"),
    ui.input_checkbox_group(
        "inCheckboxGroup", 
        "Input checkbox", 
        choices=["Item A", "Item B", "Item C"]
    ),
    ui.input_checkbox_group(
        "inCheckboxGroup2", 
        "Input checkbox 2", 
        choices=["Item A", "Item B", "Item C"]
    )
)

# r2py:entity:server
def server(input_val, output_val, session):
    @session.observe
    def _():
        x = input_val.inCheckboxGroup()

        # Can use empty list to remove all choices
        if x is None:
            x = []

        # Can also set the label and select items
        ui.update_checkbox_group(
            "inCheckboxGroup2",
            label=f"Checkboxgroup label {len(x)}",
            choices=x,
            selected=x
        )

# r2py:entity:shinyApp
app = App(app_ui, server)