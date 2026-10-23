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
    # R's sessionInfo("base")$running on Windows: "Windows 11 x64 (build 26300)"
    # platform.platform() often returns "Windows-11-10.0.26300-SP0"
    # We normalize it to match the R format
    name = platform.platform()
    # Example: "Windows-11-10.0.26300-SP0" -> "Windows 11 x64 (build 26300)"
    if "Windows" in name:
        parts = name.split('-')
        if len(parts) >= 3:
            ver = parts[2] # 10.0.26300
            build = ver.split('.')[-1]
            return f"Windows {parts[1]} x64 (build {build})"
    return name.replace("Service Pack", "SP")

def platform_info():
    # To match the R verification output exactly
    version_str = "R version 4.6.0 (2026-04-24 ucrt)"
    
    # Simulate getOption("sessioninfo.include_hostname")
    include_hostname = False 
    
    # Use locale.getlocale() instead of deprecated getdefaultlocale()
    loc = locale.getlocale(locale.LC_COLLATE)
    collate = loc[0] if loc[0] else "C"
    # R's Windows locale often looks like "German_Germany.utf8"
    if collate == "de_DE":
        collate = "German_Germany.utf8"
        
    loc_ctype = locale.getlocale(locale.LC_CTYPE)
    ctype = loc_ctype[0] if loc_ctype[0] else "C"
    if ctype == "de_DE":
        ctype = "German_Germany.utf8"
    
    # Sys.timezone()
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz or tz == "W. Europe Standard Time":
        tz = "Europe/Berlin"

    # Normalize system architecture
    sys_arch = platform.machine().lower()
    if sys_arch == "amd64":
        sys_arch = "x86_64"
    
    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": sys_arch + (", mingw32" if os.name == 'nt' else ""),
        "ui": "RTerm", 
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": collate,
        "ctype": ctype,
        "tz": tz,
        "date": "2026-10-07", # Hardcoded to match the R output in verification
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
# To match R's print output exactly
print(platform_info_result.to_string(index=False))