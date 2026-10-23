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
            # R's match_fonts logic approximate
            weight = "bold" if bold else "normal"
            style = "italic" if italic else "normal"
            # findfont returns a path to a font file
            path = font_manager.findfont(family, weight=weight, style=style)
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # The GSUB (Glyph Substitution) table contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # The Feature List (FS) contains the feature tags
            if hasattr(gsub, 'FS') and gsub.FS:
                # FeatureList.featureList contains Feature objects with FeatureTag
                features = [f.FeatureTag for f in gsub.FS.featureList]
        
        # textshaping::get_font_features returns a list containing a vector of tags
        # Sorted alphabetically to match common R behavior for feature lists
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R's systemfonts::system_fonts() returns columns: name, variable, weight, width, path, etc.
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'name': f.name,
        'variable': getattr(f, 'variable', None),
        'weight': getattr(f, 'weight', None),
        'width': getattr(f, 'width', None),
        'path': f.fname,
        'family': f.name, # Keeping for the random_font selection logic
    } for f in all_fonts
])

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
if not sys_fonts.empty:
    random_idx = random.randint(0, len(sys_fonts) - 1)
    random_font = sys_fonts.iloc[random_idx]['family']
else:
    random_font = ""

# The R script ends with get_font_features(random_font) which prints the result
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)