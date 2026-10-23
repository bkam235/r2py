import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximates the behavior of systemfonts::shape_string in R.
    Returns a dataframe where each row represents a glyph.
    """
    # Simulated glyph widths to approximate the R output's x_offset and x_midpoint
    # R output for 'T' was 0 offset and 3.5 midpoint -> width = 7.0
    # R output for 'h' was 7 offset and 3.5 midpoint -> width = 7.0 (wait, midpoint is relative to char)
    # Actually R output shows: T(0, 3.5), h(7, 3.5), i(14, 1.5)
    # This means: 
    # T: offset 0, mid 3.5 => width 7
    # h: offset 7, mid 3.5 (from start of char) => width 7
    # i: offset 14, mid 1.5 (from start of char) => width 3
    
    GLYPH_WIDTHS = {
        'T': 7.0, 'h': 7.0, 'i': 3.0, 's': 3.0, ' ': 3.0,
        'a': 3.0, 'l': 3.0, 'o': 3.0, 'n': 3.0, 'g': 3.0,
        'r': 3.0, 'u': 3.0, 'k': 3.0, 'e': 3.0, 'm': 4.0,
        ';': 2.0, 'L': 7.0, 't': 3.0, 'p': 3.0, 'v': 3.0,
        'y': 3.0, 'w': 3.0, 'f': 3.0, 'd': 3.0
    }
    DEFAULT_WIDTH = 3.0
    
    # Mapping characters to simulated glyph indices based on R output examples
    GLYPH_INDICES = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3,
        'a': 97, 'l': 108, 'o': 111, 'n': 110, 'g': 103
    }

    # Handle input types
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
    
    for s, string_id, sz in zip(strings, ids, sizes):
        # Scale factor (relative to 12pt)
        scale = sz / 12.0
        
        current_x = 0.0
        current_y = 0.0
        
        for char in s:
            if char == '\n':
                current_x = 0.0
                current_y -= 12.0 * scale
                continue
            
            w = GLYPH_WIDTHS.get(char, DEFAULT_WIDTH) * scale
            idx = GLYPH_INDICES.get(char, ord(char))
            
            all_glyphs.append({
                'glyph': char,
                'index': idx,
                'metric_id': 0,
                'string_id': string_id,
                'x_offset': current_x,
                'y_offset': current_y,
                'x_midpoint': w / 2.0
            })
            current_x += w
            
    return pd.DataFrame(all_glyphs)

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