# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/htmltools__rd_example__builder_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__builder_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tags']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from shiny import ui

# tags$html(...)
html_page = ui.tags.html(
    ui.tags.head(
        ui.tags.title('My first page')
    ),
    ui.tags.body(
        ui.tags.h1('My first heading'),
        ui.tags.p('My first paragraph, with some ', ui.tags.strong('bold'), ' text.'),
        ui.tags.div(
            'Here is a div with some attributes.',
            id='myDiv', 
            class_='simpleDiv'
        )
    ),
    name="tags$html"
)
print(html_page)

# tags$audio(...)
# In htmltools, controls = NA for boolean attributes typically means "present" 
# or is handled specifically by the builder. In shiny.ui, True is used.
audio_element = ui.tags.audio(
    ui.tags.source(
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True,
    name="tags$audio"
)
print(audio_element)

# tags$span(...)
span_element = ui.tags.span(
    ui.tags.strong("I'm strong", .noWS="outside"), 
    name="tags$span"
)
# Note: .noWS is a specific htmltools internal attribute for whitespace suppression.
# Shiny's Python implementation may not support it exactly, but we pass it.
print(span_element)