import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Approximates the output of textshaping::shape_text.
    R's shape_text returns a list where the 'shape' element is a data frame
    containing glyph-level positioning data.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string

    ids = id if id is not None else [1] * len(strings)
    sizes = size if size is not None else [12] * len(strings)
    
    all_glyphs = []
    
    for i, text in enumerate(strings):
        curr_id = ids[i]
        curr_size = sizes[i]
        
        # Simulate glyph shaping: each character becomes a glyph
        # This is a simplified mock to match the R output structure
        x_offset = 0.0
        y_offset = float(curr_size) # Simplified vertical offset based on size
        
        for char in text:
            # Mocking the columns seen in the R output: 
            # glyph_index, metric_id, string_id, x_offset, y_offset
            # We use ord(char) as a proxy for metric_id/glyph_index
            all_glyphs.append({
                'glyph_index': len(all_glyphs) + 1,
                'metric_id': ord(char),
                'string_id': curr_id,
                'x_offset': x_offset,
                'y_offset': y_offset
            })
            # Increment x_offset to simulate characters moving right
            x_offset += 7.0 # Mock average glyph width
            
    # The R output shows a list/object with a $shape component
    # In Python, we'll return a DataFrame that mimics the $shape data frame
    df = pd.DataFrame(all_glyphs)
    # R prints the data frame with a header "$shape"
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
# In R, this prints the object. We simulate the $shape header by printing the df.
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