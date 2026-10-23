import pandas as pd
import numpy as np
import uharfbuzz as hb

# r2py:entity:shape_string
def shape_string(string, id=None, size=None):
    """
    Simulates systemfonts::shape_string by using uharfbuzz to shape text.
    R's systemfonts returns a data frame of glyph positions.
    """
    # Default font: In R, systemfonts uses the default system font.
    # We use a common system font path or load a basic one for shaping.
    # For the sake of this translation, we use a generic font load.
    try:
        # Try to load a common font for shaping
        font = hb.open_font() 
    except:
        # Fallback to a dummy font if no system font is available
        font = hb.open_font("Arial.ttf")

    # Normalize inputs to lists
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
    
    for s, s_id, sz in zip(strings, ids, sizes):
        # Create a buffer for the string
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        
        # Shape the text
        # Note: systemfonts uses HarfBuzz internally
        infos = font.shape(buf)
        
        # Calculate scaling based on size (R's shape_string returns units)
        # The offsets are typically in font units or pixels
        scale = sz / 12.0
        
        for i, info in enumerate(infos):
            all_glyphs.append({
                'glyph': info.glyph_name if hasattr(info, 'glyph_name') else str(info.codepoint),
                'index': info.codepoint,
                'metric_id': 0, # Simplified
                'string_id': s_id,
                'x_offset': info.x_offset * scale,
                'y_offset': info.y_offset * scale,
                'x_midpoint': (info.x_advance * scale) / 2
            })

    # R's shape_string returns a data frame. We mimic the column names seen in the output.
    df = pd.DataFrame(all_glyphs)
    # Rename to match R's output headers exactly
    df.columns = ['glyph', 'index', 'metric_id', 'string_id', 'x_offset', 'y_offset', 'x_midpoint']
    return df

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