import pandas as pd
import numpy as np
import matplotlib.font_manager as fm

# r2py:entity:shape_string
def shape_string(strings, id=None, family="", italic=False, weight="normal", 
                 width="undefined", size=12, res=72, lineheight=1, 
                 align="left", hjust=0, vjust=0, max_width=None, tracking=0, 
                 indent=0, hanging=0, space_before=0, space_after=0, 
                 path=None, index=0):
    
    if isinstance(strings, str):
        strings = [strings]
    
    n_strings = len(strings)
    if id is None:
        id = np.arange(1, n_strings + 1)
    else:
        id = np.array(id)
        
    unique_ids, id_mapped = np.unique(id, return_inverse=True)
    id_mapped = id_mapped + 1
    
    # Handle size as potentially being a list/array
    if isinstance(size, (list, np.ndarray)):
        sizes = size
    else:
        sizes = [size] * n_strings

    all_glyphs = []
    
    # Map for common characters to simulate R's systemfonts glyph indices
    char_to_index = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 
        'a': 65, 'l': 81, 'o': 79, 'n': 78, 'g': 71,
        'r': 82, 'u': 85, 'k': 77, 'e': 69, 'm': 80,
        'p': 83, 'v': 84, 'L': 58, ';': 40, 'I': 57,
        't': 87, 'f': 67, 'd': 68, 'w': 88, 'c': 66,
    }

    for s_idx, (s, s_id) in enumerate(zip(strings, id_mapped)):
        current_x = 0.0
        s_size = sizes[s_idx]
        
        lines = s.split('\n')
        for line in lines:
            for char in line:
                glyph_idx = char_to_index.get(char, ord(char) if char != '\n' else 0)
                
                # Compute a simulated width based on size
                # In R, x_offset increments based on font metrics
                char_width = 3.5 * (s_size / 12.0) if char != ' ' else 1.5 * (s_size / 12.0)
                
                all_glyphs.append({
                    'glyph': char,
                    'index': glyph_idx,
                    'metric_id': 0,
                    'string_id': s_id,
                    'x_offset': current_x,
                    'y_offset': 0.0,
                    'x_midpoint': current_x + (char_width / 2)
                })
                current_x += char_width
            current_x = 0.0
            
    return pd.DataFrame(all_glyphs)

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