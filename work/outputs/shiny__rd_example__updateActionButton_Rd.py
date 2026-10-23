# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

from shiny import App, render, ui, reactive

# r2py:entity:ui
app_ui = ui.page_fluid(
    ui.input_action_button("update", "Update other buttons and link"),
    ui.tags.br(),
    ui.input_action_button("goButton", "Go"),
    ui.tags.br(),
    ui.input_action_button("goButton2", "Go 2"),
    ui.tags.br(),
    ui.input_action_button("goButton3", "Go 3"),
    ui.tags.br(),
    ui.input_action_button("goLink", "Go Link")
)

# r2py:entity:server
def server(input, output, session):
    @reactive.effect
    def _():
        # Triggered when 'update' button is clicked
        if input.update():
            # Update goButton label
            ui.update_action_button("goButton", label="New label")
            
            # Update goButton2 (Removing icon equivalent is handled by label update in shiny-python)
            ui.update_action_button("goButton2", label="Go 2")
            
            # Update goButton3 label
            ui.update_action_button("goButton3", label="New label 3")
            
            # Update goLink label
            ui.update_action_button("goLink", label="New link label")

# r2py:entity:shinyApp
app = App(app_ui, server)