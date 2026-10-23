# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/htmltools__rd_example__withTags_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__withTags_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tags']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from shiny import ui

# Translation of tags$div(...)
# r2py:entity:tags$div
ui.div(
    ui.h3("header"),
    ui.p("text"),
    class_="myclass"
)

# Translation of withTags(div(...))
# Note: In Python Shiny, with_tags (or the implied context) is used 
# similarly, but most layout components are standalone functions.
# r2py:entity:withTags
ui.div(
    ui.h3("header"),
    ui.p("text"),
    class_="myclass"
)

# Translation of withTags(div(...), .noWS = ...)
# Note: .noWS (no whitespace) is a low-level R htmltools feature 
# that does not have a direct equivalent in the high-level Python Shiny API.
# Standard UI components handle spacing via CSS.
# r2py:entity:withTags_1
ui.div(
    ui.h3("header"),
    ui.p(
        "One", 
        ui.strong(ui.span("two")), 
        "three"
    ),
    class_="myclass"
)