# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from shiny import App, ui, render

# Note: systemfonts::shape_string in R calculates the bounding box/dimensions 
# of text given a font and size. Python does not have a direct 1:1 
# library for this specific metadata extraction without a GUI backend.
# We approximate the logic using a simulated function that calculates 
# dimensions based on average character widths.

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    # Approximation of text shaping/measurement
    # In a real scenario, one would use PIL.ImageFont.getbbox or matplotlib.text
    avg_char_width = 0.5 
    avg_char_height = 0.8
    
    results = []
    
    # Handle case where string is a single value or a list
    if isinstance(string, str):
        strings = [string]
        ids = [1] if id is None else [id]
        sizes = [12] if size is None else [size]
    else:
        strings = string
        ids = id if id is not None else list(range(1, len(strings) + 1))
        sizes = size if size is not None else [12] * len(strings)

    for s, i, sz in zip(strings, ids, sizes):
        lines = s.split('\n')
        for line in lines:
            width = len(line) * avg_char_width * (sz / 12)
            height = avg_char_height * sz
            results.append({
                'id': i,
                'text': line,
                'width': width,
                'height': height,
                'size': sz
            })
            
    return pd.DataFrame(results)

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
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