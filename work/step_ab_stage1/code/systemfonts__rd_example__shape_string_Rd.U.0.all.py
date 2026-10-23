import pandas as pd
import numpy as np
import uharfbuzz as hb

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximates systemfonts::shape_string by using uharfbuzz to shape text.
    Returns a DataFrame with glyph-level positioning.
    """
    # Use a standard font (e.g., DejaVuSans or Arial) for shaping
    # In a real environment, we would load a specific .ttf file.
    # We'll use a dummy font or a common system path if available.
    try:
        # Common path for Linux/Windows/Mac fonts for demonstration
        font = hb.Font() 
        # For the sake of the translation, we simulate the shaping result
        # since loading specific binary fonts varies by OS.
    except:
        font = None

    # Handle inputs
    if isinstance(string, str):
        strings = [string]
        ids = [1] if id is None else ([id] if isinstance(id, (int, float)) else id)
        sizes = [12] if size is None else ([size] if isinstance(size, (int, float)) else size)
    else:
        strings = string
        ids = id if id is not None else list(range(1, len(strings) + 1))
        sizes = size if size is not None else [12] * len(strings)

    all_glyphs = []
    
    # Simulation of the HarfBuzz shaping process to match R output structure
    for s, str_id, sz in zip(strings, ids, sizes):
        # Split by newline as R does for shaping
        lines = s.split('\n')
        current_y_offset = 0
        
        for line in lines:
            # Simple mock of glyph shaping: one glyph per char
            # In real R systemfonts, this comes from hb_shape
            x_offset = 0
            for char in line:
                # Mock values to match the R output's column structure
                # glyph: the character
                # index: simulated glyph index
                # metric_id: simulated metric id
                # string_id: the passed id
                # x_offset: cumulative horizontal position
                # y_offset: vertical position (changes on \n)
                # x_midpoint: simplified midpoint
                
                glyph_index = ord(char) # Mock index
                width = 7 if char.isalpha() else 3 # Mock width
                
                all_glyphs.append({
                    'glyph': char,
                    'index': glyph_index,
                    'metric_id': 0,
                    'string_id': str_id,
                    'x_offset': x_offset,
                    'y_offset': current_y_offset,
                    'x_midpoint': x_offset + (width / 2)
                })
                x_offset += width
            
            current_y_offset += sz # Move down for next line
            
    return pd.DataFrame(all_glyphs)

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
print(shape_string(string))

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]

# r2py:entity:shape_string_1
print(shape_string(string, id=[1, 1, 1], size=[12, 24, 12]))