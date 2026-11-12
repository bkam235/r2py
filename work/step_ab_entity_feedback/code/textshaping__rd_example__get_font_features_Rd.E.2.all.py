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
            # Try to find the font file path using matplotlib's font manager
            # We search for the font family and pick the first match
            fonts = font_manager.findfonts(family)
            if not fonts:
                return [[]]
            path = fonts[0]
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # The GSUB table contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # R's textshaping usually extracts the feature tags (4-character strings)
            if hasattr(gsub, 'FeatureList'):
                for feature in gsub.FeatureList.featureList:
                    features.append(feature.FeatureTag)
            elif hasattr(gsub, 'FS'):
                for feature in gsub.FS.featureList:
                    features.append(feature.FeatureTag)
        
        # Return a list containing a sorted list of unique features to mimic R's list/vector output
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
        'variable': getattr(f, 'variable_font', False),
        'weight': f.weight,
        'width': getattr(f, 'width', None),
        'style': getattr(f, 'style_name', ''),
        'italic': (getattr(f, 'style_name', '') == 'Italic'),
        'bold': (f.weight >= 600),
        'monospace': getattr(f, 'is_monospace', False),
        'index': 0
    } for f in all_fonts
])

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
if len(sys_fonts) > 0:
    random_idx = random.randint(0, len(sys_fonts) - 1)
    random_font = sys_fonts.iloc[random_idx]['family']
else:
    random_font = ""

# The R script ends with get_font_features(random_font) which prints the result
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)