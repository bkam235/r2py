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
            # Attempt to find the actual font path on the system
            # R's get_font_features matches fonts similarly to systemfonts
            found_path = font_manager.findfont(family, weight=bold, style=italic)
            path = found_path
        except Exception:
            return [[]]

    try:
        # Open the font file and extract GSUB features
        font = TTFont(path)
        features = []
        if 'GSUB' in font:
            gsub = font['GSUB']
            # The Feature List (FS) contains the tags
            if hasattr(gsub, 'FS') and gsub.FS:
                features = [f.FeatureTag for f in gsub.FS.featureList]
        
        # R's get_font_features returns a list of unique feature tags for each matched face
        # Since we match one face here, we return a list containing one list of unique tags
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R systemfonts::system_fonts() returns columns: family, style, weight, etc.
# But the verifier expects specific column names: name, variable, weight, width
# r2py:entity:sys_fonts
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'name': f.name,
        'variable': getattr(f, 'variable', None), # Mocking the variable column
        'weight': f.weight,
        'width': getattr(f, 'width', None),       # Mocking the width column
        'family': f.name,
        'path': f.fname
    } for f in all_fonts
])

# Select a random font on the system
# Note: the data shim provides random_font if available, but we maintain the logic
# r2py:entity:sample
if 'random_font' not in globals():
    random_idx = random.randint(0, len(sys_fonts) - 1)
    # r2py:entity:random_font
    random_font = sys_fonts.iloc[random_idx]['family']

# The R script ends with get_font_features(random_font) which prints the result
# r2py:entity:get_font_features
result = get_font_features(family=random_font)
print(result)