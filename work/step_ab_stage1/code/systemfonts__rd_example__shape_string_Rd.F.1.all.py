# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximate systemfonts::shape_string which returns glyph-level 
    positioning and metrics for the provided strings.
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
    
    # Mock glyph metrics to simulate R's output
    # In reality, this would use a font shaping engine like HarfBuzz
    for s_idx, (text, s_id, s_size) in enumerate(zip(strings, ids, sizes)):
        x_offset = 0
        y_offset = 0
        # Split by lines for y_offset changes
        lines = text.split('\n')
        for line_idx, line in enumerate(lines):
            y_offset = -line_idx * (s_size * 0.8) 
            for char in line:
                # Simple mock: index is ordinal, x_midpoint is half width
                char_width = (s_size * 0.3) # Mock width
                glyph_index = ord(char)
                
                all_glyphs.append({
                    'glyph': char,
                    'index': glyph_index,
                    'metric_id': 0,
                    'string_id': s_idx,
                    'x_offset': x_offset,
                    'y_offset': y_offset,
                    'x_midpoint': x_offset + (char_width / 2)
                })
                x_offset += char_width
            # Reset x_offset for new line
            x_offset = 0
            
    # R's shape_string returns a list/dataframe. 
    # We return a DataFrame with the specific columns seen in the verification output.
    df = pd.DataFrame(all_glyphs)
    # Reordering columns to match R's output: glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint
    return df[['glyph', 'index', 'metric_id', 'string_id', 'x_offset', 'y_offset', 'x_midpoint']]

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