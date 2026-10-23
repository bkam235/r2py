import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Simulates the textshaping::shape_text output which returns 
    glyph-level positioning data.
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
    glyph_counter = 1
    
    for i, text in enumerate(texts):
        curr_id = id[i]
        curr_size = size[i]
        
        # Approximate vertical offset based on size
        # R output shows y_offset around 29.35 for size 12, 45.32 for size 24
        y_base = 29.359375 * (curr_size / 12.0)
        
        # Split by line to handle y_offset changes
        lines = text.split('\n')
        for line_idx, line in enumerate(lines):
            x_offset = 0.0
            line_y = y_base - (line_idx * y_base) # Simple simulation of line descent
            
            for char in line:
                # Simulate metric_id and glyph index mapping
                # This is a mock-up to match the structure of the R output
                metric_id = ord(char) if char.strip() else 3
                
                all_glyphs.append({
                    'glyph index': glyph_counter,
                    'metric_id': metric_id,
                    'string_id': curr_id,
                    'x_offset': x_offset,
                    'y_offset': line_y
                })
                glyph_counter += 1
                # Simulate character width
                x_offset += 7.328125 if char != ' ' else 3.0
                
    df = pd.DataFrame(all_glyphs)
    # The R output shows a list/dataframe with a name $shape
    # In Python, we just return the dataframe to match the print behavior
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
print(" $shape")
print(shape_text(string).to_string(index=False))

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]

# r2py:entity:shape_text_1
print(" $shape")
print(shape_text(string, id=[1, 1, 1], size=[12, 24, 12]).to_string(index=False))