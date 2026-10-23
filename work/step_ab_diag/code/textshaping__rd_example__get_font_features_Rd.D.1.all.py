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
            # Simulate match_fonts
            # Matplotlib's findfont doesn't take weight/style as direct args in the same way
            # we manually search for a match in the font manager
            target_path = None
            for font in font_manager.fontManager.ttflist:
                if font.name == family:
                    # Simple heuristic for bold/italic if needed
                    target_path = font.fname
                    break
            
            if target_path is None:
                target_path = font_manager.findfont(family)
            
            path = target_path
        except Exception:
            return [[]]

    try:
        font = TTFont(path)
        features = []
        # GSUB table contains the layout features
        if 'GSUB' in font:
            gsub = font['GSUB']
            # Use the feature list if available
            if hasattr(gsub, 'FS') and gsub.FS:
                features = [f.FeatureTag for f in gsub.FS.featureList]
            else:
                # Fallback: some fonts store features in different ways
                # but usually FS is the standard for feature list
                pass
        
        # R returns a list containing a character vector of unique feature tags
        return [sorted(list(set(features)))]
    except Exception:
        return [[]]

# --- Main Execution ---

# Approximate systemfonts::system_fonts()
# R's systemfonts::system_fonts() typically returns: family, file, weight, width, etc.
# r2py:entity:sys_fonts
all_fonts = font_manager.fontManager.ttflist
sys_fonts = pd.DataFrame([
    {
        'family': f.name,
        'path': f.fname,
        'name': f.name,
        'variable': getattr(f, 'is_variable', False),
        'weight': getattr(f, 'weight', 400),
        'width': getattr(f, 'width', 100),
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