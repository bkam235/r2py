# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Since systemfonts and register_variant are R-specific font management tools 
# that interact with the R graphics engine, they have no direct Python equivalent 
# in standard libraries. We simulate the logic of finding and assigning 
# a system font family.

# r2py:entity:match_fonts
try:
    import matplotlib.font_manager as fm
    # match_fonts("sans") equivalent: find a font that matches 'sans-serif'
    sans_fonts = [f.name for f in fm.fontManager.ttflist if 'Sans' in f.name]
    sans = sans_fonts[0] if sans_fonts else "sans-serif"
except ImportError:
    sans = "sans-serif"

# register_variant is a low-level R graphics operation for OpenType features.
# In Python/Matplotlib/Plotnine, we define a font dictionary to approximate 
# custom font features (though ligatures are handled by the font file/renderer).
# r2py:entity:register_variant
variant_registry = {}
variant_registry["sans_ligature"] = {
    "family": sans,
    "features": {"ligatures": "discretionary"}
}

# r2py:entity:registry_fonts
# registry_fonts() equivalent
print(variant_registry)

# r2py:entity:clear_registry
# clear_registry() equivalent
variant_registry.clear()