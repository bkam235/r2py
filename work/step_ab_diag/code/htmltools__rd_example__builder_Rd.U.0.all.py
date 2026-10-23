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

# suppressPackageStartupMessages(library(htmltools))
# Handled by imports

# tags$html(...)
html_expr = ui.tags.html(
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
print(html_expr)

# tags$audio(...)
# controls = NA in R htmltools typically means the attribute is present (boolean)
audio_expr = ui.tags.audio(
    ui.tags.source(
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)
print(audio_expr)

# tags$span(...)
span_expr = ui.tags.span(
    ui.tags.strong("I'm strong", .noWS="outside") # Note: .noWS is a special internal htmltools arg, usually ignored or handled by the renderer
)
# Since .noWS is not a standard HTML attribute but a hint to R's builder, 
# we translate it as is or omit if the Python API doesn't support it. 
# To be safe and avoid crash, we use a kwargs approach if possible.
span_expr = ui.tags.span(
    ui.tags.strong("I'm strong")
)
print(span_expr)