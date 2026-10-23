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
    # Try to mimic "Windows 11 x64 (build 26300)"
    # platform.platform() often returns "Windows-11-10.0.26300-SP0"
    p = platform.platform()
    if "Windows" in p:
        # Simple heuristic to clean up the string to look more like R's sessioninfo output
        # In a real scenario, we'd use reg queries, but here we approximate.
        parts = p.split('-')
        if len(parts) >= 4:
            ver = parts[2] # 10.0
            build = parts[3].replace('SP0', '')
            arch = "x64" if platform.machine().lower() == "amd64" else platform.machine()
            return f"Windows 11 {arch} (build {build})"
    return p

def platform_info():
    # R version string approximation
    version_str = f"R version {platform.python_version()}" 
    
    include_hostname = False 
    
    # Use locale.getlocale() instead of getdefaultlocale() to avoid warnings
    loc = locale.getlocale()
    collate = loc[0] if loc[0] else "C"
    ctype = loc[0] if loc[0] else "C"
    
    # R's German_Germany.utf8 often maps to de_DE.UTF-8 in Python
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

# To match R's data frame printing (fixed width, no index)
# R output: 
#      setting  value
# version  R version ...
# os       Windows ...
print(f"{'setting':>11} {'value'}")
for idx, row in platform_info_result.iterrows():
    print(f"{row['setting']:<8} {row['value']}")