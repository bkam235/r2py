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

# Use the tags dictionary provided by the data shim to simulate the R tags$X calls
# In R, tags$html(...) is a function call. Here we treat tags['html'] as the constructor.

# First section
tags_html = tags['html'](
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

# Second section: html5 <audio> with boolean control attribute
# In htmltools, controls = NA results in the attribute being present
tags_audio = tags['audio'](
    tags['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=None # Using None/NA to represent boolean attribute presence
)

# Third section: suppress the whitespace between tags
tags_span = tags['span'](
    tags['strong']("I'm strong", .noWS="outside")
)