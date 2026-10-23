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
            # Find the font path using matplotlib's font manager
            # R's match_fonts handles weight and style
            weight = 700 if bold else 400
            style = 'italic' if italic else 'normal'
            
            # Get all matching fonts for the family
            fonts = [f for f in font_manager.fontManager.ttflist if f.name == family]
            if not fonts:
                # Fallback to findfont if exact name match fails
                path = font_manager.findfont(family, weight=weight, style=style)
            else:
                # Try to pick the one that matches style/weight
                path = fonts[0].fname
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # Layout features are stored in the GSUB (Glyph Substitution) table
        if 'GSUB' in font:
            gsub = font['GSUB']
            # Use the feature list (FS) to get the tags
            if hasattr(gsub, 'FS') and gsub.FS:
                features = [f.FeatureTag for f in gsub.FS.featureList]
            else:
                # Fallback: Some fonts store features in different ways within GSUB
                # but FS is the standard for the feature list.
                pass
        
        # R returns a list of unique tags (sorted) wrapped in a list (from lapply)
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
        'variable': False, # Simplified approximation
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 'normal'),
    } for f in all_fonts
])
# R's systemfonts::system_fonts() returns column 'family', not 'name' usually, 
# but the prompt says sys_fonts$family. Let's rename to align.
sys_fonts = sys_fonts.rename(columns={'family': 'family'})

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
if len(sys_fonts) > 0:
    random_idx = random.randint(0, len(sys_fonts) - 1)
    # We use the shim value if available, otherwise we compute
    if 'random_font' not in globals() or random_font == "":
        random_font = sys_fonts.iloc[random_idx]['family']
else:
    random_font = ""

# The R script ends with get_font_features(random_font)
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)