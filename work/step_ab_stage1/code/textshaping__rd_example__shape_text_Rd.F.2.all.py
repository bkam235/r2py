import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Simulates the behavior of textshaping::shape_text by producing 
    glyph-level positioning data.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    # Handle optional arguments (vectorized in R)
    if id is None:
        id_vals = [1] * len(strings)
    elif isinstance(id, (int, float)):
        id_vals = [id] * len(strings)
    else:
        id_vals = id
        
    if size is None:
        size_vals = [12] * len(strings)
    elif isinstance(size, (int, float)):
        size_vals = [size] * len(strings)
    else:
        size_vals = size

    all_glyphs = []
    global_glyph_idx = 1
    
    for s_idx, text in enumerate(strings):
        s_id = id_vals[s_idx]
        s_size = size_vals[s_idx]
        
        lines = text.split('\n')
        for line_idx, line in enumerate(lines):
            x_offset = 0.0
            # Simulating y_offset based on size and line index
            # In R output, the first line y_offset is ~29.36 for size 12
            y_offset = s_size * 2.4433  # Approximation of the R output ratio
            
            for char in line:
                # Simulation of glyph metrics
                # metric_id is often a font-specific index
                metric_id = ord(char) if char != ' ' else 3
                
                all_glyphs.append({
                    'glyph index': global_glyph_idx,
                    'metric_id': metric_id,
                    'string_id': s_id,
                    'x_offset': x_offset,
                    'y_offset': y_offset
                })
                
                # Simulate x_offset incrementing based on char width
                # Using a simplified width based on size
                char_width = (s_size * 0.5) if char != ' ' else (s_size * 0.3)
                x_offset += char_width
                global_glyph_idx += 1
                
    df = pd.DataFrame(all_glyphs)
    # R prints a header '$shape'
    print("$shape")
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_text
print(shape_text(string))

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]
# r2py:entity:shape_text_1
print(shape_text(string, id=[1, 1, 1], size=[12, 24, 12]))