# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/textshaping__rd_example__get_font_features_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'textshaping__rd_example__get_font_features_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['random_font']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import random
import pandas as pd
from fontTools.ttLib import TTFont
from matplotlib import font_manager

# r2py:entity:get_font_features
def get_font_features(family="", italic=False, bold=False, path=None, index=0):
    """
    Python implementation of textshaping::get_font_features.
    """
    if path is None:
        try:
            # Use find_system_fonts to get a list of paths for the family
            # This mimics systemfonts' behavior more closely than findfont
            paths = font_manager.findSystemFonts(family)
            if not paths:
                # Fallback to findfont if the family search didn't work
                path = font_manager.findfont(family, weight=400 if not bold else 700, style='italic' if italic else 'normal')
            else:
                path = paths[0]
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # In OpenType fonts, GSUB (Glyph Substitution) contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # The Feature List (FS) contains the tags
            if hasattr(gsub, 'FS') and gsub.FS:
                # Extract feature tags (e.g., 'kern', 'liga', 'vert')
                features = [f.FeatureTag for f in gsub.FS.featureList]
        
        # R's get_font_features returns a list containing a character vector of unique tags
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# r2py:entity:sys_fonts
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'family': f.name,
        'path': f.fname,
        'style': getattr(f, 'style_name', ''),
        'italic': (getattr(f, 'style_name', '') == 'Italic'),
        'bold': (getattr(f, 'weight', 400) >= 600),
        'monospace': getattr(f, 'is_monospace', False),
        'index': 0
    } for f in all_fonts
])

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
if not hasattr(sys_fonts, 'empty') or not sys_fonts.empty:
    random_idx = random.randint(0, len(sys_fonts) - 1)
    random_font_val = sys_fonts.iloc[random_idx]['family']
else:
    random_font_val = "Arial"

# The data shim provides random_font, but the script logic calculates it.
# To be execution-equivalent to the R script flow:
random_font = random_font_val

# The R script ends with get_font_features(random_font) which prints the result
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)