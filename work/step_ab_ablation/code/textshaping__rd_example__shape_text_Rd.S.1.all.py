# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Mock implementation of textshaping::shape_text.
    In R, shape_text returns a data frame containing glyph information 
    (x, y, glyph, advance_x, advance_y, etc.)
    """
    if isinstance(string, str):
        texts = [string]
    else:
        texts = list(string)
    
    ids = id if id is not None else [1] * len(texts)
    sizes = size if size is not None else [12] * len(texts)
    
    all_glyphs = []
    
    for text, tid, tsize in zip(texts, ids, sizes):
        # Simulate glyph shaping for each character
        # In reality, textshaping calculates precise offsets based on font metrics
        x_offset = 0.0
        for char in text:
            if char == '\n':
                # Newline resets x and moves y (simulated)
                x_offset = 0.0
                continue
            
            # Mock glyph data
            all_glyphs.append({
                'id': tid,
                'x': x_offset,
                'y': 0.0,
                'glyph': ord(char),
                'advance_x': tsize * 0.6, # Approximation of width
                'advance_y': 0.0
            })
            x_offset += tsize * 0.6
            
    return pd.DataFrame(all_glyphs)

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_text
# In R, this is called and the result is printed
result1 = shape_text(string)
print(result1)

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]

# r2py:entity:shape_text_1
# In R, shape_text(string, id = c(1, 1, 1), size = c(12, 24, 12))
result2 = shape_text(string, id=[1, 1, 1], size=[12, 24, 12])
print(result2)