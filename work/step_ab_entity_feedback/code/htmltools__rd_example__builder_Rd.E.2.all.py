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

def tag_builder(name):
    def builder(*args, **kwargs):
        # Handle boolean attributes like controls = NA in R (which means present)
        attrs = []
        for k, v in kwargs.items():
            if v is None or (isinstance(v, float) and np.isnan(v)):
                attrs.append(f'{k}')
            elif v is True:
                attrs.append(f'{k}')
            elif v is False:
                pass
            else:
                attrs.append(f'{k}="{v}"')
        
        attr_str = f" { ' '.join(attrs) }" if attrs else ""
        
        # Process children (args)
        content = ""
        for arg in args:
            if hasattr(arg, 'render'):
                content += arg.render()
            elif isinstance(arg, str):
                content += arg
            else:
                content += str(arg)
        
        return Tag(name, content, attr_str)
    return builder

class Tag:
    def __init__(self, name, content, attr_str):
        self.name = name
        self.content = content
        self.attr_str = attr_str

    def render(self):
        return f"<{self.name}{self.attr_str}>{self.content}</{self.name}>"
    
    def __str__(self):
        return self.render()

# Mimic htmltools tags object
tags = {name: tag_builder(name) for name in ['html', 'head', 'title', 'body', 'h1', 'p', 'strong', 'div', 'audio', 'source', 'span']}

# R: tags$html(...)
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
            class_='simpleDiv' # R's class is handled as class_ in many py-libs or just 'class'
        )
    )
)
# Fix class attribute name to 'class' for HTML output
# In a real implementation, tag_builder would handle mapping class_ -> class
def fix_class(html):
    return html.replace('class_="', 'class="')

print(fix_class(res1.render()))

# R: tags$audio(controls = NA, ...)
# In R, controls = NA for a boolean attribute means the attribute is present.
res2 = tags['audio'](
    tags['source'](
        src="myfile.wav",
        type="audio/wav"
    ),
    controls=True # mapping NA to True for presence
)
print(res2.render())

# R: tags$span(tags$strong("I'm strong", .noWS="outside"))
# .noWS is an internal htmltools attribute to suppress whitespace.
res3 = tags['span'](
    tags['strong']("I'm strong")
)
print(res3.render())