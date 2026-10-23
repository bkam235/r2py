# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/shiny__rd_example__checkboxGroupInput_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shiny__rd_example__checkboxGroupInput_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from shiny import App, render, ui

# Load mtcars dataset (simulated as it is built-in to R)
mtcars_url = "https://gist.githubusercontent.com/seanpm/73f4305508884e9315f7/raw/df9d1e54a393c9415e08122728268f909987329f/mtcars.csv"
d = pd.read_csv(mtcars_url, index_col=0)

# r2py:entity:interactive
# App 1 Implementation
# r2py:entity:ui
ui1 = ui.page_fluid(
    ui.input_checkbox_group(
        "variable", 
        "Variables to show:", 
        choices=[
            {"label": "Cylinders", "value": "cyl"}, 
            {"label": "Transmission", "value": "am"}, 
            {"label": "Gears", "value": "gear"}
        ]
    ),
    ui.output_table("data")
)

# r2py:entity:server
def server1(input, output, session):
    @render.table
    def data():
        cols = ["mpg"] + (input.variable() if input.variable() else [])
        return d[cols]

# r2py:entity:shinyApp
app1 = App(ui1, server1)

# App 2 Implementation
# Note: Shiny for Python handles icons primarily within the UI definition
# r2py:entity:ui_1
ui2 = ui.page_fluid(
    ui.input_checkbox_group(
        "icons", 
        "Choose icons:", 
        choices=[
            {"label": ui.icon("calendar"), "value": "calendar"}, 
            {"label": ui.icon("bed"), "value": "bed"}, 
            {"label": ui.icon("cog"), "value": "cog"}, 
            {"label": ui.icon("bug"), "value": "bug"}
        ]
    ),
    ui.output_text("txt")
)

# r2py:entity:server_1
def server2(input, output, session):
    @render.text
    def txt():
        icons = ", ".join(input.icons()) if input.icons() else ""
        return f"You chose {icons}"

# r2py:entity:shinyApp_1
app2 = App(ui2, server2)

# To run these, one would typically call app1.run() or app2.run()