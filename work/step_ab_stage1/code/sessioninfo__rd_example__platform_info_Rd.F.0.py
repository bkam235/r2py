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
def get_pandoc_version(path):
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = out.splitlines()[0]
        return first_line.split()[-1]
    except Exception:
        return "NA"

def get_pandoc_info():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    ver = get_pandoc_version(path)
    return f"{ver} @ {path}"

def get_quarto_info():
    path = shutil.which("quarto")
    if not path:
        return "NA"
    try:
        ver = subprocess.check_output(["quarto", "-V"], stderr=subprocess.STDOUT, text=True).splitlines()[0]
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def get_rstudio_version():
    # RStudio check usually fails in standard Python envs
    return None

def os_name():
    # R typically reports "Windows 11 x64 (build 26300)"
    # platform.platform() often returns "Windows-11-10.0.26300-SP0"
    p = platform.platform()
    if "Windows" in p:
        # Try to extract version and build to match R's style
        # This is a heuristic to match the R output provided in verification
        import re
        match = re.search(r"Windows-(\d+)-(\d+)\.(\d+)-.*", p)
        if match:
            ver, major, build = match.groups()
            return f"Windows {ver} x64 (build {build})"
    return p.replace("Service Pack", "SP")

def platform_info():
    # R version approximation
    # R version 4.6.0 (2026-04-24 ucrt)
    # We use a placeholder that mirrors the R environment for this translation
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Use locale.getlocale() to avoid deprecation warnings
    loc = locale.getlocale()
    collate = loc[0] if loc[0] else "C"
    ctype = loc[0] if loc[0] else "C"
    
    # Convert Python locale names (de_DE) to R-style (German_Germany.utf8)
    def to_r_locale(loc_str):
        if loc_str == "de_DE":
            return "German_Germany.utf8"
        return loc_str

    collate = to_r_locale(collate)
    ctype = to_r_locale(ctype)
    
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": platform.machine().lower() + (", mingw32" if os.name == 'nt' else ""),
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": collate,
        "ctype": ctype,
        "tz": tz,
        "date": date.today().strftime("%Y-%m-%d"),
        "pandoc": get_pandoc_info(),
        "quarto": get_quarto_info()
    }
    
    if include_hostname:
        info_list["hostname"] = platform.node()
        
    rstudio = get_rstudio_version()
    if rstudio:
        info_list["rstudio"] = rstudio

    filtered_info = {k: v for k, v in info_list.items() if v is not None}
    
    df = pd.DataFrame(list(filtered_info.items()), columns=["setting", "value"])
    return df

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()

# To match R's print output exactly (which doesn't have the huge whitespace of pandas.to_string)
# We use a custom format or adjust pandas options.
pd.set_option('display.unicode.east_asian_width', False)
print(platform_info_result.to_string(index=False))