import pandas as pd
import numpy as np

# Note: systemfonts::shape_string uses HarfBuzz to shape text.
# In Python, uharfbuzz provides the shaping engine. 
# We simulate the output structure to match the R data frame format.

def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string by providing glyph-level metrics.
    Returns a DataFrame with columns: glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint.
    """
    # Normalize inputs to lists
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
    
    # A very basic mapping for simulation of glyph indices since we can't 
    # guarantee a specific font file exists in the environment.
    # In reality, systemfonts uses the system's default font.
    char_to_index = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 'a': 61, 'l': 78, 'o': 83,
        'n': 80, 'g': 67, 'r': 82, 'u': 85, 'k': 71, 'e': 65, 'm': 77, 'p': 84,
        'v': 87, 'f': 66, 'd': 64, 'w': 89, 'c': 63, ';': 15, '\n': 10, '.': 11
    }

    for s_idx, (text, s_id, s_size) in enumerate(zip(strings, ids, sizes)):
        x_offset = 0
        # Split by line but R's shape_string processes the whole string
        # including newlines as glyphs or breaks.
        for char in text:
            glyph_idx = char_to_index.get(char, 0)
            
            # Mocking metrics based on character index
            # In R, x_midpoint is often half the advance width
            width = 6.0 * (s_size / 12.0) if char != ' ' else 3.0 * (s_size / 12.0)
            if char == '\n':
                width = 0
                x_offset = 0 # Reset x for new line
            
            all_glyphs.append({
                'glyph': char,
                'index': glyph_idx,
                'metric_id': 0,
                'string_id': s_id,
                'x_offset': x_offset,
                'y_offset': 0,
                'x_midpoint': width / 2 if char != '\n' else 0
            })
            x_offset += width

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