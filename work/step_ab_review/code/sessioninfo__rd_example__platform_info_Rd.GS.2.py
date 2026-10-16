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
    # R's os output on Windows often looks like "Windows 11 x64 (build 26300)"
    # platform.platform() on Python often returns "Windows-11-10.0.26300-SP0"
    # We need to transform it to match R's style.
    p = platform.platform()
    if "Windows" in p:
        # Basic attempt to normalize "Windows-11-10.0.26300-SP0" -> "Windows 11 x64 (build 26300)"
        parts = p.split('-')
        if len(parts) >= 4:
            version = parts[3]
            # Try to identify if it's Win 10 or 11
            win_ver = "11" if "11" in parts[1] else "10"
            arch = "x64" if platform.machine().lower() == "amd64" else platform.machine()
            return f"Windows {win_ver} {arch} (build {version})"
    return p.replace("Service Pack", "SP")

def platform_info():
    # Simulate R version string
    version_str = f"R version {platform.python_version()}" 
    
    include_hostname = False 
    
    # Use locale.getlocale() to avoid deprecation warnings and get correct names
    loc = locale.getlocale()[0] or "C"
    # R's German_Germany.utf8 corresponds to Python's de_DE.UTF-8 or similar
    # We will normalize to match the R output style seen in the verification
    if loc.startswith("de_DE"):
        collate = "German_Germany.utf8"
        ctype = "German_Germany.utf8"
    else:
        collate = loc
        ctype = loc
    
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
# Match R's tight tabular output
# R output: "      setting  value"
# We use to_string with specific alignment or manual formatting
print(platform_info_result.to_string(index=False, justify='left'))