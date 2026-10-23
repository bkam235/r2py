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

# The 'tags' variable is provided by the shim as a dictionary of tag functions.
# In R, tags$html(...) calls the html function.

# First section: HTML structure
# r2py:entity:tags$html
html_result = tags['html'](
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

# Second section: Audio tag
# R: tags$audio(controls = NA, ...) 
# In htmltools, controls = NA creates a boolean attribute 'controls' without a value.
# r2py:entity:tags$audio
audio_result = tags['audio'](
    tags['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True # Boolean attributes in htmltools are typically handled as True/NA
)

# Third section: Span with strong
# r2py:entity:tags$span
span_result = tags['span'](
    tags['strong']("I'm strong", noWS="outside")
)