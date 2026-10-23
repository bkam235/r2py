# Translated from <R script> by r2py v0.3.0

# r2py:data_shim managed by the harness (loads R's input data) - do not write it
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

# mtcars is loaded by shim
mtcars = pd.DataFrame(mtcars)

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
                    # mtcars[-7] in R removes the 7th column (qsec)
                    [col for i, col in enumerate(mtcars.columns) if i != 6], 
                    selected="wt"
                ), 
                ui.input_select(
                    "color", 
                    "Color by:", 
                    [col for i, col in enumerate(mtcars.columns) if i != 6], 
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
    # Copy mtcars to avoid mutating global df inside server logic if needed, 
    # but R does it on the global mtcars.
    global mtcars
    for var in ["cyl", "vs", "am", "gear", "carb"]:
        mtcars[var] = mtcars[var].astype(str)

    @render.plot
    def gear():
        return (
            ggplot(mtcars, aes(x="gear")) 
            + geom_bar()
        )

    @render.plot
    def carb():
        return (
            ggplot(mtcars, aes(x="carb")) 
            + geom_bar()
        )

    @render.plot
    def var_vs_qsec():
        var_x = input.var_x()
        color_var = input.color()
        
        # Equivalent to req(input$var_x, input$color)
        if var_x is None or color_var is None:
            return None
            
        return (
            ggplot(mtcars, aes(x=var_x, y="qsec", color=color_var)) 
            + geom_point()
        )

# r2py:entity:shinyApp
app = App(ui, server)