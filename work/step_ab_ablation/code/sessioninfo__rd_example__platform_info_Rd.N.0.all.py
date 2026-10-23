# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import os
import sys
import platform
import subprocess
import shutil
import locale
import time
from datetime import date
import pandas as pd

# r2py:entity:platform_info
def get_pandoc_info():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = out.splitlines()[0]
        ver = first_line.split()[-1]
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def get_quarto_info():
    path = shutil.which("quarto")
    if not path:
        return "NA"
    try:
        ver = subprocess.check_output(["quarto", "-V"], stderr=subprocess.STDOUT, text=True).splitlines()[0].strip()
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def platform_info():
    # R's platform_info() provides a data frame of platform-specific information
    # We map the R sessioninfo behavior to Python system calls
    
    # OS details
    os_val = platform.platform()
    # R often shows "Windows 11 x64 (build ...)" or "macOS ..."
    
    # Locale approximations
    # R's Sys.getlocale()
    loc = locale.getdefaultlocale()
    collate = loc[0] if loc and loc[0] else "C"
    ctype = loc[0] if loc and loc[0] else "C"
    
    # Timezone
    # R's Sys.timezone()
    try:
        import tzlocal
        tz = tzlocal.get_localzone_name()
    except ImportError:
        # Fallback to standard lib
        tz = time.tzname[0] if time.tzname else "UTC"
        if "CET" in tz or "CEST" in tz:
            tz = "Europe/Berlin"

    # Constructing the dictionary to mirror the R data frame
    info_dict = {
        "os": os_val,
        "locale": collate,
        "tz": tz,
        "pandoc": get_pandoc_info(),
        "quarto": get_quarto_info(),
    }
    
    # The actual R sessioninfo::platform_info() returns a dataframe with 
    # 'setting' and 'value' columns.
    data = []
    for k, v in info_dict.items():
        data.append({"setting": k, "value": v})
        
    return pd.DataFrame(data)

# R: suppressPackageStartupMessages(library(sessioninfo))
# Equivalent to importing the package
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()
# In R, calling platform_info() in the console prints the dataframe.
# We use to_string(index=False) to mimic the clean tabular output of R's print.
print(platform_info_result.to_string(index=False))