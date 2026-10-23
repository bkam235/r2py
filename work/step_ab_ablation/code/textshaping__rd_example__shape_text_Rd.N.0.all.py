import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Approximates the R textshaping::shape_text behavior.
    In R, shape_text returns a data frame with columns like x_offset, y_offset, etc.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    # Handle defaults for id and size
    if id is None:
        id = [1] * len(strings)
    if size is None:
        size = [12] * len(strings)
        
    all_glyphs = []
    
    for i in range(len(strings)):
        text = strings[i]
        curr_id = id[i]
        curr_size = size[i]
        
        # Split by newline as textshaping handles lines
        lines = text.split('\n')
        
        for line_idx, line in enumerate(lines):
            # Create dummy glyph data mirroring a shaping output
            for char_idx, char in enumerate(line):
                all_glyphs.append({
                    'id': curr_id,
                    'glyph': char,
                    'x_offset': char_idx * (curr_size * 0.5), # Dummy positioning
                    'y_offset': -line_idx * curr_size,         # Dummy positioning
                    'size': curr_size
                })
    
    return pd.DataFrame(all_glyphs)

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
shape_text(string)

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]

# r2py:entity:shape_text_1
shape_text(string, id=[1, 1, 1], size=[12, 24, 12])