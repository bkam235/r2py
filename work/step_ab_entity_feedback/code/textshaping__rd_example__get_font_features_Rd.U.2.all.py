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
            # Match font using matplotlib's font manager
            # R's systemfonts behavior often picks the first available match
            found_font = font_manager.findfont(family, weight=bold, style=italic)
            path = found_font
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # GSUB (Glyph Substitution) table is where font features reside
        if 'GSUB' in font:
            gsub = font['GSUB']
            # In fontTools, the feature list is usually in the FeatureList attribute
            if hasattr(gsub, 'FeatureList') and gsub.FeatureList:
                for feature in gsub.FeatureList.Feature:
                    features.append(feature.FeatureTag)
            elif hasattr(gsub, 'FS') and gsub.FS:
                for feature in gsub.FS.featureList:
                    features.append(feature.FeatureTag)
        
        # Return as a list containing a sorted list of unique feature tags (mimicking R's list output)
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
        'variable': getattr(f, 'variable', None),
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
# Note: random_font is provided by the shim for verification, but we keep the logic
# r2py:entity:sample
if 'random_font' not in globals() or not isinstance(globals()['random_font'], str):
    random_idx = random.randint(0, len(sys_fonts) - 1)
    random_font = sys_fonts.iloc[random_idx]['family']
else:
    # Use the shimmed value
    random_font = globals()['random_font']

# The R script ends with get_font_features(random_font)
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)