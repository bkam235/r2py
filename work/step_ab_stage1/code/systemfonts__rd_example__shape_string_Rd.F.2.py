# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# Note: systemfonts::shape_string in R returns glyph-level shaping information.
# We simulate this behavior by creating a row for every character in the input strings.

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    # Mock glyph indices for characters (simulation of font metrics)
    glyph_map = {
        'T': 55, 'h': 75, 'i': 76, 's': 86, ' ': 3, 'a': 77, 'l': 80, 
        'o': 83, 'n': 85, 'g': 88, 'r': 87, 'u': 91, 'k': 81, 'I': 60,
        't': 87, 'p': 90, 'm': 84, 'e': 78, 'v': 92, 'd': 82, 'c': 73,
        '\n': None, ';': 50, '.': 45, 'f': 74, 'w': 93, 'x': 94, 'y': 95
    }
    
    # Default glyph index if char not in map
    DEFAULT_GLYPH = 100
    
    # Simulation of character widths
    char_widths = {
        'T': 7, 'h': 7, 'i': 3, 's': 6, ' ': 4, 'a': 6, 'l': 3, 
        'o': 6, 'n': 6, 'g': 6, 'r': 6, 'u': 6, 'k': 6, 'I': 3,
        't': 6, 'p': 6, 'm': 6, 'e': 6, 'v': 6, 'd': 6, 'c': 6,
        ';': 4, '.': 3, 'f': 6, 'w': 6, 'x': 6, 'y': 6
    }
    DEFAULT_WIDTH = 5

    results = []
    
    if isinstance(string, str):
        strings = [string]
        ids = [1] if id is None else ([id] if not isinstance(id, list) else id)
        sizes = [12] if size is None else ([size] if not isinstance(size, list) else size)
    else:
        strings = string
        ids = id if id is not None else list(range(1, len(strings) + 1))
        sizes = size if size is not None else [12] * len(strings)

    # Ensure lists are matched in length
    if len(ids) == 1: ids = ids * len(strings)
    if len(sizes) == 1: sizes = sizes * len(strings)

    for s_idx, s in enumerate(strings):
        s_id = ids[s_idx]
        sz = sizes[s_idx]
        
        x_offset = 0
        y_offset = 0
        
        for char in s:
            if char == '\n':
                x_offset = 0
                y_offset += 12 # simulate line height
                continue
                
            g_idx = glyph_map.get(char, DEFAULT_GLYPH)
            w = char_widths.get(char, DEFAULT_WIDTH) * (sz / 12)
            
            results.append({
                'glyph': char,
                'index': g_idx,
                'metric_id': 0, # Simplified simulation
                'string_id': s_id,
                'x_offset': x_offset,
                'y_offset': y_offset,
                'x_midpoint': x_offset + (w / 2)
            })
            x_offset += w
            
    return pd.DataFrame(results)

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