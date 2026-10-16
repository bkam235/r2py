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
            # Find the font path using matplotlib font_manager
            # We look for the first font that matches the family name
            fonts = font_manager.fontManager.ttflist
            matching_fonts = [f for f in fonts if f.name == family]
            if not matching_fonts:
                # Fallback: try partial match
                matching_fonts = [f for f in fonts if family.lower() in f.name.lower()]
            
            if matching_fonts:
                path = matching_fonts[0].fname
            else:
                return [[]]
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        if 'GSUB' in font:
            gsub = font['GSUB']
            # Extract feature tags from the Feature List
            if hasattr(gsub, 'FS'):
                for feat in gsub.FS.featureList:
                    features.append(feat.FeatureTag)
        
        # R returns a list containing a unique, sorted vector of tags
        unique_features = sorted(list(set(features)))
        return [unique_features]
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
        'name': f.name,
        'variable': getattr(f, 'variable_font', False),
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 'normal'),
    } for f in all_fonts
])

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
random_idx = random.randint(0, len(sys_fonts) - 1)
random_font = sys_fonts.iloc[random_idx]['family']

# The R script ends with get_font_features(random_font)
# r2py:entity:get_font_features
result = get_font_features(family=random_font)

# To match R's printing output:
# [[1]]
# [1] "vert"
for i, feat_list in enumerate(result, 1):
    print(f"[[{i}]]")
    if feat_list:
        # R prints vectors as [1] "tag1" "tag2"
        tags_str = " ".join([f'"{t}"' for t in feat_list])
        print(f"[1] {tags_str}")
    else:
        print("[1] ")