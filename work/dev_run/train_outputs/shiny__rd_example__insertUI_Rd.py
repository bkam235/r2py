# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, render, ui, reactive

# r2py:entity:interactive
# Part 1: Add UI logic
# r2py:entity:ui
ui_1 = ui.page_fluid(
    ui.input_action_button("add", "Add UI")
)

# r2py:entity:server
def server_1(input, output, session):
    @reactive.effect
    @reactive.event(input.add)
    def _():
        # In shiny for python, dynamic UI is typically handled via ui.output_ui
        # However, to mirror insertUI's behavior of injecting elements:
        session.send_custom_message("insert_ui", {
            "selector": "#add",
            "where": "afterEnd",
            "ui": f'<div class="form-group"><label>Insert some text</label><input id="txt{input.add}" class="form-control" type="text"></div>'
        })

# r2py:entity:shinyApp
app_1 = App(ui_1, server_1)

# r2py:entity:interactive_1
# Part 2: Remove UI logic
# r2py:entity:ui_1
ui_2 = ui.page_fluid(
    ui.input_action_button("rmv", "Remove UI"),
    ui.input_text("txt", "This is no longer useful")
)

# r2py:entity:server_1
def server_2(input, output, session):
    @reactive.effect
    @reactive.event(input.rmv)
    def _():
        # Mirroring removeUI via custom JS message as Python API manages state differently
        session.send_custom_message("remove_ui", {
            "selector": "div:has(> #txt)"
        })

# r2py:entity:shinyApp_1
app_2 = App(ui_2, server_2)

# Note: In a real Python Shiny app, you would typically use ui.output_ui 
# and a reactive value to conditionally render components rather than 
# direct DOM manipulation via insertUI/removeUI.