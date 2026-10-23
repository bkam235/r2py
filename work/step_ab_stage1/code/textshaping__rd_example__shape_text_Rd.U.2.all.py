import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Approximates the behavior of textshaping::shape_text in R.
    R's shape_text returns a data frame of glyph positioning information.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    if id is None:
        id = [1] * len(strings)
    if size is None:
        size = [12] * len(strings)
        
    all_glyphs = []
    glyph_counter = 1
    
    for i, text in enumerate(strings):
        # Simulate glyph shaping: treat each character as a glyph
        # In real textshaping, this would involve HarfBuzz
        curr_id = id[i]
        curr_size = size[i]
        
        x_offset = 0.0
        y_offset = float(curr_size * 2.44) # Mock vertical offset based on size
        
        for char in text:
            # Mock metric_id based on ASCII
            metric_id = ord(char) if char != '\n' else 0
            
            if char == '\n':
                x_offset = 0.0
                # Shift y_offset for new lines (mocking line spacing)
                y_offset -= curr_size * 1.2 
            else:
                # Mock x_offset increment
                all_glyphs.append({
                    'glyph index': glyph_counter,
                    'metric_id': metric_id,
                    'string_id': curr_id,
                    'x_offset': x_offset,
                    'y_offset': y_offset
                })
                glyph_counter += 1
                x_offset += 6.5 # Mock average character width
                
    # The R output prints as a data frame with a '$shape' header
    df = pd.DataFrame(all_glyphs)
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
print("$shape")
print(shape_text(string).to_string(index=False))

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]

# r2py:entity:shape_text_1
print("$shape")
print(shape_text(string, id=[1, 1, 1], size=[12, 24, 12]).to_string(index=False))