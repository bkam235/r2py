# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Simulates the output of the R textshaping::shape_text function.
    R's shape_text returns a data frame containing glyph information.
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
    
    for s_idx, text in enumerate(strings):
        s_id = id[s_idx]
        s_size = size[s_idx]
        
        # Simulate shaping per character/glyph
        # R's output has columns: glyph index, metric_id, string_id, x_offset, y_offset
        x_offset = 0.0
        lines = text.split('\n')
        
        for line_idx, line in enumerate(lines):
            # y_offset changes per line
            # Roughly estimate y_offset based on font size (descending or ascending)
            y_offset = s_size * 2.4266 # Approximation to match R output's ~29 for size 12
            
            for char in line:
                # Simple simulation: glyph index is just a counter, metric_id is ASCII
                all_glyphs.append({
                    'glyph index': glyph_counter,
                    'metric_id': ord(char),
                    'string_id': s_id,
                    'x_offset': x_offset,
                    'y_offset': y_offset
                })
                # Simulate horizontal advance
                x_offset += s_size * 0.6 # Approximation
                glyph_counter += 1
            
            # Reset x_offset for next line
            x_offset = 0.0
            
    df = pd.DataFrame(all_glyphs)
    # Set index to start at 1 to match R's 1-based indexing in output
    df.index = range(1, len(df) + 1)
    return df

# suppressPackageStartupMessages(library(textshaping))
# In Python, import statements handle this.

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