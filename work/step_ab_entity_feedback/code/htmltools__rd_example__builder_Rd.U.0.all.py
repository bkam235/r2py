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

# In R, htmltools tags are functions. In this Python environment, 
# the 'tags' dictionary provided by the shim contains the tag names.
# We simulate the builder behavior.
class Tag:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        # Simple representation to match expected HTML output
        attrs = " ".join([f'{k}="{v}"' for k, v in self.kwargs.items() if v is not None])
        attr_str = f" {attrs}" if attrs else ""
        content = "".join([str(a) for a in self.args])
        return f"<{self.name}{attr_str}>{content}</{self.name}>"

def get_tag(name):
    return lambda *args, **kwargs: Tag(name, *args, **kwargs)

# Mapping the tags dictionary to functions
tag_funcs = {name: get_tag(name) for name in tags.keys()}

# Aliases for the source code
html = tag_funcs['html']
head = tag_funcs['head']
title = tag_funcs['title']
body = tag_funcs['body']
h1 = tag_funcs['h1']
p = tag_funcs['p']
strong = tag_funcs['strong']
div = tag_funcs['div']
audio = tag_funcs['audio']
source = tag_funcs['source']
span = tag_funcs['span']

# First section: HTML structure
res1 = html(
    head(
        title('My first page')
    ),
    body(
        h1('My first heading'),
        p('My first paragraph, with some ', strong('bold'), ' text.'),
        div(
            'Here is a div with some attributes.',
            id='myDiv', class_='simpleDiv'
        )
    )
)
print(res1)

# Second section: Audio tag
# controls = NA in R's htmltools often represents a boolean attribute presence
res2 = audio(
    source(
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True
)
print(res2)

# Third section: Span with strong
res3 = span(
    strong("I'm strong", noWS="outside")
)
print(res3)