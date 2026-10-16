import pandas as pd
import numpy as np

# Note: systemfonts::shape_string in R uses HarfBuzz to return a list of glyphs, 
# their indices, and their precise offsets. 
# We implement a simulator that mimics this glyph-level breakdown.

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    # Mapping of common characters to mock glyph indices
    # In R, these indices come from the font file.
    glyph_map = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 'a': 84, 'l': 89, 
        'o': 91, 'n': 93, 'g': 94, 'r': 96, 'u': 98, 't': 87, 'e': 85, 
        '\n': 0, 'L': 56, 'k': 88, ';': 71, 'I': 57, 'm': 92, 'p': 95, 
        'v': 97, 'd': 83, 'w': 99, 'f': 82, 'y': 100
    }
    
    # Default glyph index for unknown characters
    DEFAULT_GLYPH_IDX = 0
    
    # Mock character widths (relative to size 12)
    char_widths = {
        'T': 7, 'h': 7, 'i': 3, 's': 6, ' ': 4, 'a': 6, 'l': 3, 
        'o': 6, 'n': 6, 'g': 6, 'r': 6, 'u': 6, 't': 6, 'e': 6, 
        '\n': 0, 'L': 7, 'k': 6, ';': 4, 'I': 3, 'm': 8, 'p': 6, 
        'v': 6, 'd': 6, 'w': 8, 'f': 6, 'y': 6
    }
    DEFAULT_WIDTH = 6

    results = []
    
    if isinstance(string, str):
        strings = [string]
        ids = [1] if id is None else ([id] if not isinstance(id, (list, np.ndarray)) else id)
        sizes = [12] if size is None else ([size] if not isinstance(size, (list, np.ndarray)) else size)
    else:
        strings = string
        ids = id if id is not None else list(range(1, len(strings) + 1))
        sizes = size if size is not None else [12] * len(strings)

    for s, str_id, sz in zip(strings, ids, sizes):
        x_offset = 0
        y_offset = 0
        scale = sz / 12.0
        
        for char in s:
            if char == '\n':
                # New line resets x_offset and shifts y_offset
                x_offset = 0
                y_offset += 12 * scale 
                continue
                
            glyph = char
            idx = glyph_map.get(char, DEFAULT_GLYPH_IDX)
            w = char_widths.get(char, DEFAULT_WIDTH) * scale
            
            # Midpoint is roughly half the width
            x_midpoint = w / 2
            
            results.append({
                'glyph': glyph,
                'index': idx,
                'metric_id': 0, # simplified
                'string_id': str_id,
                'x_offset': x_offset,
                'y_offset': y_offset,
                'x_midpoint': x_midpoint
            })
            x_offset += w
            
    df = pd.DataFrame(results)
    # R's print output for shape_string includes a '$shape' header implicitly 
    # as it returns a list/object. We return the DataFrame.
    return df

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
res1 = shape_string(string)
print("$shape")
print(res1.to_string(index=False))

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]

# r2py:entity:shape_string_1
res2 = shape_string(string, id=[1, 1, 1], size=[12, 24, 12])
print("$shape")
print(res2.to_string(index=False))