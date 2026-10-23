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

import numpy as np

# In R, tags$html(...) is a function call. The shim provides tags as a dictionary
# of functions that produce HTML fragments.

# First section: HTML structure
# tags$html(tags$head(tags$title('My first page')), tags$body(...))
html_out = tags['html'](
    tags['head'](
        tags['title']('My first page')
    ),
    tags['body'](
        tags['h1']('My first heading'),
        tags['p']('My first paragraph, with some ', tags['strong']('bold'), ' text.'),
        tags['div'](
            'Here is a div with some attributes.',
            id='myDiv', 
            class_='simpleDiv'
        )
    )
)
print(html_out)

# Second section: Audio tag
# tags$audio(controls = NA, tags$source(src = "myfile.wav", type = "audio/wav"))
# In htmltools, controls = NA for boolean attributes often means "present"
audio_out = tags['audio'](
    tags['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)
print(audio_out)

# Third section: Span with strong
# tags$span(tags$strong("I'm strong", .noWS="outside"))
span_out = tags['span'](
    tags['strong']("I'm strong", noWS="outside")
)
print(span_out)