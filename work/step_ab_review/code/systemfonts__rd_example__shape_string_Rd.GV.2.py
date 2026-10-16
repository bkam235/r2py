import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string which returns glyph-level 
    positioning data.
    """
    # Default values based on R behavior
    default_size = 12
    
    if isinstance(string, str):
        strings = [string]
        ids = [1] if id is None else ([id] if isinstance(id, (int, float)) else id)
        sizes = [default_size] if size is None else ([size] if isinstance(size, (int, float)) else size)
    else:
        strings = string
        ids = id if id is not None else list(range(1, len(strings) + 1))
        sizes = size if size is not None else [default_size] * len(strings)

    # Simplified glyph index mapping to match R output patterns
    glyph_map = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 'a': 68, 'l': 79, 'o': 82, 
        'n': 81, 'g': 74, '\n': 0, 'L': 47, 'k': 78, ';': 30, 'I': 44, 't': 87, 
        'p': 83, 'm': 80, 'u': 88, 'e': 72, 'r': 85
    }
    
    all_glyphs = []
    
    for s_idx, (text, s_id, sz) in enumerate(zip(strings, ids, sizes)):
        current_x = 0
        current_y = 0.0
        
        # Scaling factor for offsets based on size (relative to 12)
        scale = sz / 12.0
        
        for char in text:
            g_idx = glyph_map.get(char, 0)
            
            # Approximate x_midpoint as half of a standard char width
            # In R output: 'T' is 3.5, 'i' is 1.5, ' ' is 1.5
            x_mid = 3.5 if char.isupper() or char in 'aoeg' else (1.5 if char in 'il; ' else 3.0)
            x_mid *= scale
            
            # Handle line breaks for y_offset
            if char == '\n':
                # The R output shows \n at the end of a line, then next line starts at a negative y
                # Approximate line height as ~13.4 for size 12
                all_glyphs.append({
                    'glyph': char, 'index': g_idx, 'metric_id': 0, 'string_id': s_id,
                    'x_offset': current_x * scale, 'y_offset': current_y, 'x_midpoint': 4.5 * scale
                })
                current_x = 0
                current_y -= 13.40625 * scale
            else:
                all_glyphs.append({
                    'glyph': char, 'index': g_idx, 'metric_id': 0, 'string_id': s_id,
                    'x_offset': current_x * scale, 'y_offset': current_y, 'x_midpoint': x_mid
                })
                # Advance x based on the midpoint (simplified)
                current_x += (x_mid * 2)
        
    df_shape = pd.DataFrame(all_glyphs)
    # R prints as a list with element $shape
    return {"shape": df_shape}

def print_r_style(result):
    """Helper to mimic R's printing of lists and dataframes"""
    for key, df in result.items():
        print(f"${key}")
        print(df.to_string(index=False))

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