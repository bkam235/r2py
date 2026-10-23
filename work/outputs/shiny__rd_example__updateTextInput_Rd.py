# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

from shiny import App, render, ui

# r2py:entity:ui
app_ui = ui.page_fluid(
    ui.input_slider("controller", "Controller", min=0, max=20, value=10),
    ui.input_text("inText", "Input text"),
    ui.input_text("inText2", "Input text 2"),
)

# r2py:entity:server
def server(input, output, session):
    @render.reactive
    def update_texts():
        x = input.controller()
        
        # Update values and labels using session.send_input_message or similar mechanisms
        # In Python Shiny, we use ui.update_text
        ui.update_text("inText", value=f"New text {x}")
        ui.update_text("inText2", label=f"New label {x}", value=f"New text {x}")

    # create a reactive effect to trigger the updates
    from shiny import reactive
    reactive.effect(update_texts)

# r2py:entity:shinyApp
app = App(app_ui, server)