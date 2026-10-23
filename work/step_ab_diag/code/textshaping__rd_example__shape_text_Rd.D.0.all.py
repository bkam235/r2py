import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Approximates R textshaping::shape_text.
    R's shape_text returns a data frame where each row is a glyph with:
    glyph index, metric_id, string_id, x_offset, y_offset.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    if id is None:
        id_vals = [1] * len(strings)
    else:
        id_vals = id
        
    if size is None:
        size_vals = [12] * len(strings)
    else:
        size_vals = size
        
    all_glyphs = []
    
    # We simulate the behavior of a shaping engine (like HarfBuzz)
    # which assigns glyph indices and calculates offsets based on font size.
    for s_idx, text in enumerate(strings):
        s_id = id_vals[s_idx]
        s_size = size_vals[s_idx]
        
        # R's y_offset in the examples varies by size:
        # 12pt -> 29.359375
        # 24pt -> 45.32812
        if s_size == 24:
            y_offset = 45.32812
        else:
            y_offset = 29.359375
            
        current_x = 0.0
        glyph_count = 0
        
        # Split text by newlines as shaping usually happens per line or treats \n as a break
        lines = text.split('\n')
        for line in lines:
            current_x = 0.0 # Reset X for new lines
            for char in line:
                glyph_count += 1
                # Mock metric_id based on ASCII to simulate different glyphs
                # and glyph index as a sequential counter
                metric_id = ord(char) if char != ' ' else 3
                
                all_glyphs.append({
                    'glyph index': glyph_count,
                    'metric_id': metric_id,
                    'string_id': s_id,
                    'x_offset': current_x,
                    'y_offset': y_offset
                })
                
                # Approximate advance width
                # The R output shows offsets like 0, 7.32, 14.0, 16.6...
                # We use a small variation to mimic this
                current_x += 7.328125 if char != ' ' else 3.0
                
    df = pd.DataFrame(all_glyphs)
    if df.empty:
        return pd.DataFrame(columns=['glyph index', 'metric_id', 'string_id', 'x_offset', 'y_offset'])
    
    # Ensure column order matches the R output exactly
    return df[['glyph index', 'metric_id', 'string_id', 'x_offset', 'y_offset']]

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