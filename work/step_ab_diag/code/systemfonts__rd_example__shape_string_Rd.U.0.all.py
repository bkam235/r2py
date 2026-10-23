import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string which provides glyph-level layout information.
    Returns a DataFrame with columns: glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint.
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
    
    for s_idx, (s, s_id, sz) in enumerate(zip(strings, ids, sizes)):
        # Split by newline to handle layout
        lines = s.split('\n')
        current_x = 0
        current_y = 0
        
        for line in lines:
            for char in line:
                # Simulate glyph metrics
                # In real R systemfonts, these are precise font measurements
                glyph_width = 7.0 * (sz / 12.0) # Mock width
                glyph_mid = glyph_width / 2.0
                
                all_glyphs.append({
                    'glyph': char,
                    'index': np.random.randint(0, 1000), # Mock index
                    'metric_id': 0,
                    'string_id': s_id,
                    'x_offset': current_x,
                    'y_offset': current_y,
                    'x_midpoint': glyph_mid
                })
                current_x += glyph_width
            
            # Reset x and move y for next line
            current_x = 0
            current_y -= 12.0 * (sz / 12.0) # Mock line height
            
    df = pd.DataFrame(all_glyphs)
    # R's output shows $shape, so we ensure it looks like a data frame
    return df

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
# The R output starts with "$shape", we print the result of the function
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