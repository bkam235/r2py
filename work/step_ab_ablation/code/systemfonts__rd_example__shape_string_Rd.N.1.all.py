# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Shim for systemfonts::shape_string.
    R's shape_string returns a data frame where each row is a glyph.
    We simulate this by creating entries for each character.
    """
    # Default settings
    default_size = 12
    
    # Normalize inputs to lists
    if isinstance(string, str):
        strings = [string]
    else:
        strings = list(string)
        
    if id is None:
        ids = [1] * len(strings)
    elif isinstance(id, (int, float)):
        ids = [id] * len(strings)
    else:
        ids = list(id)
        
    if size is None:
        sizes = [default_size] * len(strings)
    elif isinstance(size, (int, float)):
        sizes = [size] * len(strings)
    else:
        sizes = list(size)

    all_glyphs = []
    
    # Simulating font metrics: basic proportional approximation
    # In R, shape_string provides precise glyph positions.
    for s, i, sz in zip(strings, ids, sizes):
        current_x = 0.0
        current_y = 0.0
        # Basic scale factor relative to size 12
        scale = sz / 12.0
        
        for char in s:
            # Approximate dimensions for the glyph
            char_w = 0.5 * scale if char != ' ' else 0.3 * scale
            char_h = 0.8 * scale
            
            all_glyphs.append({
                'id': i,
                'char': char,
                'x_start': current_x,
                'x_advance': char_w,
                'y_start': current_y,
                'y_advance': 0, # simplified
                'width': char_w,
                'height': char_h,
                'size': sz
            })
            
            current_x += char_w
            if char == '\n':
                current_x = 0.0
                current_y -= char_h # Move down for next line
                
    return pd.DataFrame(all_glyphs)

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_string
# In R, this would print to console. We wrap in print() to match behavior.
print(shape_string(string))

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]

# r2py:entity:shape_string_1
print(shape_string(string, id=[1, 1, 1], size=[12, 24, 12]))