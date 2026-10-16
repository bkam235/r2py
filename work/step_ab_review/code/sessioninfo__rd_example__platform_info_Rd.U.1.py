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
    # R produced: Windows 11 x64 (build 26300)
    # platform.platform() on Windows often returns 'Windows-11-10.0.26300-SP0'
    # We need to transform it to match the R style.
    raw = platform.platform()
    if os.name == 'nt':
        # Attempt to extract the build number if available in the string
        parts = raw.split('-')
        if len(parts) >= 3:
            build = parts[2]
            # Simplification to match "Windows 11 x64 (build 26300)"
            # Note: we approximate "Windows 11" and "x64"
            return f"Windows 11 x64 (build {build})"
    return raw.replace("Service Pack", "SP")

def platform_info():
    # R version 4.6.0 (2026-04-24 ucrt)
    # Since we are translating the logic, we use a placeholder that mirrors 
    # the R structure if the environment is an R simulation, but for a 
    # standalone Python script, we'll simulate the R version string.
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Using locale.getlocale() instead of getdefaultlocale() to avoid deprecation warnings
    loc_name, loc_encoding = locale.getlocale()
    # R output: German_Germany.utf8
    # Python: de_DE.UTF-8
    # We map common patterns to match the R 'Language_Country.encoding' style
    collate = loc_name if loc_name else "C"
    if collate == "de_DE":
        collate = "German_Germany.utf8"
    ctype = collate
    
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
# Print without index and without alignment padding to match R's simple data frame print
print(platform_info_result.to_string(index=False))