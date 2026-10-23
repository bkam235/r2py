# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'bslib__rd_example__page_fillable_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from shiny import App, render, ui
from plotnine import ggplot, aes, geom_bar, geom_point
import pandas as pd

# Global data preparation to match R's logic inside the server loop but applied once
# R does: for (var in c("cyl", "vs", "am", "gear", "carb")) { mtcars[[var]] <- as.factor(mtcars[[var]]) }
# In Python we do this on a copy or directly if allowed
for var in ["cyl", "vs", "am", "gear", "carb"]:
    mtcars[var] = mtcars[var].astype(str)

# Columns for the select inputs (mtcars[-7] in R removes the 7th column 'qsec')
# mtcars columns are: ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
# Index 6 is 'qsec'.
choices = [col for i, col in enumerate(mtcars.columns) if i != 6]

ui = ui.page_fillable(
    ui.h1("Example", ui.code("mtcars"), "dashboard"),
    ui.layout_columns(
        ui.card(
            ui.card_header("Number of forward gears"),
            ui.output_plot("gear"),
            full_screen=True
        ),
        ui.card(
            ui.card_header("Number of carburetors"),
            ui.output_plot("carb"),
            full_screen=True
        )
    ),
    ui.card(
        ui.card_header("Weight vs. Quarter Mile Time"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select("var_x", "Compare to qsec:", choices, selected="wt"),
                ui.input_select("color", "Color by:", choices, selected="cyl"),
                position="right"
            ),
            ui.output_plot("var_vs_qsec"),
        ),
        full_screen=True
    )
)

def server(input, output, session):
    @render.plot
    def gear():
        return ggplot(mtcars, aes(x="gear")) + geom_bar()

    @render.plot
    def carb():
        return ggplot(mtcars, aes(x="carb")) + geom_bar()

    @render.plot
    def var_vs_qsec():
        var_x = input.var_x()
        color_var = input.color()
        
        if var_x is None or color_var is None:
            return None
            
        return ggplot(mtcars, aes(x=var_x, y="qsec", color=color_var)) + geom_point()

app = App(ui, server)