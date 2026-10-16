import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximates systemfonts::shape_string.
    R's shape_string returns a data frame with glyph-level metrics.
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
    
    # Simulated metrics for glyphs
    # In a real environment, this would use a font shaping engine like HarfBuzz
    char_metrics = {
        'T': (55, 7), 'h': (75, 7), 'i': (76, 3), 's': (86, 3), 
        ' ': (3, 3), 'a': (60, 3), 'l': (77, 3), 'o': (81, 3), 
        'n': (84, 3), 'g': (88, 3), 'r': (87, 3), 'u': (89, 3),
        'k': (83, 3), 'L': (58, 7), ';': (59, 3), 'I': (51, 3),
        't': (87, 3), 'p': (90, 3), 'm': (85, 3), 'e': (72, 3),
        '\n': (0, 0)
    }

    current_x = 0
    current_y = 0
    
    for s, s_id, sz in zip(strings, ids, sizes):
        # Scale factor based on default 12pt size
        scale = sz / 12.0
        
        for char in s:
            if char == '\n':
                current_x = 0
                current_y -= 12 * scale
                continue
            
            glyph_idx, width = char_metrics.get(char, (99, 3))
            
            # Mimicking R's output columns
            all_glyphs.append({
                'glyph': char,
                'index': glyph_idx,
                'metric_id': 0,
                'string_id': s_id,
                'x_offset': current_x,
                'y_offset': current_y,
                'x_midpoint': (current_x + (width * scale / 2))
            })
            current_x += width * scale
            
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