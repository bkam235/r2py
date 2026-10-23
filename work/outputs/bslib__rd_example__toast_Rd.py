# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

from shiny import App, ui, render, reactive
from shiny.express import ui as ui_expr

# Note: Python's shiny implementation handles toasts via the session.show_toast method
# There is no direct equivalent to bslib's complex toast_header structure, 
# so we use the standard notification/toast system.

# r2py:entity:ui
app_ui = ui.page_fluid(
    ui.input_action_button("show_simple", "Simple Toast"),
    ui.input_action_button("show_header", "Toast with Header"),
)

# r2py:entity:server
def server(input, output, session):
    @reactive.Effect.set_source(input.show_simple)
    def _():
        session.show_toast(
            "Operation completed successfully!",
            type="success"
        )

    @reactive.Effect.set_source(input.show_header)
    def _():
        # Using a combined string to simulate the header/status behavior
        session.show_toast(
            "Settings Updated (just now): Your settings have been saved.",
            type="success"
        )

# r2py:entity:shinyApp
app = App(app_ui, server)