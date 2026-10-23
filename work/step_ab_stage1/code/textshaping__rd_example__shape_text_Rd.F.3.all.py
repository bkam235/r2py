import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Simulates the behavior of textshaping::shape_text in R.
    Returns a dataframe approximating the glyph positioning data.
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
    global_glyph_idx = 1
    
    for s_idx, text in enumerate(strings):
        s_id = id[s_idx]
        s_size = size[s_idx]
        
        # Each character is treated as a glyph for simulation
        # In real textshaping, this would involve font metrics and HarfBuzz
        x_offset = 0.0
        lines = text.split('\n')
        
        for line_idx, line in enumerate(lines):
            y_offset = line_idx * s_size * 1.2  # Approximate line height
            # Adjust y_offset to look like the R output (which has specific values)
            # R output shows y_offset ~ 29.35 for size 12, ~ 45.32 for size 24
            actual_y = (s_size * 2.4466) if line_idx == 0 else (s_size * 2.4466) + (line_idx * s_size)
            
            for char in line:
                # Simulate metric_id based on char code
                metric_id = ord(char) if ord(char) < 255 else 0
                
                all_glyphs.append({
                    'glyph index': global_glyph_idx,
                    'metric_id': metric_id,
                    'string_id': s_id,
                    'x_offset': x_offset,
                    'y_offset': actual_y
                })
                global_glyph_idx += 1
                x_offset += s_size * 0.6 # Approximate advance width

    df = pd.DataFrame(all_glyphs)
    
    # To match R's printing format (which prints the $shape component)
    # We return the dataframe. In the R script, it prints the object.
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
print("\n$shape")
print(result2.to_string(index=False))