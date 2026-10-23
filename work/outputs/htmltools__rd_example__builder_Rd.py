# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/htmltools__rd_example__builder_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__builder_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tags']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from shiny import ui

# HTML Document structure
# r2py:entity:tags$html
page_content = ui.tags.html(
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
    )
)
print(page_content)

# Audio element
# In htmltools, controls = NA creates a boolean attribute (just 'controls')
# r2py:entity:tags$audio
audio_element = ui.tags.audio(
    ui.tags.source(
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)
print(audio_element)

# Span with strong text
# .noWS="outside" in R suppresses whitespace around the tag. 
# shiny.ui.tags generally does not have a direct .noWS equivalent in the Python API, 
# but we maintain the structure.
# r2py:entity:tags$span
span_element = ui.tags.span(
    ui.tags.strong("I'm strong")
)
print(span_element)