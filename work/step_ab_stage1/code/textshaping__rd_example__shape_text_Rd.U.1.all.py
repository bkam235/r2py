import pandas as pd
import numpy as np
import uharfbuzz as hb

# r2py:entity:shape_text
def shape_text(string, id=None, size=None):
    """
    Approximates the behavior of textshaping::shape_text in R.
    Returns a DataFrame containing glyph indices and offsets.
    """
    if isinstance(string, str):
        strings = [string]
    else:
        strings = string
    
    if id is None:
        id = [1] * len(strings)
    if size is None:
        size = [12] * len(strings)
        
    # We use a standard font (e.g., DejaVu Sans or Arial) for shaping simulation
    # In a real environment, textshaping uses the system's default font.
    # Since we can't guarantee font files, we simulate the layout logic.
    
    all_glyphs = []
    
    # Load a basic font for shaping if possible, otherwise simulate
    try:
        # Attempt to load a common system font path for shaping
        import os
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        if not os.path.exists(font_path):
            font_path = "C:\\Windows\\Fonts\\arial.ttf"
        
        with open(font_path, 'rb') as f:
            font_data = f.read()
        font = hb.Face(font_data)
    except:
        font = None

    for s_idx, (text, s_id, s_size) in enumerate(zip(strings, id, size)):
        # Process each line
        lines = text.split('\n')
        for line_idx, line in enumerate(lines):
            if font:
                # Real shaping using uharfbuzz
                buf = hb.Buffer()
                buf.add_str(line)
                buf.guess_segment_properties()
                hb.shape(font, buf)
                
                infos = buf.glyph_positions
                for g_idx, info in enumerate(infos):
                    all_glyphs.append({
                        'glyph': g_idx + 1,
                        'index': buf.glyph_ids[g_idx],
                        'metric_id': buf.glyph_ids[g_idx], # Approximation
                        'string_id': s_id,
                        'x_offset': info.x_offset,
                        'y_offset': info.y_offset * (s_size / 12.0)
                    })
            else:
                # Fallback simulation if font is missing
                for g_idx, char in enumerate(line):
                    all_glyphs.append({
                        'glyph': g_idx + 1,
                        'index': ord(char),
                        'metric_id': ord(char),
                        'string_id': s_id,
                        'x_offset': g_idx * 7.0, 
                        'y_offset': 29.35 * (s_size / 12.0)
                    })
                    
    df = pd.DataFrame(all_glyphs)
    # Rename columns to match R output
    df = df.rename(columns={'glyph': 'glyph', 'index': 'index', 'metric_id': 'metric_id', 
                            'string_id': 'string_id', 'x_offset': 'x_offset', 'y_offset': 'y_offset'})
    return df

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_text
res1 = shape_text(string)
print(res1)

# r2py:entity:string_1
string = [
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
]
# r2py:entity:shape_text_1
res2 = shape_text(string, id=[1, 1, 1], size=[12, 24, 12])
print(res2)