# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import sys
import platform
import pandas as pd

# r2py:entity:external_info
# Simulating external_info() from sessioninfo
# This gathers system, platform, and python version information
external_info = {
    "platform": platform.platform(),
    "python_version": sys.version,
    "os": platform.system(),
    "os_release": platform.release(),
    "architecture": platform.machine()
}

# Convert to DataFrame to mimic R's structured output
d = pd.DataFrame([external_info])
print(d)