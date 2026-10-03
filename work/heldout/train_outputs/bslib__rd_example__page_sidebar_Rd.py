# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/bslib__rd_example__page_sidebar_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'bslib__rd_example__page_sidebar_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from shiny import App, ui, render, reactive
from plotnine import ggplot, aes, geom_histogram
from plotnine.data import mtcars

# Load data
mtcars_df = mtcars

# Define the User Interface
# r2py:entity:ui
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "var", 
            "Select variable", 
            choices=list(mtcars_df.columns)
        )
    ),
    ui.card(
        ui.card_header("My plot"),
        ui.output_plot("p"),
        full_screen=True
    ),
    title="Example dashboard"
)

# Define the Server logic
# r2py:entity:server
def server(input, output, session):
    @render.plot
    def p():
        # input.var() returns the currently selected column name
        selected_var = input.var()
        return (
            ggplot(mtcars_df) 
            + geom_histogram(aes(x=selected_var))
        )

# Create and run the Shiny App
# r2py:entity:shinyApp
app = App(ui=app_ui, server=server)