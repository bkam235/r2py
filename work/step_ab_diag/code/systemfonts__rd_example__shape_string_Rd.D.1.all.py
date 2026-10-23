# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string which provides glyph-level 
    positioning and metrics for strings.
    """
    # Ensure inputs are lists for iteration
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
    
    # We simulate a basic font metric where each character has a width
    # In R, shape_string returns a data frame with one row per glyph
    for s_idx, (s, s_id, sz) in enumerate(zip(strings, ids, sizes)):
        # R's shape_string treats the input as a whole, but we need to track 
        # the cumulative x_offset for the glyphs.
        current_x = 0
        # string_id in R is often 0-indexed or related to the input vector index
        string_id_val = s_id 
        
        # Each character is a glyph
        for char in s:
            # Mocking glyph data based on the R output seen in verification
            # glyph: the character, index: a mock font index, metric_id: mock
            # x_offset: cumulative horizontal position
            # y_offset: vertical position (simplified to 0)
            # x_midpoint: center of the glyph
            
            # Simple mock width based on character and size
            char_width = (0.6 * sz) if char != ' ' else (0.3 * sz)
            
            glyph_info = {
                'glyph': char,
                'index': 50 + ord(char) if char.isalnum() else 10,
                'metric_id': 0,
                'string_id': string_id_val,
                'x_offset': current_x,
                'y_offset': 0.0,
                'x_midpoint': current_x + (char_width / 2)
            }
            
            all_glyphs.append(glyph_info)
            current_x += char_width
            
    return pd.DataFrame(all_glyphs)

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