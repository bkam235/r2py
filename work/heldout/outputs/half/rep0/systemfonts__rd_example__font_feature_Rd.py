# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import matplotlib.pyplot as plt
from matplotlib import rcParams

# In Python/Matplotlib, font features (OpenType) are handled via the 'font.features' 
# or through specific font properties. Since systemfonts' font_feature is used 
# for text rendering settings, we configure the matplotlib rcParams.

# r2py:entity:font_feature
# Translation of font_feature(letters = "stylistic", numbers = c("lining", "tabular"))
# r2py:entity:font_feature_1
# Translation of font_feature(numbers = c("lining", "tabular"), salt = 2)

# Note: Python does not have a 1:1 global system-wide function like font_feature 
# that affects all libraries. The equivalent for plotting/rendering is setting 
# the font properties. 

rcParams['font.family'] = 'serif'  # Or the specific font being targeted
# Matplotlib supports OpenType features via the 'font-feature-settings' CSS-like string 
# when using certain backends or specifically via font managers.
# Most Python libraries approximate this by selecting a font variant that is already 
# 'tabular' or 'lining' or using raw LaTeX/Cairo rendering.

# Approximate global configuration for font features:
plt.rcParams['text.usetex'] = False 
# To apply specific OpenType features in Python, one typically uses the 'font-feature-settings' 
# in CSS (for Shiny/HTML) or specific font files. 
# For a direct translation of "lining" and "tabular" numbers:
rcParams['font.variant'] = 'tabular-nums'