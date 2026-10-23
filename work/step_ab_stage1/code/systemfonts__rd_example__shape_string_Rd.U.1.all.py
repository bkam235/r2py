import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximate systemfonts::shape_string by simulating glyph-level offsets.
    R output contains columns: glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint
    """
    # Normalize inputs
    if isinstance(string, str):
        strings = [string]
    else:
        strings = list(string)
    
    if id is None:
        ids = list(range(1, len(strings) + 1))
    elif isinstance(id, (int, float)):
        ids = [id] * len(strings)
    else:
        ids = list(id)
        
    if size is None:
        sizes = [12] * len(strings)
    elif isinstance(size, (int, float)):
        sizes = [size] * len(strings)
    else:
        sizes = list(size)

    all_glyphs = []
    
    # Simple mock glyph mapping (index is arbitrary)
    # In a real scenario, one would use a font library like freetype or matplotlib
    glyph_map = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 'a': 61, 'l': 77, 'o': 82, 
        'n': 83, 'g': 84, 'r': 85, '\n': -1, 'L': 56, 'k': 79, ';': 45, 'I': 57, 
        'p': 87, 'm': 88, 'e': 65, 'd': 68, 'v': 89, 'y': 90, 'u': 91, 't': 87
    }
    
    # we will use a simple constant width for simulation
    base_char_width = 6.0 

    for s_idx, (s, s_id, sz) in enumerate(zip(strings, ids, sizes)):
        current_x = 0
        current_y = 0
        metric_id = 0
        
        for char in s:
            if char == '\n':
                current_x = 0
                current_y += 12 # simulate line height
                continue
            
            # Assign a mock index from map or a random one
            idx = glyph_map.get(char, 100 + ord(char) % 100)
            
            # Width scaled by size (relative to 12pt)
            char_w = base_char_width * (sz / 12.0)
            
            all_glyphs.append({
                'glyph': char,
                'index': idx,
                'metric_id': metric_id,
                'string_id': s_id,
                'x_offset': current_x,
                'y_offset': current_y,
                'x_midpoint': current_x + (char_w / 2)
            })
            
            current_x += char_w
            metric_id += 1

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