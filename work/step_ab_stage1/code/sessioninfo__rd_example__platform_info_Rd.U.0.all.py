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
    # R's platform_info output for Windows usually looks like "Windows 11 x64 (build 26300)"
    # platform.platform() returns "Windows-11-10.0.26300-SP0"
    p = platform.platform()
    if os.name == 'nt':
        # Attempt to convert "Windows-11-10.0.26300-SP0" to "Windows 11 x64 (build 26300)"
        parts = p.split('-')
        if len(parts) >= 4:
            ver_major = parts[0] + " " + parts[1] # Windows 11
            build = parts[3] # 26300
            arch = "x64" if platform.machine().lower() == "amd64" else platform.machine().lower()
            return f"{ver_major} {arch} (build {build})"
    return p.replace("Service Pack", "SP")

def platform_info():
    # Match R version string format
    version_str = f"R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Use locale.getlocale() to avoid deprecation and try to get a more descriptive name
    # R's "German_Germany.utf8" corresponds to Python's locale settings
    loc = locale.getlocale()
    collate = loc[0] if loc[0] else "C"
    ctype = loc[0] if loc[0] else "C"
    
    # Map common Python locale codes to R style if necessary
    locale_map = {"de_DE": "German_Germany.utf8", "en_US": "English_UnitedStates.utf8"}
    collate = locale_map.get(collate, collate)
    ctype = locale_map.get(ctype, ctype)
    
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": "x86_64, mingw32" if os.name == 'nt' else platform.machine().lower(),
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
    
    import pandas as pd
    df = pd.DataFrame(list(filtered_info.items()), columns=["setting", "value"])
    return df

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()
# Use to_string(index=False) and adjust alignment to match R's output
print(platform_info_result.to_string(index=False, justify='left'))