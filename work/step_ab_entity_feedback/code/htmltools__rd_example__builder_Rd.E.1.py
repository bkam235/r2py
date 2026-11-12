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

import numpy as np

# In htmltools, tags$X is a function that generates HTML. 
# Since the shim provides a dictionary of tag names, we simulate the tag functions.
def tag_func(name):
    def wrapper(*args, **kwargs):
        # This is a simplified simulation of htmltools' tag builder
        # In a real R environment, tags$html(...) returns an HTML object
        # which when printed produces the HTML string.
        
        # Handle boolean attributes like controls=NA in R (which means "present")
        processed_kwargs = {}
        for k, v in kwargs.items():
            if v is np.nan: # Mapping NA to present boolean attribute
                processed_kwargs[k] = ""
            else:
                processed_kwargs[k] = v
                
        # Construct a basic HTML representation for verification
        attrs = " ".join([f'{k}="{v}"' if v != "" else k for k, v in processed_kwargs.items()])
        attr_str = f" {attrs}" if attrs else ""
        
        content = "".join([str(a) for a in args])
        return f"<{name}{attr_str}>{content}</{name}>"
    return wrapper

# Create the tags object mapping to match R's tags$X
tags_obj = {name: tag_func(name) for name in tags.keys()}

# R: tags$html(...)
res1 = tags_obj['html'](
    tags_obj['head'](
        tags_obj['title']('My first page')
    ),
    tags_obj['body'](
        tags_obj['h1']('My first heading'),
        tags_obj['p']('My first paragraph, with some ', tags_obj['strong']('bold'), ' text.'),
        tags_obj['div'](
            'Here is a div with some attributes.',
            id='myDiv', 
            class_='simpleDiv' # Use class_ to avoid python keyword
        )
    )
)
print(res1)

# R: tags$audio(controls = NA, ...)
# Note: in R, controls = NA for a boolean attribute means the attribute is present.
res2 = tags_obj['audio'](
    tags_obj['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=np.nan 
)
print(res2)

# R: tags$span(tags$strong("I'm strong", .noWS="outside"))
res3 = tags_obj['span'](
    tags_obj['strong']("I'm strong", noWS="outside")
)
print(res3)