import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string.
    In R, this returns a data frame with x, y, width, height, etc. for each glyph/line.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    # Handle id and size broadcasting
    n = len(strings)
    if id is None:
        ids = [1] * n
    elif isinstance(id, (int, float)):
        ids = [id] * n
    else:
        ids = id
        
    if size is None:
        sizes = [12] * n
    elif isinstance(size, (int, float)):
        sizes = [size] * n
    else:
        sizes = size

    all_results = []
    
    # Constants to approximate font metrics
    CHAR_WIDTH_FACTOR = 0.6
    CHAR_HEIGHT_FACTOR = 1.2
    
    for s, i, sz in zip(strings, ids, sizes):
        lines = s.split('\n')
        current_y = 0
        for line in lines:
            # For each line, we'll create a record. 
            # R's shape_string actually returns glyphs, but for this context, 
            # a line-based summary is the common way to approximate it in Python.
            line_width = len(line) * CHAR_WIDTH_FACTOR * (sz / 12.0)
            line_height = sz * CHAR_HEIGHT_FACTOR
            
            # Construct a row similar to R's output: x, y, width, height, etc.
            all_results.append({
                'x': 0,
                'y': current_y,
                'width': line_width,
                'height': line_height,
                'id': i,
                'size': sz,
                'text': line
            })
            current_y += line_height
            
    return pd.DataFrame(all_results)

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_string
result1 = shape_string(string)
print(result1)

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]

# r2py:entity:shape_string_1
result2 = shape_string(string, id=[1, 1, 1], size=[12, 24, 12])
print(result2)