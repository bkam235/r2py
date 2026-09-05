# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import shutil
import os

# r2py:entity:tryCatch
try:
    # shutil.get_terminal_size() is the Python equivalent to ps_tty_size()
    width, height = shutil.get_terminal_size()
    result = {'width': width, 'height': height}
except Exception:
    # Fallback to a default width (similar to getOption("width")) and None for height
    result = {'width': 80, 'height': None}

print(result)