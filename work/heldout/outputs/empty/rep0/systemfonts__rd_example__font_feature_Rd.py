# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import systemfonts

# In Python, font features are typically handled by the rendering engine 
# (like matplotlib or plotnine) rather than a global system-wide 
# function call like in R's systemfonts. 
# However, to replicate the intent of defining these feature tags:

# Note: Python doesn't have a global 'font_feature' state machine 
# that affects all subsequent plots globally without passing a 
# configuration dictionary to the plotting library.

# Define the feature configurations as dictionaries to be passed to plotnine/matplotlib
# r2py:entity:font_feature
font_feature_1 = {"stylistic": "letters", "numbers": ["lining", "tabular"]}
# r2py:entity:font_feature_1
font_feature_2 = {"numbers": ["lining", "tabular"], "salt": 2}