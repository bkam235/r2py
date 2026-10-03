# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import matplotlib.pyplot as plt
from matplotlib import rcParams

# In Python/Matplotlib, font features (OpenType features) are handled via 
# the 'font.properties' or passed to the backend. 
# Since systemfonts/font_feature in R is used for low-level typography 
# (lining/tabular numbers), the equivalent in Python is configuring 
# the rcParams or using specific font properties.

# Setting global font properties to emulate the R configuration
# 'lining' and 'tabular' numbers are typically controlled by the font family
# and the 'font-variant-numeric' CSS-like properties.

rcParams['font.family'] = 'sans-serif' 
# To specifically enable tabular figures (fixed width numbers) in Matplotlib:
rcParams['mathtext.fontset'] = 'stix' # Example of a font set with better numeric control

# Note: Python's standard libraries (pandas, numpy, plotnine) do not have 
# a direct 1:1 function for the 'font_feature' utility from the R 'systemfonts' 
# package as that is a wrapper for FreeType/HarfBuzz. 
# The closest approximation is setting the font properties for the rendering engine.

# Mimicking the R logic of defining stylistic features for the session:
# salt = 2 refers to Stylistic Set 2.
# r2py:entity:font_feature_1
font_config = {
    "letters": "stylistic",
    "numbers": ["lining", "tabular"],
    "salt": 2
}