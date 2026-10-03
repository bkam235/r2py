# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import matplotlib.font_manager as fm
from matplotlib import rcParams

# In Python/Matplotlib, font features (like lining/tabular figures) 
# are handled via the 'font-features' property in the rcParams 
# or passed directly to the font rendering engine (freetype/harfbuzz).

# Note: systemfonts.font_feature in R is used for OpenType feature selection.
# In Python, these are typically passed as a string of CSS-like features 
# to the rendering backend or specified via font properties.

# Equivalent to font_feature(letters = "stylistic", numbers = c("lining", "tabular"))
# and font_feature(numbers = c("lining", "tabular"), salt = 2)
# r2py:entity:font_feature_1
rcParams['font.features'] = 'stylistic, lining, tabular, salt=2'