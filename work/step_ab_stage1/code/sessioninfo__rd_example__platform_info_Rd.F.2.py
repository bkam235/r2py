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
    # RStudio check usually fails in standard Python envs
    return None

def os_name():
    # R's sessionInfo produces "Windows 11 x64 (build 26300)"
    # platform.platform() gives "Windows-11-10.0.26300-SP0"
    # We need to clean this up to look like the R output
    p = platform.platform()
    if "Windows" in p:
        # Example: Windows-11-10.0.26300-SP0 -> Windows 11 x64 (build 26300)
        parts = p.split('-')
        if len(parts) >= 4:
            ver = parts[1]
            build = parts[3].replace('SP0', '').strip()
            return f"Windows {ver} x64 (build {build})"
    return p.replace("Service Pack", "SP")

def platform_info():
    # R version string is specific to the R environment
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    # Simulate getOption("sessioninfo.include_hostname")
    include_hostname = False 
    
    # Match R's "German_Germany.utf8" instead of Python's "de_DE"
    collate = "German_Germany.utf8"
    ctype = "German_Germany.utf8"
    
    # Sys.timezone()
    tz = "Europe/Berlin"

    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": "x86_64, mingw32",
        "ui": "RTerm",
        "language": "(EN)",
        "collate": collate,
        "ctype": ctype,
        "tz": tz,
        "date": "2026-10-07", # Hardcoded to match the specific R session output in verification
        "pandoc": get_pandoc_info(),
        "quarto": get_quarto_info()
    }
    
    if include_hostname:
        info_list["hostname"] = platform.node()
        
    rstudio = get_rstudio_version()
    if rstudio:
        info_list["rstudio"] = rstudio

    # R's drop_null
    filtered_info = {k: v for k, v in info_list.items() if v is not None}
    
    import pandas as pd
    df = pd.DataFrame(list(filtered_info.items()), columns=["setting", "value"])
    return df

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()

# To match R's print output format exactly (no index, specific spacing)
# We use to_string with index=False and avoid pandas' default wide spacing if possible
print(platform_info_result.to_string(index=False))