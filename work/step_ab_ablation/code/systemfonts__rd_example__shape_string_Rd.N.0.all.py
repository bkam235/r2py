import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximates systemfonts::shape_string which returns glyph-level 
    positioning and dimensions.
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
    
    # Mocking character metrics: (width, height)
    # In reality, systemfonts uses FreeType/CoreText
    char_metrics = {
        ' ': (0.25, 0),
        '\n': (0, 0),
    }
    default_w = 0.6
    default_h = 0.7

    for s, i, sz in zip(strings, ids, sizes):
        current_x = 0.0
        current_y = 0.0
        scale = sz / 12.0
        
        for char in s:
            w = char_metrics.get(char, (default_w, default_h))[0] * scale
            h = char_metrics.get(char, (default_w, default_h))[1] * scale
            
            if char == '\n':
                # Reset x, move y down
                all_glyphs.append({
                    'id': i,
                    'char': char,
                    'x': current_x,
                    'y': current_y,
                    'width': 0,
                    'height': 0,
                    'advance': 0,
                    'size': sz
                })
                current_x = 0.0
                current_y -= sz * 1.2 # Line height
                continue

            # Simplified glyph placement
            all_glyphs.append({
                'id': i,
                'char': char,
                'x': current_x,
                'y': current_y,
                'width': w,
                'height': h,
                'advance': w,
                'size': sz
            })
            current_x += w

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