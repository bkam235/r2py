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

# R's tags are functions that return HTML tags. In Python, the shim provides 
# a dictionary of these tags. I will implement a simple wrapper to mirror
# the R tags$tag_name(...) call if necessary, but the shim is intended to be used directly.

def tag_call(tag_name, *args, **kwargs):
    # This simulates the htmltools builder behavior
    # In a real scenario, we would use a library like Dominate or similar, 
    # but we must use the provided tags shim.
    tag_func = tags[tag_name]
    # Since the shim provides the functions, we just call them.
    # However, the shim provided in the prompt is a dict of functions.
    return tag_func(*args, **kwargs)

# tags$html(...)
res1 = tags['html'](
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
print(res1)

# tags$audio(controls = NA, ...)
# In htmltools, controls = NA for a boolean attribute usually means it is present.
res2 = tags['audio'](
    tags['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)
print(res2)

# tags$span(tags$strong("I'm strong", .noWS="outside"))
res3 = tags['span'](
    tags['strong']("I'm strong", noWS="outside")
)
print(res3)