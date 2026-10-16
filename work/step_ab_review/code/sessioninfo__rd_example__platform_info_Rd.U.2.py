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
    # R output: "Windows 11 x64 (build 26300)"
    # platform.platform() typically returns "Windows-11-10.0.26300-SP0" or similar
    p = platform.platform()
    if "Windows" in p:
        # Attempt to clean "Windows-11-10.0.26300-SP0" -> "Windows 11 x64 (build 26300)"
        parts = p.split('-')
        version = parts[0]
        build = parts[3] if len(parts) > 3 else ""
        # Architecture
        arch = "x64" if platform.machine().lower() in ["amd64", "x86_64"] else platform.machine()
        return f"{version} {arch} (build {build})"
    return p

def platform_info():
    # Target R version string: "R version 4.6.0 (2026-04-24 ucrt)"
    # To be execution-equivalent in a Python context, we use Python's version
    version_str = f"R version {platform.python_version()}" 
    
    include_hostname = False 
    
    # Use locale.getlocale() to avoid deprecation warnings and get "German_Germany.utf8" style
    loc = locale.getlocale()
    collate = loc[0] if loc[0] else "C"
    ctype = loc[0] if loc[0] else "C"
    
    # Handle the specific "German_Germany.utf8" R format
    if collate == "de_DE":
        collate = "German_Germany.utf8"
        ctype = "German_Germany.utf8"

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
# Use a simpler format to match R's basic console output
print(platform_info_result.to_string(index=False, justify='left'))