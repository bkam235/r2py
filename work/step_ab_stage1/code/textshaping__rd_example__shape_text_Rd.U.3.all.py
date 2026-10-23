import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Simulates the behavior of textshaping::shape_text in R.
    Returns a data frame with glyph indices and offsets.
    """
    if isinstance(string, str):
        texts = [string]
    else:
        texts = string
    
    if id is None:
        id = [1] * len(texts)
    if size is None:
        size = [12] * len(texts)
        
    all_glyphs = []
    global_glyph_idx = 1
    
    for i, text in enumerate(texts):
        # Split by newline to handle multi-line strings
        lines = text.split('\n')
        current_size = size[i]
        current_id = id[i]
        
        # In R's textshaping, glyphs are mapped. We simulate this mapping.
        # We generate a row for every character in the text.
        y_offset = current_size * 2.4 # Rough approximation of baseline
        x_offset = 0.0
        
        for line in lines:
            for char in line:
                # Simulate metric_id based on char code
                metric_id = ord(char)
                
                all_glyphs.append({
                    'glyph index': global_glyph_idx,
                    'metric_id': metric_id,
                    'string_id': current_id,
                    'x_offset': x_offset,
                    'y_offset': y_offset
                })
                # Increment x_offset based on size to simulate shaping
                x_offset += (current_size * 0.6)
                global_glyph_idx += 1
            # Reset x_offset for new line, though R's shape_text 
            # handles layout differently, we simulate the column structure.
            x_offset = 0.0 

    df = pd.DataFrame(all_glyphs)
    # Match R output format (printing the $shape list element usually looks like a df)
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
result1 = shape_text(string)
print("$shape")
print(result1.to_string(index=False))

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]

# r2py:entity:shape_text_1
result2 = shape_text(string, id=[1, 1, 1], size=[12, 24, 12])
print("$shape")
print(result2.to_string(index=False))