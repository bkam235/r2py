import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximate systemfonts::shape_string which returns glyph-level 
    positioning information for strings.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
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

    # This is a simulation of the shaping process to match the R output format
    # R's shape_string returns a data frame with columns: 
    # glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint
    
    all_glyphs = []
    
    current_string_id = 0
    for s, s_id, sz in zip(strings, ids, sizes):
        # Simple simulation of glyph metrics
        # In reality, this would use a font shaping engine (like HarfBuzz)
        x_cursor = 0
        # We treat the string as a sequence of characters (glyphs)
        # Note: R's shape_string handles \n by resetting x_offset and incrementing y_offset
        y_offset = 0
        
        for char in s:
            if char == '\n':
                x_cursor = 0
                y_offset += sz # Simple vertical advance
                continue
                
            # Simulate glyph properties
            # glyph: character, index: fake index, metric_id: 0, 
            # string_id: the provided id, x_offset: cumulative, y_offset: current line
            # x_midpoint: half of a simulated width
            
            glyph_width = 6 if char == ' ' else 4 # crude width
            x_midpoint = glyph_width / 2
            
            all_glyphs.append({
                'glyph': char,
                'index': ord(char) if char != ' ' else 3, # Dummy index
                'metric_id': 0,
                'string_id': s_id,
                'x_offset': x_cursor,
                'y_offset': float(y_offset),
                'x_midpoint': float(x_midpoint)
            })
            x_cursor += glyph_width
            
        current_string_id += 1

    # To match the R output structure exactly, we return a DataFrame
    # R returns a list with a $shape component. We'll return the DataFrame 
    # as that's the primary data.
    df = pd.DataFrame(all_glyphs)
    # To mimic the " $shape " print in R, we can wrap it or just return the df
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