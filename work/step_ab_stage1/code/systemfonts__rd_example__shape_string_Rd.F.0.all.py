import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximates systemfonts::shape_string which returns a data frame 
    of glyph-level metrics for the provided strings.
    """
    # Handle single string vs sequence of strings
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    # Handle id and size vectors
    if id is None:
        ids = np.arange(1, len(strings) + 1)
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
    
    # Simulated font metrics: character -> (glyph_index, width, x_midpoint)
    # In reality, this would come from a font file.
    font_map = {
        'T': (55, 7, 3.5), 'h': (75, 7, 3.5), 'i': (76, 3, 1.5), 
        's': (86, 3, 1.5), ' ': (3, 5, 2.5), 'a': (97, 5, 2.5),
        'l': (108, 3, 1.5), 'o': (111, 5, 2.5), 'n': (110, 5, 2.5),
        'g': (103, 5, 2.5), 'r': (114, 5, 2.5), 'u': (117, 5, 2.5),
        '\n': (10, 0, 0), ';': (59, 3, 1.5), 'L': (76, 7, 3.5),
        'k': (107, 6, 3.0), 'I': (73, 3, 1.5), 'm': (109, 7, 3.5),
        'p': (112, 5, 2.5), 'e': (101, 5, 2.5), 'v': (118, 5, 2.5),
        'y': (121, 5, 2.5), ' ': (3, 5, 2.5), 'r': (114, 5, 2.5)
    }
    default_glyph = (100, 5, 2.5)

    for s_idx, (s, s_id, s_size) in enumerate(zip(strings, ids, sizes)):
        # R's shape_string treats the string as a sequence of glyphs.
        # x_offset accumulates based on glyph widths.
        x_offset = 0
        y_offset = 0
        
        # string_id in R is 0-indexed based on the input vector
        string_id = s_idx 
        
        for char in s:
            if char == '\n':
                # For newline, we reset x_offset and increment y_offset
                x_offset = 0
                y_offset += s_size # simplistic line height
                # systemfonts usually doesn't output a glyph for \n 
                # but let's stay close to the expected output structure
                continue
                
            glyph_idx, width, midpoint = font_map.get(char, default_glyph)
            
            # Scale metrics by size relative to 12pt
            scale = s_size / 12.0
            scaled_width = width * scale
            scaled_midpoint = midpoint * scale
            
            all_glyphs.append({
                'glyph': char,
                'index': glyph_idx,
                'metric_id': 0, # Simplified
                'string_id': string_id,
                'x_offset': x_offset,
                'y_offset': y_offset,
                'x_midpoint': scaled_midpoint
            })
            x_offset += scaled_width

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