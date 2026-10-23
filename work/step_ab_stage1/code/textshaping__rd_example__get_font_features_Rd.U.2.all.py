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
            # R's textshaping uses systemfonts to match the family.
            # We approximate this by finding a font matching the family name.
            fonts = font_manager.findSystemFonts(fontnames=[family])
            if not fonts:
                # If direct family match fails, try any font that contains the family name
                all_fonts = font_manager.fontManager.ttflist
                fonts = [f.fname for f in all_fonts if family.lower() in f.name.lower()]
            
            if not fonts:
                return [[]]
            path = fonts[0]
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        if 'GSUB' in font:
            gsub = font['GSUB']
            # fontTools: GSUB.FeatureList.Feature contains the actual features
            if hasattr(gsub, 'FeatureList') and gsub.FeatureList:
                features = [f.FeatureTag for f in gsub.FeatureList.Feature]
        
        # R returns a list of character vectors. 
        # We return a list containing one sorted list of unique tags.
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# r2py:entity:sys_fonts
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'name': f.name,
        'family': f.name,
        'path': f.fname,
        'variable': False, # Not easily available in matplotlib.font_manager
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 'normal'),
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
if not sys_fonts.empty:
    random_idx = random.randint(0, len(sys_fonts) - 1)
    random_font = sys_fonts.iloc[random_idx]['family']
else:
    random_font = "Arial"

# The R script ends with get_font_features(random_font)
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)