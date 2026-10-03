# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shiny__rd_example__modalDialog_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tags']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from shiny import App, render, ui, reactive
import pandas as pd

# r2py:entity:interactive
def interactive():
    return True

# --- App 1 ---
# r2py:entity:shinyApp
def server1(input, output, session):
    @reactive.effect
    def _():
        if input.show():
            ui.show_modal(
                ui.modal_dialog(
                    "This is an important message!",
                    title="Important message"
                )
            )

app1 = App(
    ui=ui.page_bootstrap(
        ui.input_action_button("show", "Show modal dialog")
    ),
    server=server1
)

# --- App 2 ---
# r2py:entity:shinyApp_1
def server2(input, output, session):
    @reactive.effect
    def _():
        if input.show():
            ui.show_modal(
                ui.modal_dialog(
                    "This is a somewhat important message.",
                    title="Somewhat important message",
                    easy_close=True,
                    footer=None
                )
            )

app2 = App(
    ui=ui.page_bootstrap(
        ui.input_action_button("show", "Show modal dialog")
    ),
    server=server2
)

# --- App 3 ---
# Mocking some data frames to simulate exists() and get() from R
mtcars = pd.DataFrame({"mpg": [21.0, 21.0], "cyl": [6, 6]})

# r2py:entity:shinyApp_2
def server3(input, output, session):
    vals = reactive.Value(None)

    def data_modal(failed=False):
        return ui.modal_dialog(
            ui.input_text("dataset", "Choose data set", placeholder='Try "mtcars" or "abc"'),
            ui.span('(Try the name of a valid data object like "mtcars", then a name of a non-existent object like "abc")'),
            ui.div(ui.tags.b("Invalid name of data object", style="color: red;")) if failed else None,
            footer=ui.tag_list(
                ui.modal_button("Cancel"),
                ui.input_action_button("ok", "OK")
            )
        )

    @reactive.effect
    def _():
        if input.show():
            ui.show_modal(data_modal())

    @reactive.effect
    def _():
        if input.ok():
            dataset_name = input.dataset()
            # Approximation of R's exists() and get() using globals()
            if dataset_name and dataset_name in globals() and isinstance(globals()[dataset_name], pd.DataFrame):
                vals.set(globals()[dataset_name])
                ui.remove_modal()
            else:
                ui.show_modal(data_modal(failed=True))

    @render.text
    def dataInfo():
        d = vals.get()
        if d is None:
            return "No data selected"
        else:
            return str(d.describe())

app3 = App(
    ui=ui.page_bootstrap(
        ui.input_action_button("show", "Show modal dialog"),
        ui.output_text_verbatim("dataInfo")
    ),
    server=server3
)