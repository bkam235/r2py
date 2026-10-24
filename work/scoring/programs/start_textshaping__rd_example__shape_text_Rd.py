# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from shiny import App, ui, render

# Since textshaping is a specialized R library for glyph positioning/shaping 
# that doesn't have a 1:1 direct high-level equivalent in standard Python data libraries, 
# we approximate the data structure and behavior using a helper logic.

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    # Convert single string to list for consistent processing
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    results = []
    for i, text in enumerate(strings):
        # Split by newline to simulate multi-line shaping
        lines = text.split('\n')
        curr_id = id[i] if id is not None else 1
        curr_size = size[i] if size is not None else 12
        
        for line in lines:
            results.append({
                'id': curr_id,
                'text': line,
                'size': curr_size,
                'length': len(line)
            })
    return pd.DataFrame(results)

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_text
print(shape_text(string))

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]
# r2py:entity:shape_text_1
print(shape_text(string, id=[1, 1, 1], size=[12, 24, 12]))