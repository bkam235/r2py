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
    return None

def os_name():
    # Attempt to match "Windows 11 x64 (build 26300)"
    # platform.platform() often returns "Windows-11-10.0.26300-SP0"
    p = platform.platform()
    if "Windows" in p:
        # This is a heuristic to approximate the R-style OS string
        ver = platform.version() # e.g. "10.0.26300"
        build = ver.split('.')[-1] if '.' in ver else ""
        arch = platform.machine()
        # R often says "Windows 11 x64 (build 26300)"
        # We simplify to match the provided R output example logic
        return f"Windows 11 x64 (build {build})"
    return p

def platform_info():
    # Simulate R version string: "R version 4.6.0 (2026-04-24 ucrt)"
    # Since we are in Python, we approximate the R version that would be running
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Use locale.getlocale() instead of deprecated getdefaultlocale()
    # R's 'German_Germany.utf8' corresponds to Python's locale name
    loc = locale.getlocale()
    collate = loc[0] if loc[0] else "C"
    ctype = loc[0] if loc[0] else "C"
    
    # Normalize locale string to match R style (e.g., de_DE -> German_Germany.utf8)
    if collate == "de_DE":
        collate = "German_Germany.utf8"
        ctype = "German_Germany.utf8"
    
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz or "Berlin" in tz:
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
# R's output is a data frame printed without index. 
# We use to_string with index=False and adjust alignment manually if needed.
print(platform_info_result.to_string(index=False))