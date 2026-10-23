import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Simulates the behavior of textshaping::shape_text in R.
    R's shape_text returns a data frame with glyph indices and offsets.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    # Default values if not provided
    if id is None:
        id = [1] * len(strings)
    if size is None:
        size = [12] * len(strings)
        
    all_glyphs = []
    glyph_counter = 1
    
    for s_idx, text in enumerate(strings):
        curr_id = id[s_idx]
        curr_size = size[s_idx]
        
        # Base offset multipliers to simulate different font sizes
        size_mult = curr_size / 12.0
        y_offset = 29.359375 * size_mult
        
        # Process each character as a glyph
        x_offset = 0.0
        for char in text:
            # Simulated metric_id based on character code
            metric_id = ord(char) if ord(char) != 10 else 0 # 10 is \n
            
            if char == '\n':
                # Newline resets x_offset and shifts y_offset
                x_offset = 0.0
                y_offset -= 29.359375 * size_mult
            else:
                # Simulate a glyph entry
                all_glyphs.append({
                    'glyph': glyph_counter,
                    'index': metric_id,
                    'metric_id': metric_id,
                    'string_id': curr_id,
                    'x_offset': x_offset,
                    'y_offset': y_offset
                })
                # Simulate character width (roughly 7 units)
                x_offset += 7.328125 * size_mult
                glyph_counter += 1
                
    # The R output uses a list-like structure ($shape), 
    # we return a DataFrame simulating the 'shape' element.
    df = pd.DataFrame(all_glyphs)
    # Rename to match R column names exactly as seen in output
    df.columns = ['glyph', 'index', 'metric_id', 'string_id', 'x_offset', 'y_offset']
    # R indices start at 1
    df.index = df.index + 1
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
# Simulate printing the result of shape_text(string)
res1 = shape_text(string)
print("$shape")
print(res1)

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]

# r2py:entity:shape_text_1
# Simulate printing the result of shape_text(string, id = c(1, 1, 1), size = c(12, 24, 12))
res2 = shape_text(string, id=[1, 1, 1], size=[12, 24, 12])
print("$shape")
print(res2)