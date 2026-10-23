import pandas as pd
import numpy as np

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Approximate the behavior of systemfonts::shape_string.
    R's shape_string returns a data frame with glyph/line layout details.
    """
    # In R, if string is a vector, id and size are matched or recycled.
    if isinstance(string, str):
        strings = [string]
        ids = [1] if id is None else ([id] if not isinstance(id, (list, np.ndarray)) else id)
        sizes = [12] if size is None else ([size] if not isinstance(size, (list, np.ndarray)) else size)
    else:
        strings = list(string)
        ids = id if id is not None else [1] * len(strings)
        sizes = size if size is None else [12] * len(strings)
    
    # Ensure id and size match the length of strings (recycling)
    if len(ids) < len(strings):
        ids = (ids * (len(strings) // len(ids) + 1))[:len(strings)]
    if len(sizes) < len(strings):
        sizes = (sizes * (len(strings) // len(sizes) + 1))[:len(strings)]

    all_results = []
    
    # Simplified layout simulation to mimic the R data frame structure
    # R's shape_string output typically contains: x, y, width, height, advance, etc.
    for s, i, sz in zip(strings, ids, sizes):
        lines = s.split('\n')
        current_y = 0
        for line in lines:
            # Simplified: one entry per line to approximate the "shaping" result
            # Actual systemfonts returns glyph-level data, but for basic examples 
            # a row per line/segment is often how it's analyzed.
            line_width = len(line) * (sz * 0.5) # Mock width
            line_height = sz * 1.2 # Mock height
            
            all_results.append({
                'id': i,
                'x': 0,
                'y': current_y,
                'width': line_width,
                'height': line_height,
                'advance': line_width,
                'size': sz,
                'text': line
            })
            current_y -= line_height
            
    return pd.DataFrame(all_results)

# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
res1 = shape_string(string)
print(res1)

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]

# r2py:entity:shape_string_1
res2 = shape_string(string, id=[1, 1, 1], size=[12, 24, 12])
print(res2)