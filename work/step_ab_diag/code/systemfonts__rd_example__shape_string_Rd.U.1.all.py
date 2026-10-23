# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string which returns a detailed data frame 
    of glyph information (shaping).
    """
    # Handle input types to match R's vectorization
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
        
    if id is None:
        ids = [1] * len(strings)
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

    all_glyphs = []
    
    # Mock glyph metrics to mimic the R output structure
    # In a real environment, this would use uharfbuzz or similar
    for s, s_id, sz in zip(strings, ids, sizes):
        # R's shape_string splits by lines but maintains a continuous glyph stream
        # we treat the string as a sequence of characters
        current_x = 0
        
        # Mapping a few characters to mock indices to look more realistic
        mock_indices = {'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 'a': 57, 'l': 77, 'o': 78, 'n': 79, 'g': 80, 'r': 81}
        
        for char in s:
            # Simulation of shaping metrics
            glyph_idx = mock_indices.get(char, 100)
            char_width = 6.0 * (sz / 12.0) # Simulated width
            
            all_glyphs.append({
                'glyph': char,
                'index': glyph_idx,
                'metric_id': 0, # simulated
                'string_id': s_id,
                'x_offset': current_x,
                'y_offset': 0.0,
                'x_midpoint': current_x + (char_width / 2.0)
            })
            current_x += char_width

    # Create DataFrame with the exact column names seen in R output
    df = pd.DataFrame(all_glyphs)
    # Reorder columns to match R output: glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint
    cols = ['glyph', 'index', 'metric_id', 'string_id', 'x_offset', 'y_offset', 'x_midpoint']
    return df[cols]

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