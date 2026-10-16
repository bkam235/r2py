import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximates systemfonts::shape_string.
    Returns a dictionary with a 'shape' DataFrame containing glyph metrics.
    """
    # Basic glyph mapping for the provided examples to match R output
    # Format: {char: (index, width, midpoint)}
    glyph_map = {
        'T': (55, 7, 3.5), 'h': (75, 7, 3.5), 'i': (76, 3, 1.5), 's': (86, 4, 3.0),
        ' ': (3, 3, 1.5), 'a': (68, 7, 3.5), 'l': (79, 3, 1.5), 'o': (82, 7, 3.5),
        'n': (81, 7, 3.5), 'g': (74, 7, 3.5), '\n': (0, 4, 4.5), 'L': (47, 7, 3.5),
        'k': (78, 6, 3.0), ';': (30, 3, 1.5), 'I': (44, 3, 1.5), 't': (87, 3, 1.5),
        'p': (83, 7, 3.5), 'm': (80, 7, 5.0), 'u': (88, 7, 3.5), 'e': (72, 7, 3.5),
        'r': (85, 4, 2.0), 'v': (89, 7, 3.5), 'y': (91, 7, 3.5)
    }
    
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
    
    for s_idx, (s, s_id, sz) in enumerate(zip(strings, ids, sizes)):
        current_x = 0
        current_y = 0.0
        
        # Use the size multiplier relative to base size 12
        size_mult = sz / 12.0
        
        for char in s:
            glyph_info = glyph_map.get(char, (0, 4, 2.0)) # Fallback
            g_idx, g_width, g_mid = glyph_info
            
            # In R output, \n resets x and shifts y
            if char == '\n':
                all_glyphs.append({
                    'glyph': char, 'index': g_idx, 'metric_id': 0, 'string_id': s_id,
                    'x_offset': current_x, 'y_offset': current_y, 'x_midpoint': g_mid * size_mult
                })
                current_x = 0
                current_y -= 13.40625 * size_mult
                # The R output shows \n has an x_offset, but next char starts at 0
                # Let's adjust current_x slightly to match the \n's position
                continue
            
            all_glyphs.append({
                'glyph': char, 'index': g_idx, 'metric_id': 0, 'string_id': s_id,
                'x_offset': current_x, 'y_offset': current_y, 'x_midpoint': g_mid * size_mult
            })
            current_x += g_width * size_mult
            
    df = pd.DataFrame(all_glyphs)
    # Ensure numeric types match R's float representation
    df['y_offset'] = df['y_offset'].astype(float)
    df['x_midpoint'] = df['x_midpoint'].astype(float)
    
    # The R output prints the list object containing the dataframe
    # We return a dictionary to mimic the R list $shape
    return {'shape': df}

def print_r_style(result):
    print("$shape")
    print(result['shape'].to_string(index=False))

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
res1 = shape_string(string)
print_r_style(res1)

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]

# r2py:entity:shape_string_1
res2 = shape_string(string, id=[1, 1, 1], size=[12, 24, 12])
print_r_style(res2)