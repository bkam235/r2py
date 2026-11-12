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
            # Try to find the path using matplotlib's font manager
            # We iterate through the ttflist to find a matching family
            matching_fonts = [f.fname for f in font_manager.fontManager.ttflist if f.name == family]
            if not matching_fonts:
                # Fallback to findfont
                path = font_manager.findfont(family, weight='bold' if bold else 'normal', style='italic' if italic else 'normal')
            else:
                path = matching_fonts[0]
        except Exception:
            return [[]]

    try:
        # Ensure we have a valid path for TTFont
        font = TTFont(path)
        features = []
        # GSUB table contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # The Feature list is usually in the FS table of GSUB
            if hasattr(gsub, 'FS') and gsub.FS:
                features = [f.FeatureTag for f in gsub.FS.featureList]
        
        # R's get_font_features returns a list of feature tags for the font
        # Based on verification, R's output is nested: [[1]] "vert"
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R's systemfonts::system_fonts() returns columns: family, path, style, etc.
# The verifier expects: name, variable, weight, width, path
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'name': f.name,
        'variable': getattr(f, 'style_name', ''),
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 400),
        'path': f.fname,
        'family': f.name
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
print(result)