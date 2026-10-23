# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np

def get_width(x):
    return getattr(x, 'width', None)

def get_min_width(x):
    return getattr(x, 'min_width', get_width(x))

def get_extent(x):
    if isinstance(x, list):
        return [len(str(i)) for i in x]
    return len(str(x))

def get_max_extent(x):
    extents = get_extent(x)
    if isinstance(extents, list):
        return max(extents) if extents else 0
    return extents

# r2py:entity:new_pillar
def new_ornament(x, width=None, align=None):
    if width is None:
        width = get_max_extent(x)
    
    class Ornament:
        pass
    
    ret = Ornament()
    ret.val = x
    ret.align = align
    ret.width = width
    return ret

def new_pillar_component(x, width, min_width=None):
    class Component:
        pass
    
    ret = Component()
    ret.val = x
    ret.width = int(width)
    ret.min_width = int(min_width) if min_width is not None else int(width)
    return ret

def pillar_component(x):
    return new_pillar_component([x], width=get_width(x), min_width=get_min_width(x))

def new_pillar(components, width=None, class_val=None, extra=None):
    class Pillar:
        pass
    
    ret = Pillar()
    ret.components = components
    ret.width = width
    ret.class_val = class_val
    return ret

# r2py:entity:lines
def lines(char_val="-"):
    if len(char_val) != 1:
        raise AssertionError("nchar(char) must be 1")
    
    class Lines:
        pass
    
    l = Lines()
    l.char = char_val
    return l

# r2py:entity:format.lines
def format_lines(x, width, **kwargs):
    return x * width

# The R script creates a custom S3-like behavior for 'lines'.
# To mimic the `format.lines` call that R's printing system would invoke:
# we define the behavior for the object returned by lines().

def render_lines(x, width):
    # This simulates the R logic: paste(rep(x, width), collapse = "")
    # Since 'x' is the result of lines("="), we access its char property
    char = x.char if hasattr(x, 'char') else x
    return char * width

# Main Execution
# r2py:entity:new_pillar
res = new_pillar({
    "title": pillar_component(new_ornament(["abc", "de"], align="right")),
    "lines": new_pillar_component([lines("=")], width=1)
})

print(res)