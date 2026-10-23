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
import os

# r2py:entity:get_font_features
def get_font_features(family="", italic=False, bold=False, path=None, index=0):
    """
    Python implementation of textshaping::get_font_features.
    """
    if path is None:
        try:
            # Attempt to find the font path via matplotlib's font manager
            # R's match_fonts logic handles weight and style
            weight = 700 if bold else 400
            style = "italic" if italic else "normal"
            
            # Find all fonts matching the family
            fonts = font_manager.fontManager.ttflist
            matching = [f for f in fonts if f.name == family]
            
            if not matching:
                # Fallback search
                matching = [f for f in fonts if family.lower() in f.name.lower()]
            
            if matching:
                # Try to pick the one that matches bold/italic best
                best_match = None
                for f in matching:
                    f_bold = (f.weight >= 600)
                    f_italic = ("italic" in f.style_name.lower())
                    if f_bold == bold and f_italic == italic:
                        best_match = f.fname
                        break
                if best_match:
                    path = best_match
                else:
                    path = matching[0].fname
            else:
                return [[]]
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # In OpenType fonts, GSUB table defines glyph substitution features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # The FeatureList (FS) contains the tags
            if hasattr(gsub, 'FeatureList') and gsub.FeatureList:
                features = [f.FeatureTag for f in gsub.FeatureList.Feature]
            elif hasattr(gsub, 'FS') and gsub.FS:
                # Some versions of fontTools use FS
                features = [f.FeatureTag for f in gsub.FS.featureList]
        
        # R returns a list of unique feature tags for the font
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
        'italic': ("italic" in getattr(f, 'style_name', '').lower()),
        'bold': (getattr(f, 'weight', 400) >= 600),
        'monospace': getattr(f, 'is_monospace', False),
        'index': 0
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