# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'bslib__rd_example__page_fillable_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from shiny import App, render, ui, reactive
from plotnine import ggplot, aes, geom_bar, geom_point
import pandas as pd

# r2py:entity:ui
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
        ),
    ),
    ui.card(
        ui.card_header("Weight vs. Quarter Mile Time"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select(
                    "var_x", 
                    "Compare to qsec:", 
                    [col for col in mtcars.columns if col != "qsec"], 
                    selected="wt"
                ), 
                ui.input_select(
                    "color", 
                    "Color by:", 
                    [col for col in mtcars.columns if col != "qsec"], 
                    selected="cyl"
                ), 
                position="right"
            ),
            ui.output_plot("var_vs_qsec"),
        ), 
        full_screen=True
    ),
)

# r2py:entity:server
def server(input, output, session):
    # Create a local copy and convert to factors to avoid modifying global shim data
    df = mtcars.copy()
    vars_to_factor = ["cyl", "vs", "am", "gear", "carb"]
    for var in vars_to_factor:
        df[var] = df[var].astype(str)

    @render.plot
    def gear():
        return (
            ggplot(df, aes(x="gear")) 
            + geom_bar()
        )

    @render.plot
    def carb():
        return (
            ggplot(df, aes(x="carb")) 
            + geom_bar()
        )

    @render.plot
    def var_vs_qsec():
        var_x = input.var_x()
        color_var = input.color()
        
        if var_x is None or color_var is None:
            return None
            
        return (
            ggplot(df, aes(x=var_x, y="qsec", color=color_var)) 
            + geom_point()
        )

# r2py:entity:shinyApp
app = App(ui, server)