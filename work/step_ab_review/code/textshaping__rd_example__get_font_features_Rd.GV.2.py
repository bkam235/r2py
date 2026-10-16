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
            # Matplotlib's findfont returns a path to a font file
            weight = 700 if bold else 400
            style = "italic" if italic else "normal"
            # Note: findfont doesn't take weight/style as direct args like this, 
            # we use the family and let it resolve.
            path = font_manager.findfont(family)
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # GSUB table contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # In fontTools, the GSUB table often has a FeatureList (FS)
            if hasattr(gsub, 'FeatureList') and gsub.FeatureList:
                for feature in gsub.FeatureList.Feature:
                    features.append(feature.FeatureTag)
            elif hasattr(gsub, 'FS') and gsub.FS:
                for feature in gsub.FS.featureList:
                    features.append(feature.FeatureTag)
        
        # R's get_font_features returns a list of unique feature tags
        # Sorted to be deterministic
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
        'italic': (getattr(f, 'style_name', '') == 'Italic'),
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

# Custom printing to match R output: [[1]]\n[1] "vert"
if isinstance(result, list) and len(result) > 0:
    for i, item in enumerate(result, 1):
        print(f"[[{i}]]")
        if isinstance(item, list):
            # Mimic [1] "feat1" "feat2"
            vals = " ".join([f'"{v}"' for v in item])
            print(f"[1] {vals}")
else:
    print(result)