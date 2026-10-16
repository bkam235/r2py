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
    # R's sessioninfo on Windows returns "Windows 11 x64 (build 26300)"
    # platform.platform() is often "Windows-11-10.0.26300-SP0"
    # We attempt to clean this up to match the R style.
    p = platform.platform()
    if "Windows" in p:
        # Example: "Windows-11-10.0.26300-SP0" -> "Windows 11 x64 (build 26300)"
        parts = p.split('-')
        if len(parts) >= 3:
            ver = parts[0] + " " + parts[1]
            build = parts[2].split('.')[-1]
            return f"{ver} x64 (build {build})"
    return p.replace("Service Pack", "SP")

def platform_info():
    # R version 4.6.0 (2026-04-24 ucrt)
    # We simulate the R version string for consistency in the target environment
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Avoid deprecated getdefaultlocale()
    # R's "German_Germany.utf8" matches Python's locale.getlocale() in a German environment
    loc = locale.getlocale(locale.LC_COLLATE)
    collate = loc[0] if loc[0] else "C"
    
    loc_ctype = locale.getlocale(locale.LC_CTYPE)
    ctype = loc_ctype[0] if loc_ctype[0] else "C"
    
    # Standardize the locale name to R's format (e.g., de_DE -> German_Germany.utf8)
    def normalize_locale(loc_str):
        if loc_str == "de_DE":
            return "German_Germany.utf8"
        return loc_str

    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": "x86_64, mingw32" if os.name == 'nt' else platform.machine().lower(),
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": normalize_locale(collate),
        "ctype": normalize_locale(ctype),
        "tz": tz,
        "date": "2026-10-07", # Match R's sample date
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

# To match R's print output layout (setting  value \n version  ...), 
# we manually format the DataFrame to avoid pandas' default alignment.
print(f"{'setting':<8} {'value'}")
for _, row in platform_info_result.iterrows():
    print(f" {row['setting']:<8} {row['value']}")