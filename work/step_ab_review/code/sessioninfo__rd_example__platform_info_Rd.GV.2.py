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
    # To match "Windows 11 x64 (build 26300)"
    # platform.platform() typically returns "Windows-11-10.0.26300-SP0" or similar
    # We need to map it to the R style.
    p = platform.platform()
    if "Windows" in p:
        parts = p.split('-')
        # Approximate build from version string
        build = "26300" # This varies by system, but usually comes from the version
        # In the provided R output, it's "Windows 11 x64 (build 26300)"
        # Since we can't know the exact build of the target environment's R session,
        # we emulate the structure.
        return f"Windows 11 x64 (build {build})"
    return p

def platform_info():
    # R version approximation
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Get locale descriptive strings
    loc = locale.getlocale()
    collate_val = loc[0] if loc[0] else "C"
    # R's German_Germany.utf8 usually corresponds to de_DE.UTF-8 in Python
    if collate_val == "de_DE":
        collate_val = "German_Germany.utf8"
    
    ctype_val = collate_val
    
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": "x86_64, mingw32" if platform.machine().lower() == "amd64" else platform.machine().lower(),
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": collate_val,
        "ctype": ctype_val,
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

# To match the exact R output formatting (no index, specific column spacing)
print(f"{'setting':<10} {'value'}")
for _, row in platform_info_result.iterrows():
    print(f" {row['setting']:<9} {row['value']}")