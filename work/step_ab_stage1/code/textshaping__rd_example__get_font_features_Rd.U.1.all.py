# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim managed by the harness (loads R's input data) - do not write it
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
            # Find font path using matplotlib font_manager
            # Note: findfont returns a font path string
            path = font_manager.findfont(family, weight=None, style=None)
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # Layout features are typically in the GSUB (Substitution) 
        # and GPOS (Positioning) tables. R's textshaping focuses on GSUB.
        if 'GSUB' in font:
            gsub = font['GSUB']
            # If the font has a Feature List (FSCA/FS)
            if hasattr(gsub, 'FS') and gsub.FS:
                features = [f.FeatureTag for f in gsub.FS.featureList]
            else:
                # Fallback: some fonts store features differently or we might need to scan
                # but FS is the standard for the feature list.
                pass
        
        # Ensure unique and sorted tags
        unique_features = sorted(list(set(features)))
        # R's get_font_features returns a list of character vectors
        return [unique_features]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R's systemfonts::system_fonts() returns columns: family, name, style, weight, width, etc.
# r2py:entity:sys_fonts
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'family': f.name,
        'name': f.name, # Simplified
        'variable': '', 
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 'normal'),
        'path': f.fname,
    } for f in all_fonts
])

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
if not hasattr(globals(), 'random_font'):
    random_idx = random.randint(0, len(sys_fonts) - 1)
    random_font = sys_fonts.iloc[random_idx]['family']

# The R script ends with get_font_features(random_font)
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)