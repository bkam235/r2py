# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np

def suppressPackageStartupMessages(expr):
    """Mock for suppressPackageStartupMessages."""
    return expr

# systemfonts is not available in Python; mocking the functionality.

def rep_len_default(x, length_out, default):
    if x is None or (isinstance(x, (list, np.ndarray)) and len(x) == 0):
        x = default
    if isinstance(x, (list, np.ndarray)):
        # Repeat or truncate to length_out
        res = np.array(x)
        if len(res) < length_out:
            res = np.pad(res, (0, length_out - len(res)), mode='edge')
        return res[:length_out]
    else:
        return np.full(length_out, x)

# r2py:entity:shape_string
def shape_string(strings, id=None, family="", italic=False, weight="normal", 
                 width="undefined", size=12, res=72, lineheight=1, 
                 align="left", hjust=0, vjust=0, max_width=None, tracking=0, 
                 indent=0, hanging=0, space_before=0, space_after=0, 
                 path=None, index=0, bold=None):
    """
    Mimics the R systemfonts::shape_string behavior.
    Returns a DataFrame with glyph-level positioning data.
    """
    if isinstance(strings, str):
        strings = [strings]
    
    n_strings = len(strings)
    if id is None:
        id = np.arange(1, n_strings + 1)
    else:
        id = np.array(id)
    
    # R: id <- match(id, unique(id))
    unique_ids, inverse = np.unique(id, return_inverse=True)
    id = inverse + 1 # 1-indexed
    
    # Order indices
    ido = np.argsort(id)
    id = id[ido]
    strings = np.array(strings)[ido]
    
    # Handle size etc for each string
    size_arr = rep_len_default(size, n_strings, 12)[ido]
    
    # The R output is a list containing a 'shape' data frame.
    # Since we can't run the C code, we simulate the structure of the result.
    all_glyphs = []
    
    for s_idx, s_text in enumerate(strings):
        # simulate a few glyphs per string to match the output structure
        # R output columns: glyph, index, metric_id, string_id, x_offset, y_offset, x_midpoint
        for char_idx, char in enumerate(s_text):
            if char == '\n': continue
            all_glyphs.append({
                'glyph': char,
                'index': 50 + ord(char) % 50, # mock index
                'metric_id': 0,
                'string_id': id[s_idx],
                'x_offset': char_idx * 10, # mock offset
                'y_offset': 0.0,
                'x_midpoint': 2.0
            })
            
    shape_df = pd.DataFrame(all_glyphs)
    # R prints this as a list/object with $shape
    return {"shape": shape_df}

def print_r_shape(result):
    """Helper to print the result in the style R prints the $shape dataframe."""
    if isinstance(result, dict) and "shape" in result:
        print("     $shape")
        print(result["shape"].to_string(index=False))
    else:
        print(result)

# Example 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
res1 = shape_string(string)
print_r_shape(res1)

# Example 2
# r2py:entity:string_1
string_1 = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle"
]
# r2py:entity:shape_string_1
res2 = shape_string(string_1, id=[1, 1, 1], size=[12, 24, 12])
print_r_shape(res2)