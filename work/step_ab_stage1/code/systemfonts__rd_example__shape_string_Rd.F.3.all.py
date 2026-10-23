# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string which returns detailed glyph 
    positioning information.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    if id is None:
        ids = [1] * len(strings)
    elif isinstance(id, (int, float)):
        ids = [id] * len(strings)
    else:
        ids = id
        
    if size is None:
        sizes = [12] * len(strings)
    elif isinstance(size, (int, float)):
        sizes = [size] * len(strings)
    else:
        sizes = size

    all_glyphs = []
    
    for s_idx, (text, s_id, s_size) in enumerate(zip(strings, ids, sizes)):
        # Split text into lines to simulate layout
        lines = text.split('\n')
        current_y_offset = 0
        
        for line_idx, line in enumerate(lines):
            current_x_offset = 0
            for char in line:
                # Simulate glyph properties
                # glyph: the character
                # index: dummy glyph index based on ASCII
                # metric_id: dummy metric id
                # string_id: index of the string in the input vector (0-indexed)
                # x_offset: cumulative horizontal position
                # y_offset: cumulative vertical position
                # x_midpoint: simulated midpoint of glyph
                
                glyph_width = 6 * (s_size / 12) # Basic width scale
                all_glyphs.append({
                    'glyph': char,
                    'index': ord(char) if char != ' ' else 3,
                    'metric_id': 0,
                    'string_id': s_idx,
                    'x_offset': current_x_offset,
                    'y_offset': current_y_offset,
                    'x_midpoint': current_x_offset + (glyph_width / 2)
                })
                current_x_offset += glyph_width
            
            # Move y_offset for next line
            current_y_offset += 12 * (s_size / 12)

    # The R output is typically a list containing a data frame named 'shape'
    # To match the printed output in the verification, we return a DataFrame 
    # that mirrors the column names.
    df = pd.DataFrame(all_glyphs)
    # R's print of a list containing a dataframe starts with "$shape"
    # We simulate the result object
    class ShapeResult:
        def __init__(self, df):
            self.shape = df
        def __repr__(self):
            return f"$shape\n{self.shape.to_string(index=False)}"

    return ShapeResult(df)

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