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

# R: suppressPackageStartupMessages(library(htmltools))
# (Handled by shim and imports)

# r2py:entity:tags$html
# In R, tags$html(...) builds an HTML tree. 
# We use the functions provided in the 'tags' dictionary from the shim.
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
            class_='simpleDiv' # Use class_ to avoid python keyword conflict
        )
    )
)
print(html_result)

# r2py:entity:tags$audio
# R: tags$audio(controls = NA, ...) 
# In htmltools, controls=NA for a boolean attribute means it's present.
audio_result = tags['audio'](
    tags['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True # Boolean attribute presence
)
print(audio_result)

# r2py:entity:tags$span
# R: tags$span(tags$strong("I'm strong", .noWS="outside"))
span_result = tags['span'](
    tags['strong']("I'm strong", noWS="outside")
)
print(span_result)