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

# First section: HTML structure
# r2py:entity:tags$html
html_page = ui.HTML(
    """
    <html>
      <head>
        <title>My first page</title>
      </head>
      <body>
        <h1>My first heading</h1>
        <p>My first paragraph, with some <strong>bold</strong> text.</p>
        <div id="myDiv" class_val="simpleDiv">
          Here is a div with some attributes.
        </div>
      </body>
    </html>
    """
)

# Second section: Audio tag
# r2py:entity:tags$audio
audio_element = ui.tags.audio(
    ui.tags.source(
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)

# Third section: Span with strong
# r2py:entity:tags$span
span_element = ui.tags.span(
    ui.tags.strong("I'm strong")
)