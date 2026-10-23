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
            # Use font_manager to find a font matching the family and style
            # We try to find a font that matches the family name
            matching_fonts = [f for f in font_manager.fontManager.ttflist if family.lower() in f.name.lower()]
            if not matching_fonts:
                return [[]]
            
            # Simple heuristic to pick the best match based on bold/italic
            best_font = matching_fonts[0]
            for f in matching_fonts:
                f_bold = getattr(f, 'weight', 400) >= 600
                f_italic = getattr(f, 'style_name', '').lower().find('italic') != -1
                if f_bold == bold and f_italic == italic:
                    best_font = f
                    break
            path = best_font.fname
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # GSUB table contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # The Feature List (FS) contains the mapping of tags to lookup indices
            if hasattr(gsub, 'FeatureList') and gsub.FeatureList:
                for feature in gsub.FeatureList.featureList:
                    features.append(feature.FeatureTag)
            elif hasattr(gsub, 'FS') and gsub.FS:
                for feature in gsub.FS.featureList:
                    features.append(feature.FeatureTag)
            else:
                # Fallback: look at the lookups themselves
                if hasattr(gsub, 'LookupList') and gsub.LookupList:
                    # In some versions, features are tied to lookups
                    # This is a simplification
                    pass
        
        # Return a list containing a sorted list of unique feature tags
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R's systemfonts::system_fonts() returns a data frame with columns: 
# family, name, variable, weight, width, path, etc.
# r2py:entity:sys_fonts
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'family': f.name,
        'name': f.name,
        'variable': False,
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 400),
        'path': f.fname,
        'style': getattr(f, 'style_name', ''),
        'italic': (getattr(f, 'style_name', '').lower().find('italic') != -1),
        'bold': (getattr(f, 'weight', 400) >= 600),
        'monospace': getattr(f, 'is_monospace', False),
        'index': 0
    } for f in all_fonts
])

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
random_idx = random.randint(0, len(sys_fonts) - 1)
random_font = sys_fonts.iloc[random_idx]['family']

# The R script ends with get_font_features(random_font) which prints the result
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)