# Translated from <R script> by r2py v0.3.0

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

# The R code uses tags$html(...) etc. 
# The data_shim provides 'tags' as a dictionary of tag functions.
# We should use these functions to build the HTML.

# First section: tags$html
# Note: htmltools tags can be called as functions. 
# In Python shiny.ui.tags is the equivalent.
html_result = ui.tags.html(
    ui.tags.head(
        ui.tags.title('My first page')
    ),
    ui.tags.body(
        ui.tags.h1('My first heading'),
        ui.tags.p('My first paragraph, with some ', ui.tags.strong('bold'), ' text.'),
        ui.tags.div(
            'Here is a div with some attributes.',
            id='myDiv', 
            class_val='simpleDiv' # R's class is reserved in Python
        )
    )
)
print(html_result)

# Second section: tags$audio with boolean control attribute
# controls = NA in htmltools often means "presence of the attribute regardless of value"
# for boolean attributes in HTML5.
audio_result = ui.tags.audio(
    ui.tags.source(
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)
print(audio_result)

# Third section: tags$span with .noWS="outside"
# .noWS is a special attribute in htmltools to suppress whitespace.
span_result = ui.tags.span(
    ui.tags.strong("I'm strong", noWS="outside")
)
print(span_result)