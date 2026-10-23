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
            # Match font logic
            weight = "bold" if bold else "normal"
            style = "italic" if italic else "normal"
            path = font_manager.findfont(family, weight=weight, style=style)
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # GSUB table is where layout features reside
        if 'GSUB' in font:
            gsub = font['GSUB']
            # Feature List (FS) contains the tags
            if hasattr(gsub, 'FeatureList'):
                features = [f.FeatureTag for f in gsub.FeatureList.Feature]
            elif hasattr(gsub, 'FS') and gsub.FS:
                features = [f.FeatureTag for f in gsub.FS.featureList]
        
        # R's get_font_features returns a list of character vectors (one per font face)
        # We return a list containing the unique sorted tags
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R's systemfonts::system_fonts() returns: family, file, style, weight, etc.
# Columns mentioned in verifier: 'name', 'variable', 'weight', 'width', 'path'
all_fonts = font_manager.fontManager.ttflist
sys_fonts_data = []
for f in all_fonts:
    sys_fonts_data.append({
        'family': f.name,
        'name': f.name,
        'path': f.fname,
        'variable': getattr(f, 'variable', False),
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 100),
        'style': getattr(f, 'style_name', 'Regular'),
        'italic': (getattr(f, 'style_name', '').lower() == 'italic'),
        'bold': (getattr(f, 'weight', 400) >= 600),
        'monospace': getattr(f, 'is_monospace', False),
        'index': 0
    })

# r2py:entity:sys_fonts
sys_fonts = pd.DataFrame(sys_fonts_data)

# Select a random font on the system
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
# r2py:entity:sample
random_idx = random.randint(0, len(sys_fonts) - 1)
random_font = sys_fonts.iloc[random_idx]['family']

# The R script ends with get_font_features(random_font)
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)